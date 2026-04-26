from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.artefactos_modelos import (
    cargar_modelo_final_censurado,
    predecir_tipo_propiedad,
)
from src.resultados_finales import construir_payload_benchmark, obtener_modelo_api_final


class SolicitudPrediccion(BaseModel):
    descripcion: str = Field(..., min_length=1, description="Descripcion textual del inmueble.")


class RespuestaPrediccion(BaseModel):
    clase_predicha: str
    texto_limpio: str
    modelo_activo: str
    condicion_modelo: str
    ruta_modelo: str


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
PRESENTACION_HTML = STATIC_DIR / "presentacion.html"
PRESENTACION_CSS = STATIC_DIR / "presentacion.css"
PRESENTACION_JS = STATIC_DIR / "presentacion.js"


app = FastAPI(
    title="TIF NLP - API local de inmuebles",
    version="0.1.0",
    description="Mini-API local para consultar el mejor modelo censurado del benchmark final.",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@lru_cache(maxsize=1)
def _cargar_modelo_activo_api():
    metadata = obtener_modelo_api_final()
    return cargar_modelo_final_censurado(metadata["ruta_artefacto"])


@app.get("/", include_in_schema=False)
def raiz() -> RedirectResponse:
    """Redirige a la presentacion HTML principal."""
    return RedirectResponse(url="/presentacion", status_code=307)


@app.get("/presentacion", include_in_schema=False)
def presentacion() -> FileResponse:
    """Sirve la presentacion HTML local del trabajo final."""
    return FileResponse(PRESENTACION_HTML)


@app.get("/presentacion.css", include_in_schema=False)
def presentacion_css() -> FileResponse:
    """Sirve el stylesheet esperado por la presentacion cuando se abre en /presentacion."""
    return FileResponse(PRESENTACION_CSS, media_type="text/css")


@app.get("/presentacion.js", include_in_schema=False)
def presentacion_js() -> FileResponse:
    """Sirve el script esperado por la presentacion cuando se abre en /presentacion."""
    return FileResponse(PRESENTACION_JS, media_type="application/javascript")


@app.get("/salud")
def salud() -> dict[str, str]:
    """Permite verificar que la API esta levantada."""
    return {"estado": "ok"}


@app.get("/benchmark")
def benchmark() -> dict[str, object]:
    """Expone la comparativa final y el modelo activo de la API."""
    return construir_payload_benchmark()


@app.post("/predecir", response_model=RespuestaPrediccion)
def predecir(solicitud: SolicitudPrediccion) -> RespuestaPrediccion:
    """Predice `Casa`, `Departamento` o `PH` a partir de una descripcion."""
    metadata = obtener_modelo_api_final()
    try:
        modelo = _cargar_modelo_activo_api()
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    clase_predicha, texto_limpio = predecir_tipo_propiedad(
        modelo,
        solicitud.descripcion,
        preprocesamiento=str(metadata["preprocesamiento"]),
    )
    return RespuestaPrediccion(
        clase_predicha=clase_predicha,
        texto_limpio=texto_limpio,
        modelo_activo=str(metadata["modelo"]),
        condicion_modelo=str(metadata["condicion"]),
        ruta_modelo=str(metadata["ruta_artefacto"]),
    )
