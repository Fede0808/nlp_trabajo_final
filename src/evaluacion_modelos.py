from __future__ import annotations

from typing import Sequence

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import StratifiedKFold, cross_validate

from src.property_text_pipeline import (
    COLUMNA_OBJETIVO,
    COLUMNA_TEXTO_LIMPIO,
    construir_pipeline_svm,
)


def construir_tabla_metricas(
    etiquetas_reales: Sequence[str],
    etiquetas_predichas: Sequence[str],
) -> pd.DataFrame:
    """Resume metricas globales comparables entre modelos."""
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        etiquetas_reales,
        etiquetas_predichas,
        average="macro",
        zero_division=0,
    )
    precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
        etiquetas_reales,
        etiquetas_predichas,
        average="weighted",
        zero_division=0,
    )

    return pd.DataFrame(
        [
            {
                "accuracy": round(accuracy_score(etiquetas_reales, etiquetas_predichas), 4),
                "precision_macro": round(precision_macro, 4),
                "recall_macro": round(recall_macro, 4),
                "f1_macro": round(f1_macro, 4),
                "precision_weighted": round(precision_weighted, 4),
                "recall_weighted": round(recall_weighted, 4),
                "f1_weighted": round(f1_weighted, 4),
            }
        ]
    )


def construir_reporte_clasificacion(
    etiquetas_reales: Sequence[str],
    etiquetas_predichas: Sequence[str],
) -> str:
    """Genera el texto clasico de classification_report de sklearn."""
    return classification_report(
        etiquetas_reales,
        etiquetas_predichas,
        digits=4,
        zero_division=0,
    )


def construir_matriz_confusion_tabla(
    etiquetas_reales: Sequence[str],
    etiquetas_predichas: Sequence[str],
    etiquetas_ordenadas: Sequence[str],
) -> pd.DataFrame:
    """Devuelve la matriz de confusion en formato tabular."""
    matriz = confusion_matrix(
        etiquetas_reales,
        etiquetas_predichas,
        labels=list(etiquetas_ordenadas),
    )
    return pd.DataFrame(
        matriz,
        index=[f"real_{etiqueta}" for etiqueta in etiquetas_ordenadas],
        columns=[f"pred_{etiqueta}" for etiqueta in etiquetas_ordenadas],
    )


def evaluar_svm_con_validacion_cruzada(
    df: pd.DataFrame,
    columna_texto: str = COLUMNA_TEXTO_LIMPIO,
    columna_objetivo: str = COLUMNA_OBJETIVO,
    particiones: int = 5,
    semilla: int = 42,
    max_caracteristicas: int = 5000,
) -> pd.DataFrame:
    """Ejecuta validacion cruzada estratificada para el baseline SVM."""
    validador = StratifiedKFold(
        n_splits=particiones,
        shuffle=True,
        random_state=semilla,
    )
    pipeline = construir_pipeline_svm(max_caracteristicas=max_caracteristicas)
    puntajes = cross_validate(
        pipeline,
        df[columna_texto],
        df[columna_objetivo],
        cv=validador,
        scoring={
            "accuracy": "accuracy",
            "precision_macro": "precision_macro",
            "recall_macro": "recall_macro",
            "f1_macro": "f1_macro",
            "f1_weighted": "f1_weighted",
        },
        n_jobs=1,
    )

    filas = []
    for clave, valores in puntajes.items():
        if not clave.startswith("test_"):
            continue
        nombre = clave.replace("test_", "")
        serie = pd.Series(valores)
        filas.append(
            {
                "metrica": nombre,
                "media": round(float(serie.mean()), 4),
                "desvio": round(float(serie.std(ddof=0)), 4),
            }
        )

    return pd.DataFrame(filas)
