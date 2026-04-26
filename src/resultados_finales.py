from __future__ import annotations

from copy import deepcopy

from src.artefactos_modelos import (
    PREPROCESAMIENTO_CENSURADO,
    RUTA_MODELO_FINAL_CENSURADO,
)


FECHA_BENCHMARK_CPU = "2026-04-26"

RESULTADOS_BENCHMARK = [
    {
        "modelo": "SVM",
        "condicion": "base",
        "familia": "clasico",
        "accuracy": 0.9040,
        "f1_macro": 0.8129,
    },
    {
        "modelo": "Bayes",
        "condicion": "base",
        "familia": "clasico",
        "accuracy": 0.7850,
        "f1_macro": 0.6799,
    },
    {
        "modelo": "Reg Log",
        "condicion": "base",
        "familia": "clasico",
        "accuracy": 0.9085,
        "f1_macro": 0.8161,
    },
    {
        "modelo": "DistilBERT",
        "condicion": "base",
        "familia": "transformer",
        "accuracy": 0.9035,
        "f1_macro": 0.8292,
    },
    {
        "modelo": "SVM",
        "condicion": "censurado",
        "familia": "clasico",
        "accuracy": 0.8355,
        "f1_macro": 0.7262,
    },
    {
        "modelo": "Bayes",
        "condicion": "censurado",
        "familia": "clasico",
        "accuracy": 0.7555,
        "f1_macro": 0.6538,
    },
    {
        "modelo": "Reg Log",
        "condicion": "censurado",
        "familia": "clasico",
        "accuracy": 0.8515,
        "f1_macro": 0.7483,
    },
    {
        "modelo": "DistilBERT 1ep",
        "condicion": "censurado",
        "familia": "transformer",
        "accuracy": 0.8180,
        "f1_macro": 0.7038,
    },
    {
        "modelo": "DistilBERT 2ep",
        "condicion": "censurado",
        "familia": "transformer",
        "accuracy": 0.8165,
        "f1_macro": 0.7075,
    },
]

MODELO_API_FINAL = {
    "modelo": "Reg Log",
    "condicion": "censurado",
    "familia": "clasico",
    "accuracy": 0.8515,
    "f1_macro": 0.7483,
    "criterio_seleccion": "Mayor F1 macro; accuracy como desempate entre modelos censurados.",
    "preprocesamiento": PREPROCESAMIENTO_CENSURADO,
    "ruta_artefacto": str(RUTA_MODELO_FINAL_CENSURADO),
}

GUARDRAIL_CENSURA = {
    "se_sostiene": False,
    "hallazgo": (
        "En la corrida local del 26 de abril de 2026, todos los modelos censurados "
        "quedaron por debajo de sus equivalentes base en accuracy y F1 macro."
    ),
    "lectura": (
        "La censura funciono como control metodologico del leakage, pero no mejoro el "
        "rendimiento predictivo en este split y debe revisarse como guardrail."
    ),
}


def obtener_resultados_benchmark() -> list[dict[str, object]]:
    """Devuelve una copia lista para serializar del benchmark final."""
    return deepcopy(RESULTADOS_BENCHMARK)


def obtener_modelo_api_final() -> dict[str, object]:
    """Expone el metadata del modelo activo de la API."""
    return deepcopy(MODELO_API_FINAL)


def obtener_guardrail_censura() -> dict[str, object]:
    """Expone la conclusion metodologica sobre el escenario censurado."""
    return deepcopy(GUARDRAIL_CENSURA)


def construir_payload_benchmark() -> dict[str, object]:
    """Arma el payload compartido entre API, presentacion y documentacion."""
    return {
        "fecha_benchmark_cpu": FECHA_BENCHMARK_CPU,
        "modelo_api_final": obtener_modelo_api_final(),
        "guardrail_censura": obtener_guardrail_censura(),
        "resultados": obtener_resultados_benchmark(),
    }
