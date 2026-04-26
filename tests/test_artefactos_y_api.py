from __future__ import annotations

from pathlib import Path
import shutil
from uuid import uuid4

import pytest

from src import api_local
from src.api_local import SolicitudPrediccion, benchmark, salud
from src.artefactos_modelos import (
    PREPROCESAMIENTO_CENSURADO,
    cargar_modelo_svm,
    validar_snapshot_transformer,
)


def _scratch_dir() -> Path:
    ruta = Path("artifacts") / "_pytest_scratch" / uuid4().hex
    ruta.mkdir(parents=True, exist_ok=False)
    return ruta


def test_cargar_modelo_svm_informa_falta_de_artefacto() -> None:
    scratch = _scratch_dir()
    try:
        ruta_modelo = scratch / "modelo_svm.joblib"

        with pytest.raises(FileNotFoundError, match="No existe el artefacto del SVM"):
            cargar_modelo_svm(ruta_modelo)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def test_salud_api_local_responde_ok() -> None:
    assert salud() == {"estado": "ok"}


def test_benchmark_expone_modelo_activo_y_guardrail() -> None:
    payload = benchmark()

    assert payload["modelo_api_final"]["modelo"] == "Reg Log"
    assert payload["modelo_api_final"]["condicion"] == "censurado"
    assert payload["guardrail_censura"]["se_sostiene"] is False
    assert payload["fecha_benchmark_cpu"] == "2026-04-26"


def test_predecir_usa_el_modelo_censurado_activo(monkeypatch) -> None:
    class FakeModel:
        def predict(self, textos: list[str]) -> list[str]:
            assert len(textos) == 1
            assert "casa" not in textos[0]
            return ["PH"]

    monkeypatch.setattr(api_local, "_cargar_modelo_activo_api", lambda: FakeModel())
    monkeypatch.setattr(
        api_local,
        "obtener_modelo_api_final",
        lambda: {
            "modelo": "Reg Log",
            "condicion": "censurado",
            "preprocesamiento": PREPROCESAMIENTO_CENSURADO,
            "ruta_artefacto": "artifacts/modelo_censurado_final.joblib",
        },
    )

    respuesta = api_local.predecir(SolicitudPrediccion(descripcion="Casa con patio y entrada independiente"))

    assert respuesta.clase_predicha == "PH"
    assert respuesta.modelo_activo == "Reg Log"
    assert respuesta.condicion_modelo == "censurado"
    assert "casa" not in respuesta.texto_limpio


def test_validar_snapshot_transformer_detecta_archivos_faltantes() -> None:
    scratch = _scratch_dir()
    try:
        snapshot = scratch / "distilbert_local"
        snapshot.mkdir()
        (snapshot / "config.json").write_text("{}", encoding="utf-8")

        estado = validar_snapshot_transformer(snapshot)

        assert estado.completo is False
        assert "model.safetensors" in estado.archivos_faltantes
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
