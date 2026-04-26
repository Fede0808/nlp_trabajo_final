from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from src.artefactos_modelos import (
    PREPROCESAMIENTO_CENSURADO,
    guardar_modelo_joblib,
    obtener_ruta_modelo_final_censurado,
)
from src.configuracion_proyecto import RUTA_DATASET_ENTRENAMIENTO, TAMANIO_MUESTRA_OBJETIVO
from src.corpus_inmuebles import preparar_corpus_para_modelado
from src.evaluacion_modelos import construir_tabla_metricas
from src.property_text_pipeline import (
    COLUMNA_OBJETIVO,
    COLUMNA_TEXTO_LIMPIO,
    COLUMNA_TEXTO_LIMPIO_CENSURADO,
    COLUMNA_TEXTO_LIMPIO_TRANSFORMER,
    COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO,
    entrenar_modelo_base_svm,
    entrenar_modelo_bayes,
    entrenar_modelo_logistica,
)
from src.transformer_cpu import (
    cargar_modelo_transformer_para_clasificacion,
    cargar_tokenizador_transformer,
    construir_mapeo_etiquetas,
    crear_dataloaders_transformer,
    predecir_con_transformer,
)


RUTA_RESULTADOS = RAIZ / "artifacts" / "resultados_modelos_finales.csv"
RUTA_METADATA = RAIZ / "artifacts" / "modelo_api_final.json"


def _evaluar_clasicos(df_train: pd.DataFrame, df_test: pd.DataFrame) -> list[dict[str, object]]:
    y_train = df_train[COLUMNA_OBJETIVO]
    y_test = df_test[COLUMNA_OBJETIVO]
    filas: list[dict[str, object]] = []

    configuraciones = [
        ("SVM", "base", COLUMNA_TEXTO_LIMPIO, entrenar_modelo_base_svm),
        ("Bayes", "base", COLUMNA_TEXTO_LIMPIO, entrenar_modelo_bayes),
        ("Reg Log", "base", COLUMNA_TEXTO_LIMPIO, entrenar_modelo_logistica),
        ("SVM", "censurado", COLUMNA_TEXTO_LIMPIO_CENSURADO, entrenar_modelo_base_svm),
        ("Bayes", "censurado", COLUMNA_TEXTO_LIMPIO_CENSURADO, entrenar_modelo_bayes),
        ("Reg Log", "censurado", COLUMNA_TEXTO_LIMPIO_CENSURADO, entrenar_modelo_logistica),
    ]

    for modelo, condicion, columna_texto, entrenador in configuraciones:
        pipeline = entrenador(df_train, y_train, columna_texto=columna_texto)
        predicciones = pipeline.predict(df_test[columna_texto])
        metricas = construir_tabla_metricas(y_test, predicciones).iloc[0].to_dict()
        filas.append(
            {
                "modelo": modelo,
                "condicion": condicion,
                "familia": "clasico",
                "pipeline": pipeline,
                **metricas,
            }
        )

    return filas


def _evaluar_transformers(df_train: pd.DataFrame, df_test: pd.DataFrame) -> list[dict[str, object]]:
    y_train = df_train[COLUMNA_OBJETIVO]
    y_test = df_test[COLUMNA_OBJETIVO]
    etiqueta_a_id, id_a_etiqueta = construir_mapeo_etiquetas(y_train.tolist())
    filas: list[dict[str, object]] = []

    configuraciones = [
        ("DistilBERT", "base", "distilbert_normal", COLUMNA_TEXTO_LIMPIO_TRANSFORMER),
        (
            "DistilBERT 1ep",
            "censurado",
            "distilbert_censurado_1ep",
            COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO,
        ),
        (
            "DistilBERT 2ep",
            "censurado",
            "distilbert_censurado_2ep",
            COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO,
        ),
    ]

    for modelo, condicion, variante_artifacto, columna_texto in configuraciones:
        tokenizador = cargar_tokenizador_transformer(
            modo_offline=True,
            variante_artifacto=variante_artifacto,
        )
        modelo_hf = cargar_modelo_transformer_para_clasificacion(
            cantidad_etiquetas=len(etiqueta_a_id),
            etiqueta_a_id=etiqueta_a_id,
            id_a_etiqueta=id_a_etiqueta,
            variante_artifacto=variante_artifacto,
        )
        _, dataloader_prueba = crear_dataloaders_transformer(
            df_train,
            df_test,
            tokenizador,
            etiqueta_a_id,
            columna_texto=columna_texto,
            batch_size=16,
        )
        pred_ids = predecir_con_transformer(modelo_hf, dataloader_prueba)
        predicciones = [id_a_etiqueta[indice] for indice in pred_ids]
        metricas = construir_tabla_metricas(y_test, predicciones).iloc[0].to_dict()
        filas.append(
            {
                "modelo": modelo,
                "condicion": condicion,
                "familia": "transformer",
                "variante_artifacto": variante_artifacto,
                **metricas,
            }
        )

    return filas


def main() -> None:
    _, df_train, df_test = preparar_corpus_para_modelado(
        RUTA_DATASET_ENTRENAMIENTO,
        TAMANIO_MUESTRA_OBJETIVO,
    )

    filas_clasicos = _evaluar_clasicos(df_train, df_test)
    filas_transformers = _evaluar_transformers(df_train, df_test)
    filas_benchmark = filas_clasicos + filas_transformers

    df_resultados = pd.DataFrame(
        [
            {clave: valor for clave, valor in fila.items() if clave not in {"pipeline"}}
            for fila in filas_benchmark
        ]
    )
    df_resultados = df_resultados.sort_values(["condicion", "f1_macro", "accuracy"], ascending=[True, False, False])
    RUTA_RESULTADOS.parent.mkdir(parents=True, exist_ok=True)
    df_resultados.to_csv(RUTA_RESULTADOS, index=False)

    filas_censuradas = [fila for fila in filas_benchmark if fila["condicion"] == "censurado"]
    ganador = sorted(
        filas_censuradas,
        key=lambda fila: (fila["f1_macro"], fila["accuracy"]),
        reverse=True,
    )[0]

    if ganador["familia"] != "clasico":
        raise RuntimeError(
            "El ganador censurado no es un modelo clasico. La API actual espera un pipeline joblib."
        )

    guardar_modelo_joblib(ganador["pipeline"], obtener_ruta_modelo_final_censurado())

    payload = {
        "modelo": ganador["modelo"],
        "condicion": ganador["condicion"],
        "familia": ganador["familia"],
        "accuracy": ganador["accuracy"],
        "f1_macro": ganador["f1_macro"],
        "criterio_seleccion": "Mayor F1 macro; accuracy como desempate entre modelos censurados.",
        "preprocesamiento": PREPROCESAMIENTO_CENSURADO,
        "ruta_artefacto": str(obtener_ruta_modelo_final_censurado()),
    }
    RUTA_METADATA.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(df_resultados[["modelo", "condicion", "accuracy", "f1_macro"]].to_string(index=False))
    print("")
    print("Ganador censurado:", payload["modelo"])
    print("Artefacto API:", payload["ruta_artefacto"])


if __name__ == "__main__":
    main()
