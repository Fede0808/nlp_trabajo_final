from __future__ import annotations

import html
import re
import unicodedata
from typing import Iterable

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from src.configuracion_proyecto import (
    LONGITUD_MAXIMA_TRANSFORMER,
    MAX_FEATURES_TFIDF,
    SEMILLA_REPRODUCIBLE,
)


COLUMNA_TEXTO_LIMPIO = "texto_limpio"
COLUMNA_TEXTO_LIMPIO_CENSURADO = "texto_limpio_censurado"
COLUMNA_TEXTO_LIMPIO_TRANSFORMER = "texto_limpio_transformer"
COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO = "texto_limpio_transformer_censurado"
COLUMNA_TEXTO_ORIGINAL = "description"
COLUMNA_OBJETIVO = "property_type"
TERMINOS_CLAVE = ("expensas", "balcon", "entrada independiente")

STOP_WORDS = [
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'es', 'lo',
    'como', 'mas', 'pero', 'sus', 'le', 'ya', 'o', 'este', 'ha', 'si', 'porque', 'esta', 'son', 'entre', 'cuando', 'muy', 'sin', 'sobre'
]

_PATRON_X000D = re.compile(r"_x000d_", flags=re.IGNORECASE)
_PATRON_ETIQUETAS_HTML = re.compile(r"<[^>]+>")
_PATRON_DIGITOS = re.compile(r"\d+")
_PATRON_NO_ALFABETICO = re.compile(r"[^a-zA-ZÀ-ÿ\s]+")
_PATRON_ESPACIOS = re.compile(r"\s+")

_PATRON_AMBIENTES = re.compile(r'(\d+)\s*(amb|ambs|ambiente|ambientes)\b', flags=re.IGNORECASE)
_PATRON_DORMITORIOS = re.compile(r'(\d+)\s*(dorm|dormitorio|dormitorios)\b', flags=re.IGNORECASE)
_PATRON_PISO = re.compile(r'\b(piso|ps)\s*(\d+)\b', flags=re.IGNORECASE)
_PATRON_M2 = re.compile(r'(\d+)\s*(m2|mt2|mts|metros\s+cuadrados)\b', flags=re.IGNORECASE)


def _quitar_diacriticos(texto: str) -> str:
    normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(
        caracter for caracter in normalizado if not unicodedata.combining(caracter)
    )


def _convertir_palabras_a_digitos(texto: str) -> str:
    texto = re.sub(r'\buno\b', '1', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bdos\b', '2', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\btres\b', '3', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bcuatro\b', '4', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bcinco\b', '5', texto, flags=re.IGNORECASE)
    return texto


def _fusion_semantica(texto: str) -> str:
    texto = _PATRON_AMBIENTES.sub(r'\1_ambientes', texto)
    texto = _PATRON_DORMITORIOS.sub(r'\1_dormitorios', texto)
    texto = _PATRON_PISO.sub(r'piso_\2', texto)
    texto = _PATRON_M2.sub(r'\1_m2', texto)
    return texto


def _eliminar_stop_words(texto: str) -> str:
    palabras = texto.split()
    palabras_filtradas = [palabra for palabra in palabras if palabra.lower() not in STOP_WORDS]
    return ' '.join(palabras_filtradas)


def censurar_fugas(texto: str) -> str:
    """Elimina palabras que delatan directamente la clase (data leakage)."""
    if pd.isna(texto):
        return ""
    texto_str = str(texto)
    texto_str = re.sub(r'\bcasa\b', ' ', texto_str, flags=re.IGNORECASE)
    texto_str = re.sub(r'\b(departamento|depto|dpto)\b', ' ', texto_str, flags=re.IGNORECASE)
    texto_str = re.sub(r'\b(ph|horizontal)\b', ' ', texto_str, flags=re.IGNORECASE)
    return texto_str


def limpiar_texto(texto: str | float | None) -> str:
    """Aplica la limpieza de texto compartida por ambos enfoques (SVM y Transformer).

    Incluye normalización a dígitos, fusión semántica y limpieza agresiva.
    """
    if pd.isna(texto):
        return ""

    texto_limpio = html.unescape(str(texto))
    texto_limpio = _PATRON_X000D.sub(" ", texto_limpio)
    texto_limpio = _PATRON_ETIQUETAS_HTML.sub(" ", texto_limpio)
    texto_limpio = _PATRON_ESPACIOS.sub(" ", texto_limpio)
    texto_limpio = texto_limpio.lower()
    texto_limpio = _quitar_diacriticos(texto_limpio)
    texto_limpio = _convertir_palabras_a_digitos(texto_limpio)
    texto_limpio = _fusion_semantica(texto_limpio)
    texto_limpio = _eliminar_stop_words(texto_limpio)
    texto_limpio = re.sub(r'[^a-záéíóúñ0-9_ ]', ' ', texto_limpio)  # aggressive clean, keep digits for unigrams
    texto_limpio = _PATRON_ESPACIOS.sub(" ", texto_limpio).strip()

    return texto_limpio


def expandir_abreviaturas_inmobiliarias(texto: str) -> str:
    if not isinstance(texto, str):
        return ""
    
    diccionario = {
        r'\b(dorm|dorms|dormit)\b': 'dormitorios',
        r'\b(bño|bños|ba)\b': 'baños',
        r'\b(toil)\b': 'toilette',
        r'\b(dep serv|dep)\b': 'dependencia de servicio',
        r'\b(lav|lavad)\b': 'lavadero',
        r'\b(liv com|liv)\b': 'living comedor',
        r'\b(coc)\b': 'cocina',
        r'\b(plac)\b': 'placard',
        r'\b(c/fte|ctf|ctfte|cfte|c fte)\b': 'al contrafrente',
        r'\b(fte|frent)\b': 'al frente',
        r'\b(lat)\b': 'lateral',
        r'\b(pb|p\.b\.)\b': 'planta baja',
        r'\b(pa|p\.a\.)\b': 'planta alta',
        r'\b(ss|s\.s\.)\b': 'subsuelo',
        r'\b(s/cub|semicub)\b': 'semicubiertos',
        r'\b(cub|cubta)\b': 'cubiertos',
        r'\b(desc|descub)\b': 'descubiertos',
        r'\b(balc)\b': 'balcón',
        r'\b(terr)\b': 'terraza',
        r'\b(coch)\b': 'cochera',
        r'\b(parri)\b': 'parrilla',
        r'\b(s/exp)\b': 'sin expensas',
        r'\b(exp|expens)\b': 'expensas',
        r'\b(apto prof)\b': 'apto profesional',
        r'\b(apto cred)\b': 'apto crédito',
        r'\b(exc|excel)\b': 'excelente',
        r'\b(lum)\b': 'luminoso',
        r'\b(sum|s\.u\.m\.)\b': 'salón de usos múltiples',
        r'\b(pile)\b': 'pileta'
    }
    
    for patron, reemplazo in diccionario.items():
        texto = re.sub(patron, reemplazo, texto, flags=re.IGNORECASE)
        
    return texto


def limpiar_texto_transformer(texto: str | float | None) -> str:
    """Aplica la limpieza de texto especifica para modelos Transformer.

    Mantiene puntuacion, stop words, y expande abreviaturas a lenguaje natural.
    """
    if pd.isna(texto):
        return ""

    texto_limpio = html.unescape(str(texto))
    texto_limpio = _PATRON_X000D.sub(" ", texto_limpio)
    texto_limpio = _PATRON_ETIQUETAS_HTML.sub(" ", texto_limpio)
    texto_limpio = _PATRON_ESPACIOS.sub(" ", texto_limpio)
    
    texto_limpio = _convertir_palabras_a_digitos(texto_limpio)
    
    texto_limpio = re.sub(r'\b(\d+)\s*(m2|mt2|mts2|mts\.|mts|m²)\b', r'\1 metros cuadrados', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'\b(\d+)\s*(amb|ambs|ambiente|ambientes)\b', r'\1 ambientes', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'\b(\d+)\s*(dorm|dorms|dormitorio|dormitorios)\b', r'\1 dormitorios', texto_limpio, flags=re.IGNORECASE)
    
    texto_limpio = expandir_abreviaturas_inmobiliarias(texto_limpio)
    
    texto_limpio = _PATRON_ESPACIOS.sub(" ", texto_limpio).strip()

    return texto_limpio


def agregar_columna_texto_limpio(
    df: pd.DataFrame,
    columna_origen: str = COLUMNA_TEXTO_ORIGINAL,
    columna_destino: str = COLUMNA_TEXTO_LIMPIO,
    columna_destino_transformer: str = COLUMNA_TEXTO_LIMPIO_TRANSFORMER,
    columna_destino_censurado: str = COLUMNA_TEXTO_LIMPIO_CENSURADO,
    columna_destino_transformer_censurado: str = COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO,
) -> pd.DataFrame:
    """Crea la columna canonica de texto limpio que usan todos los modelos."""
    df_salida = df.copy()
    
    # Original (con leakage)
    df_salida[columna_destino] = df_salida[columna_origen].map(limpiar_texto)
    df_salida[columna_destino_transformer] = df_salida[columna_origen].map(limpiar_texto_transformer)
    
    # Censurado (sin leakage)
    textos_censurados = df_salida[columna_origen].map(censurar_fugas)
    df_salida[columna_destino_censurado] = textos_censurados.map(limpiar_texto)
    df_salida[columna_destino_transformer_censurado] = textos_censurados.map(limpiar_texto_transformer)
    
    assert (
        df_salida[columna_destino].isna().sum() == 0
    ), f"{columna_destino} contiene nulos"
    assert (
        df_salida[columna_destino_transformer].isna().sum() == 0
    ), f"{columna_destino_transformer} contiene nulos"
    assert (
        df_salida[columna_destino_censurado].isna().sum() == 0
    ), f"{columna_destino_censurado} contiene nulos"
    assert (
        df_salida[columna_destino_transformer_censurado].isna().sum() == 0
    ), f"{columna_destino_transformer_censurado} contiene nulos"
    
    return df_salida


def construir_ejemplos_limpieza(
    df: pd.DataFrame,
    columna_origen: str = COLUMNA_TEXTO_ORIGINAL,
    columna_limpia: str = COLUMNA_TEXTO_LIMPIO,
    tamanio_muestra: int = 5,
    semilla: int = SEMILLA_REPRODUCIBLE,
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


def construir_pipeline_svm(max_caracteristicas: int = MAX_FEATURES_TFIDF) -> Pipeline:
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
    max_caracteristicas: int = MAX_FEATURES_TFIDF,
) -> Pipeline:
    """Entrena el modelo base SVM usando la columna de texto limpio compartida."""
    assert columna_texto in df.columns, f"Falta la columna: {columna_texto}"
    modelo = construir_pipeline_svm(max_caracteristicas=max_caracteristicas)
    modelo.fit(df[columna_texto], etiquetas)
    return modelo


def entrenar_modelo_bayes(
    df: pd.DataFrame,
    etiquetas: pd.Series,
    columna_texto: str = COLUMNA_TEXTO_LIMPIO,
    max_caracteristicas: int = MAX_FEATURES_TFIDF,
) -> Pipeline:
    """Entrena el modelo Naive Bayes usando la columna de texto limpio compartida."""
    assert columna_texto in df.columns, f"Falta la columna: {columna_texto}"
    modelo = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=max_caracteristicas, lowercase=False, strip_accents=None)),
        ('clasificador', MultinomialNB())
    ])
    modelo.fit(df[columna_texto], etiquetas)
    return modelo


def entrenar_modelo_logistica(
    df: pd.DataFrame,
    etiquetas: pd.Series,
    columna_texto: str = COLUMNA_TEXTO_LIMPIO,
    max_caracteristicas: int = MAX_FEATURES_TFIDF,
) -> Pipeline:
    """Entrena el modelo de Regresión Logística usando la columna de texto limpio compartida."""
    assert columna_texto in df.columns, f"Falta la columna: {columna_texto}"
    modelo = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=max_caracteristicas, lowercase=False, strip_accents=None)),
        ('clasificador', LogisticRegression(max_iter=1000))
    ])
    modelo.fit(df[columna_texto], etiquetas)
    return modelo


def tokenizar_para_transformer(
    df: pd.DataFrame,
    tokenizador,
    columna_texto: str = COLUMNA_TEXTO_LIMPIO_TRANSFORMER,
    longitud_maxima: int = LONGITUD_MAXIMA_TRANSFORMER,
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


def limpiar_textos_para_prediccion_transformer(
    textos: Iterable[str | float | None],
) -> list[str]:
    """Limpia una lista de textos para inferencia o depuracion rapida con modelo transformer."""
    return [limpiar_texto_transformer(texto) for texto in textos]
