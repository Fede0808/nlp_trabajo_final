from __future__ import annotations

import gc
import multiprocessing
import os
from dataclasses import asdict, dataclass

import pandas as pd
import psutil
import torch


PORCENTAJE_HILOS_TORCH = 0.8


@dataclass(frozen=True)
class ResumenHardware:
    nucleos_fisicos: int
    nucleos_logicos: int
    memoria_total_gb: float
    memoria_disponible_gb: float
    memoria_usada_porcentaje: float


def relevar_hardware() -> ResumenHardware:
    """Devuelve un resumen simple del hardware local relevante para CPU-only."""
    memoria = psutil.virtual_memory()
    nucleos_fisicos = psutil.cpu_count(logical=False) or multiprocessing.cpu_count()
    nucleos_logicos = psutil.cpu_count(logical=True) or multiprocessing.cpu_count()
    return ResumenHardware(
        nucleos_fisicos=nucleos_fisicos,
        nucleos_logicos=nucleos_logicos,
        memoria_total_gb=round(memoria.total / (1024**3), 2),
        memoria_disponible_gb=round(memoria.available / (1024**3), 2),
        memoria_usada_porcentaje=round(memoria.percent, 2),
    )


def resumen_hardware_como_tabla(resumen: ResumenHardware) -> pd.DataFrame:
    """Convierte el resumen de hardware en una tabla amigable para scripts/notebooks."""
    return pd.DataFrame([asdict(resumen)])


def calcular_hilos_torch(
    nucleos_logicos: int | None = None,
    porcentaje_uso: float = PORCENTAJE_HILOS_TORCH,
) -> int:
    """Calcula un numero conservador de hilos para no saturar la maquina."""
    total_logicos = nucleos_logicos or psutil.cpu_count(logical=True) or 1
    if total_logicos <= 1:
        return 1

    hilos = max(1, int(total_logicos * porcentaje_uso))
    return min(hilos, total_logicos - 1)


def configurar_torch_cpu(
    porcentaje_uso: float = PORCENTAJE_HILOS_TORCH,
) -> int:
    """Configura PyTorch para CPU con una politica defensiva de hilos."""
    hilos = calcular_hilos_torch(porcentaje_uso=porcentaje_uso)
    torch.set_num_threads(hilos)

    try:
        torch.set_num_interop_threads(max(1, min(2, hilos)))
    except RuntimeError:
        # Puede fallar si ya se inicializo el runtime; en ese caso mantenemos los hilos.
        pass

    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    return hilos


def sugerir_tamanio_muestra(memoria_disponible_gb: float | None = None) -> int:
    """Sugiere un tamanio inicial de muestra compatible con CPU y RAM local."""
    memoria = memoria_disponible_gb
    if memoria is None:
        memoria = relevar_hardware().memoria_disponible_gb

    if memoria < 4:
        return 4000
    if memoria < 8:
        return 6000
    if memoria < 12:
        return 8000
    if memoria < 20:
        return 10000
    if memoria < 32:
        return 12000
    return 15000


def liberar_memoria() -> int:
    """Fuerza una pasada de GC para liberar memoria entre etapas pesadas."""
    return gc.collect()
