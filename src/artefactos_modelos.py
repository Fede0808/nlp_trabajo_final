from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib

from src.property_text_pipeline import censurar_fugas, limpiar_texto, limpiar_texto_transformer


RUTA_ARTIFACTOS = Path(__file__).resolve().parents[1] / "artifacts"
RUTA_MODELO_SVM = RUTA_ARTIFACTOS / "modelo_svm.joblib"
RUTA_MODELO_FINAL_CENSURADO = RUTA_ARTIFACTOS / "modelo_censurado_final.joblib"
ARCHIVOS_MINIMOS_TRANSFORMER = (
    "config.json",
    "model.safetensors",
    "tokenizer.json",
    "tokenizer_config.json",
    "vocab.txt",
)

PREPROCESAMIENTO_BASE = "base"
PREPROCESAMIENTO_CENSURADO = "censurado"
PREPROCESAMIENTO_TRANSFORMER_BASE = "transformer_base"
PREPROCESAMIENTO_TRANSFORMER_CENSURADO = "transformer_censurado"


@dataclass(frozen=True)
class EstadoSnapshotTransformer:
    nombre: str
    ruta: Path
    completo: bool
    archivos_faltantes: tuple[str, ...]


def obtener_ruta_modelo_svm() -> Path:
    """Devuelve la ruta canonica del artefacto del SVM."""
    return RUTA_MODELO_SVM


def obtener_ruta_modelo_final_censurado() -> Path:
    """Devuelve la ruta canonica del modelo censurado elegido para la API."""
    return RUTA_MODELO_FINAL_CENSURADO


def obtener_ruta_snapshot_transformer(nombre_variante: str) -> Path:
    """Devuelve la ruta canonica de un snapshot transformer dentro de `artifacts/`."""
    return RUTA_ARTIFACTOS / nombre_variante


def validar_snapshot_transformer(ruta_snapshot: str | Path) -> EstadoSnapshotTransformer:
    """Verifica que un snapshot local tenga los archivos minimos esperados."""
    ruta = Path(ruta_snapshot)
    faltantes = tuple(
        archivo for archivo in ARCHIVOS_MINIMOS_TRANSFORMER if not (ruta / archivo).exists()
    )
    return EstadoSnapshotTransformer(
        nombre=ruta.name,
        ruta=ruta,
        completo=not faltantes,
        archivos_faltantes=faltantes,
    )


def resolver_snapshot_transformer_local(nombre_variante: str) -> Path | None:
    """Resuelve un snapshot transformer local solo si existe y esta completo."""
    ruta = obtener_ruta_snapshot_transformer(nombre_variante)
    estado = validar_snapshot_transformer(ruta)
    if estado.completo:
        return estado.ruta
    return None


def listar_snapshots_transformer_locales() -> list[EstadoSnapshotTransformer]:
    """Lista snapshots transformer presentes en `artifacts/` con su estado de completitud."""
    estados: list[EstadoSnapshotTransformer] = []
    if not RUTA_ARTIFACTOS.exists():
        return estados

    for ruta in sorted(path for path in RUTA_ARTIFACTOS.iterdir() if path.is_dir()):
        estados.append(validar_snapshot_transformer(ruta))
    return estados


def guardar_modelo_joblib(modelo, ruta_modelo: str | Path) -> Path:
    """Persiste un pipeline clasico reusable en formato joblib."""
    ruta_destino = Path(ruta_modelo)
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, ruta_destino)
    return ruta_destino


def guardar_modelo_svm(modelo, ruta_modelo: str | Path | None = None) -> Path:
    """Persiste el pipeline completo del SVM para reutilizarlo localmente."""
    ruta_destino = Path(ruta_modelo) if ruta_modelo is not None else obtener_ruta_modelo_svm()
    return guardar_modelo_joblib(modelo, ruta_destino)


def cargar_modelo_joblib(
    ruta_modelo: str | Path,
    mensaje_error: str,
):
    """Carga un artefacto `joblib` con mensaje de error contextualizado."""
    ruta_origen = Path(ruta_modelo)
    if not ruta_origen.exists():
        raise FileNotFoundError(f"{mensaje_error} en {ruta_origen}.")
    return joblib.load(ruta_origen)


def cargar_modelo_svm(ruta_modelo: str | Path | None = None):
    """Carga el artefacto del SVM si ya fue generado por el pipeline."""
    ruta_origen = Path(ruta_modelo) if ruta_modelo is not None else obtener_ruta_modelo_svm()
    return cargar_modelo_joblib(
        ruta_origen,
        "No existe el artefacto del SVM. Ejecuta primero el notebook o script del baseline",
    )


def cargar_modelo_final_censurado(ruta_modelo: str | Path | None = None):
    """Carga el modelo clasico censurado elegido para la API final."""
    ruta_origen = (
        Path(ruta_modelo) if ruta_modelo is not None else obtener_ruta_modelo_final_censurado()
    )
    return cargar_modelo_joblib(
        ruta_origen,
        "No existe el artefacto del modelo censurado final. Recalcula el benchmark y guarda el ganador",
    )


def preprocesar_descripcion_para_modelo(
    descripcion: str,
    preprocesamiento: str = PREPROCESAMIENTO_BASE,
) -> str:
    """Aplica el preprocesamiento adecuado segun el tipo de modelo o guardrail."""
    if preprocesamiento == PREPROCESAMIENTO_BASE:
        return limpiar_texto(descripcion)
    if preprocesamiento == PREPROCESAMIENTO_CENSURADO:
        return limpiar_texto(censurar_fugas(descripcion))
    if preprocesamiento == PREPROCESAMIENTO_TRANSFORMER_BASE:
        return limpiar_texto_transformer(descripcion)
    if preprocesamiento == PREPROCESAMIENTO_TRANSFORMER_CENSURADO:
        return limpiar_texto_transformer(censurar_fugas(descripcion))
    raise ValueError(f"Preprocesamiento no soportado: {preprocesamiento}")


def predecir_tipo_propiedad(
    modelo,
    descripcion: str,
    preprocesamiento: str = PREPROCESAMIENTO_BASE,
) -> tuple[str, str]:
    """Devuelve la clase predicha y el texto limpio usado para inferencia."""
    texto_limpio = preprocesar_descripcion_para_modelo(
        descripcion,
        preprocesamiento=preprocesamiento,
    )
    clase = str(modelo.predict([texto_limpio])[0])
    return clase, texto_limpio
