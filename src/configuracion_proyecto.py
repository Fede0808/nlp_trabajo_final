from __future__ import annotations

from dataclasses import asdict, dataclass

import pandas as pd


SEMILLA_REPRODUCIBLE = 42
TAMANIO_TEST = 0.2
TAMANIO_MUESTRA_OBJETIVO = 10000
MAX_FEATURES_TFIDF = 5000
LONGITUD_MAXIMA_TRANSFORMER = 128
BATCH_SIZE_TRANSFORMER = 4
EPOCHS_TRANSFORMER = 1
NOMBRE_MODELO_TRANSFORMER = "distilbert-base-multilingual-cased"
CLASES_OBJETIVO = ("Departamento", "Casa", "PH")
COLUMNAS_DATASET = ("description", "property_type")
RUTA_DATASET_ENTRENAMIENTO = "data/entrenamiento.csv"
RUTA_DATASET_VALIDACION = "data/venta_descripcion.csv"


@dataclass(frozen=True)
class ConfiguracionProyecto:
    semilla: int = SEMILLA_REPRODUCIBLE
    tamanio_test: float = TAMANIO_TEST
    tamanio_muestra_objetivo: int = TAMANIO_MUESTRA_OBJETIVO
    max_features_tfidf: int = MAX_FEATURES_TFIDF
    longitud_maxima_transformer: int = LONGITUD_MAXIMA_TRANSFORMER
    batch_size_transformer: int = BATCH_SIZE_TRANSFORMER
    epochs_transformer: int = EPOCHS_TRANSFORMER
    nombre_modelo_transformer: str = NOMBRE_MODELO_TRANSFORMER


def construir_tabla_configuracion() -> pd.DataFrame:
    """Resume la configuracion reproducible compartida por el proyecto."""
    return pd.DataFrame([asdict(ConfiguracionProyecto())])
