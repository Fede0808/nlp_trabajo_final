from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pandas as pd
from sklearn.model_selection import train_test_split

from src.configuracion_proyecto import CLASES_OBJETIVO, SEMILLA_REPRODUCIBLE, TAMANIO_TEST
from src.property_text_pipeline import (
    COLUMNA_OBJETIVO,
    COLUMNA_TEXTO_ORIGINAL,
    agregar_columna_texto_limpio,
)


CLASES_OBJETIVO_POR_DEFECTO = CLASES_OBJETIVO


def cargar_corpus_base(
    ruta_datos: str | Path,
    columna_texto: str = COLUMNA_TEXTO_ORIGINAL,
    columna_objetivo: str = COLUMNA_OBJETIVO,
    clases_objetivo: Sequence[str] = CLASES_OBJETIVO_POR_DEFECTO,
) -> pd.DataFrame:
    """Carga solo las columnas necesarias y filtra las clases del problema."""
    ruta_csv = Path(ruta_datos)
    df = pd.read_csv(ruta_csv, usecols=[columna_texto, columna_objetivo])
    df = df[df[columna_objetivo].isin(clases_objetivo)].copy()
    return df.reset_index(drop=True)


def muestrear_corpus_estratificado(
    df: pd.DataFrame,
    tamanio_muestra: int,
    columna_objetivo: str = COLUMNA_OBJETIVO,
    semilla: int = SEMILLA_REPRODUCIBLE,
) -> pd.DataFrame:
    """Obtiene una muestra estratificada exacta manteniendo la proporcion de clases."""
    if tamanio_muestra <= 0:
        raise ValueError("tamanio_muestra debe ser mayor a cero")

    if tamanio_muestra >= len(df):
        return df.sample(frac=1.0, random_state=semilla).reset_index(drop=True)

    _, df_muestra = train_test_split(
        df,
        test_size=tamanio_muestra,
        random_state=semilla,
        stratify=df[columna_objetivo],
    )
    return df_muestra.reset_index(drop=True)


def construir_tabla_distribucion_clases(
    df: pd.DataFrame,
    columna_objetivo: str = COLUMNA_OBJETIVO,
) -> pd.DataFrame:
    """Resume la distribucion de clases en conteo absoluto y porcentaje."""
    conteos = df[columna_objetivo].value_counts(dropna=False)
    porcentajes = (conteos / len(df) * 100).round(2)
    tabla = pd.DataFrame(
        {
            "clase": conteos.index,
            "cantidad": conteos.values,
            "porcentaje": porcentajes.values,
        }
    )
    return tabla


def preparar_corpus_para_modelado(
    ruta_datos: str | Path,
    tamanio_muestra: int,
    tamanio_test: float = TAMANIO_TEST,
    semilla: int = SEMILLA_REPRODUCIBLE,
    columna_texto: str = COLUMNA_TEXTO_ORIGINAL,
    columna_objetivo: str = COLUMNA_OBJETIVO,
    clases_objetivo: Sequence[str] = CLASES_OBJETIVO_POR_DEFECTO,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carga, muestrea, limpia y separa el corpus en train/test.

    El flujo de datos es el siguiente:
    1. se define un tamaño de muestra total ``tamanio_muestra`` según el hardware;
    2. se extrae un conjunto de prueba estratificado de tamaño ``tamanio_test * tamanio_muestra``
       a partir del corpus original, conservando las proporciones de clases del dataset;
    3. el conjunto de entrenamiento se arma con el resto de datos y se submuestrea
       de forma balanceada en partes iguales por clase hasta alcanzar aproximadamente
       ``(1 - tamanio_test) * tamanio_muestra`` registros.

    De esta manera, todos los modelos usan el mismo ``df_entrenamiento`` y ``df_prueba``
    base, aunque cada modelo aplique su propio tratamiento de texto.

    Args:
        ruta_datos: Ruta al archivo CSV
        tamanio_muestra: Tamaño total de la muestra definida por el hardware
        tamanio_test: Fracción del conjunto total que se reserva para prueba
        semilla: Seed para reproducibilidad
        columna_texto: Nombre de la columna con texto original
        columna_objetivo: Nombre de la columna con etiquetas
        clases_objetivo: Clases a incluir en el análisis
    """
    if tamanio_muestra is None:
        raise ValueError("tamanio_muestra no puede ser None")

    df_base = cargar_corpus_base(
        ruta_datos=ruta_datos,
        columna_texto=columna_texto,
        columna_objetivo=columna_objetivo,
        clases_objetivo=clases_objetivo,
    )

    tamanio_prueba = max(1, int(tamanio_muestra * tamanio_test))
    tamanio_entrenamiento = tamanio_muestra - tamanio_prueba

    df_entrenamiento_original, df_prueba = train_test_split(
        df_base,
        test_size=tamanio_prueba,
        random_state=semilla,
        stratify=df_base[columna_objetivo],
    )

    # Balancear el entrenamiento con partes iguales por clase.
    cantidad_por_clase = tamanio_entrenamiento // len(clases_objetivo)
    resto = tamanio_entrenamiento % len(clases_objetivo)

    dfs_entrenamiento = []
    for indice, clase in enumerate(clases_objetivo):
        n_ejemplos = cantidad_por_clase + (1 if indice < resto else 0)
        df_clase = df_entrenamiento_original[df_entrenamiento_original[columna_objetivo] == clase]
        if len(df_clase) < n_ejemplos:
            raise ValueError(
                f"No hay suficientes ejemplos de la clase {clase} para construir un entrenamiento balanceado."
            )
        dfs_entrenamiento.append(df_clase.sample(n=n_ejemplos, random_state=semilla))

    df_entrenamiento = pd.concat(dfs_entrenamiento, ignore_index=True)
    df_entrenamiento = df_entrenamiento.sample(frac=1.0, random_state=semilla).reset_index(drop=True)
    df_prueba = df_prueba.sample(frac=1.0, random_state=semilla).reset_index(drop=True)

    df_entrenamiento = agregar_columna_texto_limpio(df_entrenamiento)
    df_prueba = agregar_columna_texto_limpio(df_prueba)

    df_muestra = pd.concat([df_entrenamiento, df_prueba], ignore_index=True)

    return (
        df_muestra.reset_index(drop=True),
        df_entrenamiento.reset_index(drop=True),
        df_prueba.reset_index(drop=True),
    )
