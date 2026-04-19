from __future__ import annotations

from pathlib import Path

import joblib

from src.property_text_pipeline import limpiar_texto


RUTA_ARTIFACTOS = Path(__file__).resolve().parents[1] / "artifacts"
RUTA_MODELO_SVM = RUTA_ARTIFACTOS / "modelo_svm.joblib"


def obtener_ruta_modelo_svm() -> Path:
    """Devuelve la ruta canonica del artefacto del SVM."""
    return RUTA_MODELO_SVM


def guardar_modelo_svm(modelo, ruta_modelo: str | Path | None = None) -> Path:
    """Persiste el pipeline completo del SVM para reutilizarlo localmente."""
    ruta_destino = Path(ruta_modelo) if ruta_modelo is not None else obtener_ruta_modelo_svm()
    ruta_destino.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, ruta_destino)
    return ruta_destino


def cargar_modelo_svm(ruta_modelo: str | Path | None = None):
    """Carga el artefacto del SVM si ya fue generado por el pipeline."""
    ruta_origen = Path(ruta_modelo) if ruta_modelo is not None else obtener_ruta_modelo_svm()
    if not ruta_origen.exists():
        raise FileNotFoundError(
            f"No existe el artefacto del SVM en {ruta_origen}. Ejecuta primero el notebook o script del baseline."
        )
    return joblib.load(ruta_origen)


def predecir_tipo_propiedad(modelo, descripcion: str) -> tuple[str, str]:
    """Devuelve la clase predicha y el texto limpio usado para inferencia."""
    texto_limpio = limpiar_texto(descripcion)
    clase = str(modelo.predict([texto_limpio])[0])
    return clase, texto_limpio
