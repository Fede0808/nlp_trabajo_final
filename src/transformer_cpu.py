from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from src.configuracion_proyecto import (
    BATCH_SIZE_TRANSFORMER,
    EPOCHS_TRANSFORMER,
    LONGITUD_MAXIMA_TRANSFORMER,
    NOMBRE_MODELO_TRANSFORMER,
)
from src.property_text_pipeline import COLUMNA_OBJETIVO, COLUMNA_TEXTO_LIMPIO_TRANSFORMER

RAIZ_CACHE_HF = Path.home() / ".cache" / "huggingface" / "hub"


@dataclass(frozen=True)
class EstadoModeloLocal:
    nombre_modelo: str
    tokenizador_disponible: bool
    pesos_modelo_disponibles: bool
    origen_tokenizador: str | None
    origen_modelo: str | None


class DatasetTextosClasificacion(Dataset):
    """Dataset minimo para fine-tuning de texto en PyTorch."""

    def __init__(
        self,
        textos: Sequence[str],
        etiquetas: Sequence[int],
        tokenizador,
        longitud_maxima: int = LONGITUD_MAXIMA_TRANSFORMER,
    ) -> None:
        self.textos = list(textos)
        self.etiquetas = list(etiquetas)
        self.tokenizador = tokenizador
        self.longitud_maxima = longitud_maxima

    def __len__(self) -> int:
        return len(self.textos)

    def __getitem__(self, indice: int) -> dict[str, torch.Tensor]:
        codificado = self.tokenizador(
            self.textos[indice],
            truncation=True,
            padding="max_length",
            max_length=self.longitud_maxima,
            return_tensors="pt",
        )
        item = {clave: valor.squeeze(0) for clave, valor in codificado.items()}
        item["labels"] = torch.tensor(self.etiquetas[indice], dtype=torch.long)
        return item


def _normalizar_nombre_modelo(nombre_modelo: str) -> str:
    return nombre_modelo.replace("/", "--")


def _resolver_snapshot_local(nombre_modelo: str) -> Path | None:
    raiz_modelo = RAIZ_CACHE_HF / f"models--{_normalizar_nombre_modelo(nombre_modelo)}" / "snapshots"
    if not raiz_modelo.exists():
        return None

    snapshots = sorted(path for path in raiz_modelo.iterdir() if path.is_dir())
    if not snapshots:
        return None
    return snapshots[-1]


def resolver_origen_tokenizador(nombre_modelo: str = NOMBRE_MODELO_TRANSFORMER) -> tuple[str, bool]:
    """Prioriza el snapshot local del tokenizador si existe."""
    snapshot = _resolver_snapshot_local(nombre_modelo)
    if snapshot and (snapshot / "tokenizer.json").exists():
        return str(snapshot), True
    return nombre_modelo, False


def resolver_origen_modelo(nombre_modelo: str = NOMBRE_MODELO_TRANSFORMER) -> tuple[str | None, bool]:
    """Devuelve origen local del modelo solo si hay pesos disponibles."""
    snapshot = _resolver_snapshot_local(nombre_modelo)
    if snapshot is None:
        return None, False

    if (snapshot / "model.safetensors").exists() or (snapshot / "pytorch_model.bin").exists():
        return str(snapshot), True
    return None, False


def relevar_estado_modelo_local(nombre_modelo: str = NOMBRE_MODELO_TRANSFORMER) -> pd.DataFrame:
    """Resume si el tokenizador y los pesos del modelo estan disponibles offline."""
    origen_tokenizador, tokenizador_local = resolver_origen_tokenizador(nombre_modelo)
    origen_modelo, modelo_local = resolver_origen_modelo(nombre_modelo)
    estado = EstadoModeloLocal(
        nombre_modelo=nombre_modelo,
        tokenizador_disponible=tokenizador_local,
        pesos_modelo_disponibles=modelo_local,
        origen_tokenizador=origen_tokenizador if tokenizador_local else None,
        origen_modelo=origen_modelo,
    )
    return pd.DataFrame([asdict(estado)])


def construir_estado_contingencia_transformer(
    nombre_modelo: str = NOMBRE_MODELO_TRANSFORMER,
) -> pd.DataFrame:
    """Resume el estado offline del transformer y la accion recomendada."""
    estado = relevar_estado_modelo_local(nombre_modelo).iloc[0].to_dict()
    pesos_disponibles = bool(estado["pesos_modelo_disponibles"])
    tokenizador_disponible = bool(estado["tokenizador_disponible"])

    if pesos_disponibles:
        bloqueo = "sin_bloqueo"
        accion = "Se puede ejecutar entrenamiento e inferencia CPU-only con el snapshot local."
    elif tokenizador_disponible:
        bloqueo = "faltan_pesos"
        accion = (
            "El tokenizador existe en cache, pero faltan pesos locales. Mantener documentada "
            "la contingencia y no presentar comparacion final del transformer como concluida."
        )
    else:
        bloqueo = "sin_cache_local"
        accion = (
            "No hay tokenizador ni pesos locales. El flujo queda preparado, pero la fase depende "
            "de cargar el modelo offline antes de entrenar."
        )

    return pd.DataFrame(
        [
            {
                **estado,
                "bloqueo": bloqueo,
                "accion_recomendada": accion,
                "batch_size_recomendado": BATCH_SIZE_TRANSFORMER,
                "longitud_maxima_recomendada": LONGITUD_MAXIMA_TRANSFORMER,
                "epochs_recomendadas": EPOCHS_TRANSFORMER,
            }
        ]
    )


def cargar_tokenizador_transformer(
    nombre_modelo: str = NOMBRE_MODELO_TRANSFORMER,
):
    """Carga el tokenizador usando cache local si esta disponible."""
    origen, es_local = resolver_origen_tokenizador(nombre_modelo)
    return AutoTokenizer.from_pretrained(
        origen,
        local_files_only=es_local,
        fix_mistral_regex=True,
    )


def construir_mapeo_etiquetas(
    etiquetas: Sequence[str],
) -> tuple[dict[str, int], dict[int, str]]:
    """Codifica etiquetas string a ids numericos estables."""
    etiquetas_ordenadas = sorted(pd.Series(etiquetas).dropna().unique().tolist())
    etiqueta_a_id = {etiqueta: indice for indice, etiqueta in enumerate(etiquetas_ordenadas)}
    id_a_etiqueta = {indice: etiqueta for etiqueta, indice in etiqueta_a_id.items()}
    return etiqueta_a_id, id_a_etiqueta


def cargar_modelo_transformer_para_clasificacion(
    cantidad_etiquetas: int,
    nombre_modelo: str = NOMBRE_MODELO_TRANSFORMER,
    etiqueta_a_id: dict[str, int] | None = None,
    id_a_etiqueta: dict[int, str] | None = None,
):
    """Carga un modelo de clasificacion solo si hay pesos disponibles offline."""
    origen_modelo, es_local = resolver_origen_modelo(nombre_modelo)
    if not es_local or origen_modelo is None:
        raise FileNotFoundError(
            "No hay pesos locales del transformer. Tokenizador disponible, pero faltan model.safetensors o pytorch_model.bin."
        )

    return AutoModelForSequenceClassification.from_pretrained(
        origen_modelo,
        local_files_only=True,
        num_labels=cantidad_etiquetas,
        label2id=etiqueta_a_id,
        id2label=id_a_etiqueta,
    )


def crear_dataloaders_transformer(
    df_entrenamiento: pd.DataFrame,
    df_prueba: pd.DataFrame,
    tokenizador,
    etiqueta_a_id: dict[str, int],
    columna_texto: str = COLUMNA_TEXTO_LIMPIO_TRANSFORMER,
    columna_objetivo: str = COLUMNA_OBJETIVO,
    batch_size: int = BATCH_SIZE_TRANSFORMER,
    longitud_maxima: int = LONGITUD_MAXIMA_TRANSFORMER,
) -> tuple[DataLoader, DataLoader]:
    """Construye dataloaders de entrenamiento y prueba listos para CPU."""
    dataset_entrenamiento = DatasetTextosClasificacion(
        textos=df_entrenamiento[columna_texto].tolist(),
        etiquetas=df_entrenamiento[columna_objetivo].map(etiqueta_a_id).tolist(),
        tokenizador=tokenizador,
        longitud_maxima=longitud_maxima,
    )
    dataset_prueba = DatasetTextosClasificacion(
        textos=df_prueba[columna_texto].tolist(),
        etiquetas=df_prueba[columna_objetivo].map(etiqueta_a_id).tolist(),
        tokenizador=tokenizador,
        longitud_maxima=longitud_maxima,
    )
    return (
        DataLoader(dataset_entrenamiento, batch_size=batch_size, shuffle=True),
        DataLoader(dataset_prueba, batch_size=batch_size, shuffle=False),
    )


def entrenar_transformer_en_cpu(
    modelo,
    dataloader_entrenamiento: DataLoader,
    epochs: int = EPOCHS_TRANSFORMER,
    learning_rate: float = 5e-5,
) -> pd.DataFrame:
    """Ejecuta un loop minimo de entrenamiento CPU-only para el transformer."""
    optimizador = torch.optim.AdamW(modelo.parameters(), lr=learning_rate)
    dispositivo = torch.device("cpu")
    modelo.to(dispositivo)
    modelo.train()

    historial = []
    for epoch in range(epochs):
        perdida_total = 0.0
        for batch in dataloader_entrenamiento:
            batch_cpu = {clave: valor.to(dispositivo) for clave, valor in batch.items()}
            optimizador.zero_grad()
            salida = modelo(**batch_cpu)
            perdida = salida.loss
            perdida.backward()
            optimizador.step()
            perdida_total += float(perdida.item())

        historial.append(
            {
                "epoch": epoch + 1,
                "loss_promedio": round(perdida_total / max(1, len(dataloader_entrenamiento)), 4),
            }
        )

    return pd.DataFrame(historial)


def predecir_con_transformer(modelo, dataloader_prueba: DataLoader) -> list[int]:
    """Obtiene ids de clase predichos para un dataloader."""
    dispositivo = torch.device("cpu")
    modelo.to(dispositivo)
    modelo.eval()

    predicciones: list[int] = []
    with torch.no_grad():
        for batch in dataloader_prueba:
            batch_cpu = {clave: valor.to(dispositivo) for clave, valor in batch.items()}
            labels = batch_cpu.pop("labels")
            _ = labels  # Se elimina solo para inferencia.
            logits = modelo(**batch_cpu).logits
            predicciones.extend(torch.argmax(logits, dim=1).cpu().tolist())

    return predicciones


def cuantizar_modelo_dinamicamente(modelo):
    """Aplica cuantizacion dinamica para acelerar inferencia en CPU."""
    return torch.quantization.quantize_dynamic(
        modelo,
        {torch.nn.Linear},
        dtype=torch.qint8,
    )
