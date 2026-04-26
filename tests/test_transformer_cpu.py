from __future__ import annotations

from pathlib import Path
import shutil
from uuid import uuid4

import pytest

from src import artefactos_modelos
from src import transformer_cpu


def _scratch_dir() -> Path:
    ruta = Path("artifacts") / "_pytest_scratch" / uuid4().hex
    ruta.mkdir(parents=True, exist_ok=False)
    return ruta


def test_cargar_tokenizador_offline_estricto_falla_sin_cache(monkeypatch) -> None:
    scratch = _scratch_dir()
    try:
        monkeypatch.setattr(transformer_cpu, "RAIZ_CACHE_HF", scratch)

        with pytest.raises(FileNotFoundError, match="modo offline estricto"):
            transformer_cpu.cargar_tokenizador_transformer("modelo-inexistente", modo_offline=True)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def test_cargar_tokenizador_offline_estricto_usa_snapshot_local(monkeypatch) -> None:
    scratch = _scratch_dir()
    try:
        tmp_path = scratch
        snapshot = (
            tmp_path
            / "models--distilbert-base-multilingual-cased"
            / "snapshots"
            / "abc123"
        )
        snapshot.mkdir(parents=True)
        (snapshot / "tokenizer.json").write_text("{}", encoding="utf-8")

        monkeypatch.setattr(transformer_cpu, "RAIZ_CACHE_HF", tmp_path)

        llamadas: dict[str, object] = {}

        def fake_from_pretrained(origen: str, local_files_only: bool, fix_mistral_regex: bool):
            llamadas["origen"] = origen
            llamadas["local_files_only"] = local_files_only
            llamadas["fix_mistral_regex"] = fix_mistral_regex
            return {"origen": origen}

        monkeypatch.setattr(
            transformer_cpu.AutoTokenizer,
            "from_pretrained",
            fake_from_pretrained,
        )

        resultado = transformer_cpu.cargar_tokenizador_transformer(modo_offline=True)

        assert resultado == {"origen": str(snapshot)}
        assert llamadas["origen"] == str(snapshot)
        assert llamadas["local_files_only"] is True
        assert llamadas["fix_mistral_regex"] is True
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def test_cargar_tokenizador_permite_resolucion_remota_si_se_pide(monkeypatch) -> None:
    scratch = _scratch_dir()
    try:
        monkeypatch.setattr(transformer_cpu, "RAIZ_CACHE_HF", scratch)

        llamadas: dict[str, object] = {}

        def fake_from_pretrained(origen: str, local_files_only: bool, fix_mistral_regex: bool):
            llamadas["origen"] = origen
            llamadas["local_files_only"] = local_files_only
            llamadas["fix_mistral_regex"] = fix_mistral_regex
            return {"origen": origen}

        monkeypatch.setattr(
            transformer_cpu.AutoTokenizer,
            "from_pretrained",
            fake_from_pretrained,
        )

        resultado = transformer_cpu.cargar_tokenizador_transformer(
            "modelo-remoto",
            modo_offline=False,
        )

        assert resultado == {"origen": "modelo-remoto"}
        assert llamadas["origen"] == "modelo-remoto"
        assert llamadas["local_files_only"] is False
        assert llamadas["fix_mistral_regex"] is True
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def test_cargar_tokenizador_prioriza_snapshot_local_del_proyecto(monkeypatch) -> None:
    scratch = _scratch_dir()
    try:
        tmp_path = scratch
        snapshot = tmp_path / "distilbert_censurado_2ep"
        snapshot.mkdir(parents=True)
        for archivo in (
            "config.json",
            "model.safetensors",
            "tokenizer.json",
            "tokenizer_config.json",
            "vocab.txt",
        ):
            (snapshot / archivo).write_text("{}", encoding="utf-8")

        monkeypatch.setattr(transformer_cpu, "RAIZ_CACHE_HF", tmp_path / "cache-vacio")
        monkeypatch.setattr(artefactos_modelos, "RUTA_ARTIFACTOS", tmp_path)

        llamadas: dict[str, object] = {}

        def fake_from_pretrained(origen: str, local_files_only: bool, fix_mistral_regex: bool):
            llamadas["origen"] = origen
            llamadas["local_files_only"] = local_files_only
            llamadas["fix_mistral_regex"] = fix_mistral_regex
            return {"origen": origen}

        monkeypatch.setattr(transformer_cpu.AutoTokenizer, "from_pretrained", fake_from_pretrained)

        resultado = transformer_cpu.cargar_tokenizador_transformer(
            modo_offline=True,
            variante_artifacto="distilbert_censurado_2ep",
        )

        assert resultado == {"origen": str(snapshot)}
        assert llamadas["origen"] == str(snapshot)
        assert llamadas["local_files_only"] is True
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
