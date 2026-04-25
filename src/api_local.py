from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.artefactos_modelos import (
    cargar_modelo_svm,
    obtener_ruta_modelo_svm,
    predecir_tipo_propiedad,
)


class SolicitudPrediccion(BaseModel):
    descripcion: str = Field(..., min_length=1, description="Descripcion textual del inmueble.")


class RespuestaPrediccion(BaseModel):
    clase_predicha: str
    texto_limpio: str
    ruta_modelo: str


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
PRESENTACION_HTML = STATIC_DIR / "presentacion.html"


app = FastAPI(
    title="TIF NLP - API local de inmuebles",
    version="0.1.0",
    description="Mini-API local para consultar el baseline SVM entrenado.",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def raiz() -> RedirectResponse:
    """Redirige a la presentacion HTML principal."""
    return RedirectResponse(url="/presentacion", status_code=307)


@app.get("/presentacion", include_in_schema=False)
def presentacion() -> FileResponse:
    """Sirve la presentacion HTML local del trabajo final."""
    return FileResponse(PRESENTACION_HTML)


@app.get("/salud")
def salud() -> dict[str, str]:
    """Permite verificar que la API esta levantada."""
    return {"estado": "ok"}


@app.post("/predecir", response_model=RespuestaPrediccion)
def predecir(solicitud: SolicitudPrediccion) -> RespuestaPrediccion:
    """Predice `Casa`, `Departamento` o `PH` a partir de una descripcion."""
    try:
        modelo = cargar_modelo_svm()
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    clase_predicha, texto_limpio = predecir_tipo_propiedad(modelo, solicitud.descripcion)
    return RespuestaPrediccion(
        clase_predicha=clase_predicha,
        texto_limpio=texto_limpio,
        ruta_modelo=str(obtener_ruta_modelo_svm()),
    )
