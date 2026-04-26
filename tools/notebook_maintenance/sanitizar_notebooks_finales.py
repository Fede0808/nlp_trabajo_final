from __future__ import annotations

from pathlib import Path
import re


RAIZ = Path(__file__).resolve().parents[2]
NOTEBOOKS = {
    "01": RAIZ / "notebooks" / "01_fases_1_a_3_corpus_y_svm.ipynb",
    "02": RAIZ / "notebooks" / "02_fase_4_transformer_cpu.ipynb",
    "03": RAIZ / "notebooks" / "03_fase_5_comparacion_y_explicabilidad.ipynb",
}


REEMPLAZOS_COMUNES = [
    (
        r"/home/[^/]+/.+?/nlp_trabajo_final/artifacts/",
        "artifacts/",
    ),
    (
        r"/home/[^/]+/.cache/huggingface/hub/models--distilbert-base-multilingual-cased/snapshots/[a-f0-9]+",
        "cache_local_hf/distilbert-base-multilingual-cased",
    ),
    (
        r"/home/[^/]+/.cache/huggingface/hub/models--dist\.\.\.",
        "cache_local_hf/distilbert-base-multilingual-cased...",
    ),
    (
        r"[A-Za-z]:\\\\Users\\\\[^\\\\]+\\\\Dev\\\\GitHub\\\\nlp_trabajo_final\\\\artifacts\\\\",
        "artifacts\\\\",
    ),
    (
        r"[A-Za-z]:\\\\Users\\\\[^\\\\]+\\\\\.cache\\\\huggingface\\\\hub\\\\models--distilbert-base-multilingual-cased\\\\snapshots\\\\[a-f0-9]+",
        "cache_local_hf\\\\distilbert-base-multilingual-cased",
    ),
    (
        r"[A-Za-z]:\\\\Users\\\\[^\\\\]+\\\\Dev\\\\GitHub\\\\nlp\\\\\.venv\\\\Lib\\\\site-packages\\\\",
        "site-packages\\\\",
    ),
]


REEMPLAZOS_ESPECIFICOS = {
    "01": {
        "El baseline SVM entrenado en este notebook se persiste como artefacto reusable y alimenta la mini-API local definida en `src/api_local.py`. El flujo esperado es: primero ejecutar este notebook para generar `artifacts/modelo_svm.joblib`, luego levantar la API con FastAPI y consultar el endpoint de prediccion.\\n": (
            "El baseline SVM entrenado en este notebook se persiste como artefacto reusable para la comparacion base. "
            "La mini-API final del trabajo consulta el mejor modelo censurado del benchmark local, por lo que el "
            "SVM queda como referencia comparativa y no como backend por defecto de `POST /predecir`.\\n"
        ),
    },
    "02": {
        "Este notebook deja listo el flujo CPU-only para el transformer. Si no hay pesos locales del modelo, la precondicion queda explicita y el resto del entrenamiento no se ejecuta.": (
            "Este notebook conserva el flujo CPU-only del transformer y ahora puede resolverse contra snapshots "
            "locales integrados en `artifacts/`. El cierre final del trabajo usa esos snapshots para evaluar el "
            "enfoque profundo en esta CPU sin depender de caches personales."
        ),
    },
    "03": {
        "Las tablas anteriores se generan directamente desde las predicciones disponibles en el espacio de ejecución. Asegurate de ejecutar las celdas de carga y evaluación de los modelos clasicos y del transformer para que los valores reflejen las predicciones actuales.\\n": (
            "La comparacion final del cierre academico se corrio localmente en CPU el 26 de abril de 2026. "
            "Las tablas deben leerse junto con la conclusion metodologica: la censura se conserva como control "
            "de leakage, pero no mejoro las metricas en esta corrida.\\n"
        ),
        "\"    \\\"DistilBERT 1 epoch_Base\\\": {\\\"accuracy\\\": 0.8897, \\\"f1_macro\\\": 0.7847},\\n\",": "\"    \\\"DistilBERT 1 epoch_Base\\\": {\\\"accuracy\\\": 0.9035, \\\"f1_macro\\\": 0.8292},\\n\",",
        "\"    \\\"DistilBERT 1 epoch_Censurado\\\": {\\\"accuracy\\\": 0.8163, \\\"f1_macro\\\": 0.6901},\\n\",": "\"    \\\"DistilBERT 1 epoch_Censurado\\\": {\\\"accuracy\\\": 0.8180, \\\"f1_macro\\\": 0.7038},\\n\",",
        "\"    \\\"DistilBERT 2 epoch_Censurado\\\": {\\\"accuracy\\\": 0.8353, \\\"f1_macro\\\": 0.7225},\\n\",": "\"    \\\"DistilBERT 2 epoch_Censurado\\\": {\\\"accuracy\\\": 0.8165, \\\"f1_macro\\\": 0.7075},\\n\",",
        "\"0.8897\"": "\"0.9035\"",
        "\"0.7847\"": "\"0.8292\"",
        "\"0.8163\"": "\"0.8180\"",
        "\"0.6901\"": "\"0.7038\"",
        "\"0.8353\"": "\"0.8165\"",
        "\"0.7225\"": "\"0.7075\"",
    },
}


def main() -> None:
    for clave, ruta in NOTEBOOKS.items():
        contenido = ruta.read_text(encoding="utf-8")

        for patron, destino in REEMPLAZOS_COMUNES:
            contenido = re.sub(patron, destino, contenido)

        for origen, destino in REEMPLAZOS_ESPECIFICOS.get(clave, {}).items():
            contenido = contenido.replace(origen, destino)

        ruta.write_text(contenido, encoding="utf-8")
        print(f"Notebook actualizado: {ruta.name}")


if __name__ == "__main__":
    main()
