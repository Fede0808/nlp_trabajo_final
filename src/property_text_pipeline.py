from __future__ import annotations

import html
import re
import unicodedata
from typing import Iterable

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


COLUMNA_TEXTO_LIMPIO = "texto_limpio"
COLUMNA_TEXTO_ORIGINAL = "description"
COLUMNA_OBJETIVO = "property_type"
TERMINOS_CLAVE = ("expensas", "balcon", "entrada independiente")

_PATRON_X000D = re.compile(r"_x000d_", flags=re.IGNORECASE)
_PATRON_ETIQUETAS_HTML = re.compile(r"<[^>]+>")
_PATRON_DIGITOS = re.compile(r"\d+")
_PATRON_NO_ALFABETICO = re.compile(r"[^a-zA-ZÀ-ÿ\s]+")
_PATRON_ESPACIOS = re.compile(r"\s+")


def _quitar_diacriticos(texto: str) -> str:
    normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(
        caracter for caracter in normalizado if not unicodedata.combining(caracter)
    )


def limpiar_texto(texto: str | float | None) -> str:
    """Aplica la limpieza de texto compartida por ambos enfoques (SVM y Transformer).

    Nota: la tokenizacion posterior (TF-IDF a nivel palabra vs subpalabras del
    Transformer) es distinta, pero la limpieza previa es identica.
    """
    if pd.isna(texto):
        return ""

    texto_limpio = html.unescape(str(texto))
    texto_limpio = _PATRON_X000D.sub(" ", texto_limpio)
    texto_limpio = _PATRON_ETIQUETAS_HTML.sub(" ", texto_limpio)
    texto_limpio = _PATRON_ESPACIOS.sub(" ", texto_limpio)
    texto_limpio = _PATRON_DIGITOS.sub(" ", texto_limpio)
    texto_limpio = _PATRON_NO_ALFABETICO.sub(" ", texto_limpio)
    texto_limpio = texto_limpio.lower()
    texto_limpio = _quitar_diacriticos(texto_limpio)
    texto_limpio = _PATRON_ESPACIOS.sub(" ", texto_limpio).strip()

    return texto_limpio


def agregar_columna_texto_limpio(
    df: pd.DataFrame,
    columna_origen: str = COLUMNA_TEXTO_ORIGINAL,
    columna_destino: str = COLUMNA_TEXTO_LIMPIO,
) -> pd.DataFrame:
    """Crea la columna canonica de texto limpio que usan todos los modelos."""
    df_salida = df.copy()
    df_salida[columna_destino] = df_salida[columna_origen].map(limpiar_texto)
    assert (
        df_salida[columna_destino].isna().sum() == 0
    ), f"{columna_destino} contiene nulos"
    return df_salida


def construir_ejemplos_limpieza(
    df: pd.DataFrame,
    columna_origen: str = COLUMNA_TEXTO_ORIGINAL,
    columna_limpia: str = COLUMNA_TEXTO_LIMPIO,
    tamanio_muestra: int = 5,
    semilla: int = 42,
) -> pd.DataFrame:
    """Devuelve una muestra original->limpio para verificar visualmente la limpieza."""
    disponibles = df[[columna_origen, columna_limpia]].drop_duplicates()
    return disponibles.sample(
        n=min(tamanio_muestra, len(disponibles)),
        random_state=semilla,
    )


def construir_auditoria_terminos(
    df: pd.DataFrame,
    columna_origen: str = COLUMNA_TEXTO_ORIGINAL,
    columna_limpia: str = COLUMNA_TEXTO_LIMPIO,
    terminos_clave: Iterable[str] = TERMINOS_CLAVE,
) -> pd.DataFrame:
    """Compara presencia de terminos antes y despues de la limpieza."""
    texto_original_normalizado = (
        df[columna_origen]
        .fillna("")
        .map(lambda valor: _quitar_diacriticos(html.unescape(str(valor))).lower())
    )
    texto_limpio = df[columna_limpia].fillna("")

    filas = []
    for termino in terminos_clave:
        filas.append(
            {
                "termino": termino,
                "coincidencias_original": int(
                    texto_original_normalizado.str.contains(termino, regex=False).sum()
                ),
                "coincidencias_limpio": int(
                    texto_limpio.str.contains(termino, regex=False).sum()
                ),
            }
        )

    return pd.DataFrame(filas)


def construir_pipeline_svm(max_caracteristicas: int = 5000) -> Pipeline:
    """Construye el modelo base clasico (TF-IDF + LinearSVC) sin normalizaciones extra."""
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=max_caracteristicas,
                    lowercase=False,
                    strip_accents=None,
                ),
            ),
            ("clasificador", LinearSVC()),
        ]
    )


def entrenar_modelo_base_svm(
    df: pd.DataFrame,
    etiquetas: pd.Series,
    columna_texto: str = COLUMNA_TEXTO_LIMPIO,
    max_caracteristicas: int = 5000,
) -> Pipeline:
    """Entrena el modelo base SVM usando la columna de texto limpio compartida."""
    assert columna_texto in df.columns, f"Falta la columna: {columna_texto}"
    modelo = construir_pipeline_svm(max_caracteristicas=max_caracteristicas)
    modelo.fit(df[columna_texto], etiquetas)
    return modelo


def tokenizar_para_transformer(
    df: pd.DataFrame,
    tokenizador,
    columna_texto: str = COLUMNA_TEXTO_LIMPIO,
    longitud_maxima: int = 128,
):
    """Tokeniza la columna de texto limpio sin aplicar limpieza adicional."""
    assert columna_texto in df.columns, f"Falta la columna: {columna_texto}"
    textos = df[columna_texto].fillna("").astype(str).tolist()
    return tokenizador(
        textos,
        truncation=True,
        padding=True,
        max_length=longitud_maxima,
    )


def limpiar_textos_para_prediccion(
    textos: Iterable[str | float | None],
) -> list[str]:
    """Limpia una lista de textos para inferencia o depuracion rapida."""
    return [limpiar_texto(texto) for texto in textos]
