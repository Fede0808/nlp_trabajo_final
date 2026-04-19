from __future__ import annotations

from pathlib import Path
from typing import Sequence

import pandas as pd
from sklearn.model_selection import train_test_split

from src.property_text_pipeline import (
    COLUMNA_OBJETIVO,
    COLUMNA_TEXTO_ORIGINAL,
    agregar_columna_texto_limpio,
)


CLASES_OBJETIVO_POR_DEFECTO = ("Departamento", "Casa", "PH")


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
    semilla: int = 42,
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
    tamanio_test: float = 0.2,
    semilla: int = 42,
    columna_texto: str = COLUMNA_TEXTO_ORIGINAL,
    columna_objetivo: str = COLUMNA_OBJETIVO,
    clases_objetivo: Sequence[str] = CLASES_OBJETIVO_POR_DEFECTO,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carga, muestrea, limpia y separa el corpus en train/test."""
    df_base = cargar_corpus_base(
        ruta_datos=ruta_datos,
        columna_texto=columna_texto,
        columna_objetivo=columna_objetivo,
        clases_objetivo=clases_objetivo,
    )
    df_muestra = muestrear_corpus_estratificado(
        df=df_base,
        tamanio_muestra=tamanio_muestra,
        columna_objetivo=columna_objetivo,
        semilla=semilla,
    )
    df_muestra = agregar_columna_texto_limpio(df_muestra)

    df_entrenamiento, df_prueba = train_test_split(
        df_muestra,
        test_size=tamanio_test,
        random_state=semilla,
        stratify=df_muestra[columna_objetivo],
    )

    return (
        df_muestra.reset_index(drop=True),
        df_entrenamiento.reset_index(drop=True),
        df_prueba.reset_index(drop=True),
    )
