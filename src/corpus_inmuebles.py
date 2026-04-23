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


def balancear_clases_mediante_submuestreo(
    df: pd.DataFrame,
    columna_objetivo: str = COLUMNA_OBJETIVO,
    cantidad_por_clase: int = 5000,
    semilla: int = SEMILLA_REPRODUCIBLE,
) -> pd.DataFrame:
    """Realiza submuestreo balanceado: toma igual cantidad de ejemplos por clase.
    
    Sin crear datos sintéticos. Si una clase tiene menos ejemplos que los solicitados,
    se toma todo lo disponible de esa clase.
    
    Args:
        df: DataFrame con datos
        columna_objetivo: Nombre de la columna con etiquetas
        cantidad_por_clase: Cantidad de ejemplos a tomar de cada clase (default 5000)
        semilla: Seed para reproducibilidad
    """
    dfs_balanceados = []
    for clase in df[columna_objetivo].unique():
        df_clase = df[df[columna_objetivo] == clase]
        # Tomar min(cantidad_por_clase, len(df_clase)) para no pedir más de lo disponible
        n_ejemplos = min(cantidad_por_clase, len(df_clase))
        df_clase_submuestreada = df_clase.sample(n=n_ejemplos, random_state=semilla, replace=False)
        dfs_balanceados.append(df_clase_submuestreada)
    
    df_balanceado = pd.concat(dfs_balanceados, ignore_index=True)
    return df_balanceado.sample(frac=1.0, random_state=semilla).reset_index(drop=True)


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
    tamanio_muestra: int | None = None,
    tamanio_test: float = TAMANIO_TEST,
    semilla: int = SEMILLA_REPRODUCIBLE,
    balancear_clases: bool = True,
    cantidad_entrenamiento_por_clase: int = 5000,
    cantidad_prueba_total: int | None = None,
    columna_texto: str = COLUMNA_TEXTO_ORIGINAL,
    columna_objetivo: str = COLUMNA_OBJETIVO,
    clases_objetivo: Sequence[str] = CLASES_OBJETIVO_POR_DEFECTO,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carga, muestrea, limpia y separa el corpus en train/test.

    Args:
        ruta_datos: Ruta al archivo CSV
        tamanio_muestra: Tamaño de la muestra a extraer (usado si balancear_clases=False)
        tamanio_test: Fracción para el conjunto de test (usado si balancear_clases=False)
        semilla: Seed para reproducibilidad
        balancear_clases: Si True, realiza un muestreo exacto para entrenamiento y test
        cantidad_entrenamiento_por_clase: Cuántos ejemplos por clase para entrenamiento
        cantidad_prueba_total: Cuántos ejemplos aleatorios en total para prueba. Si es None se calcula automáticamente asumiendo que train es el 70% del total.
        columna_texto: Nombre de la columna con texto original
        columna_objetivo: Nombre de la columna con etiquetas
        clases_objetivo: Clases a incluir en el análisis
    """
    df_base = cargar_corpus_base(
        ruta_datos=ruta_datos,
        columna_texto=columna_texto,
        columna_objetivo=columna_objetivo,
        clases_objetivo=clases_objetivo,
    )

    if balancear_clases:
        if cantidad_prueba_total is None:
            # Calcular cantidad de prueba total para que represente el 30% del total,
            # siendo el entrenamiento el 70% (con "n" casos por clase)
            total_train = cantidad_entrenamiento_por_clase * len(clases_objetivo)
            cantidad_prueba_total = int((total_train / 0.7) - total_train)

        dfs_entrenamiento = []
        df_restante = df_base.copy()

        for clase in clases_objetivo:
            df_clase = df_base[df_base[columna_objetivo] == clase]
            n_ejemplos = min(cantidad_entrenamiento_por_clase, len(df_clase))
            df_clase_train = df_clase.sample(n=n_ejemplos, random_state=semilla)
            dfs_entrenamiento.append(df_clase_train)
            df_restante = df_restante.drop(df_clase_train.index)

        df_entrenamiento = pd.concat(dfs_entrenamiento, ignore_index=True)

        n_prueba = min(cantidad_prueba_total, len(df_restante))
        df_prueba = df_restante.sample(n=n_prueba, random_state=semilla)

        df_entrenamiento = df_entrenamiento.sample(frac=1.0, random_state=semilla).reset_index(drop=True)
        df_prueba = df_prueba.sample(frac=1.0, random_state=semilla).reset_index(drop=True)

        df_entrenamiento = agregar_columna_texto_limpio(df_entrenamiento)
        df_prueba = agregar_columna_texto_limpio(df_prueba)

        df_muestra = pd.concat([df_entrenamiento, df_prueba], ignore_index=True)

        return (
            df_muestra,
            df_entrenamiento,
            df_prueba,
        )
    else:
        if tamanio_muestra is None:
            raise ValueError("tamanio_muestra no puede ser None cuando balancear_clases=False")

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
