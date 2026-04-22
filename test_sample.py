import sys
from pathlib import Path
import re

RAIZ_PROYECTO = Path.cwd().resolve()
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from src.corpus_inmuebles import preparar_corpus_para_modelado
from src.infraestructura_cpu import relevar_hardware, configurar_torch_cpu, sugerir_tamanio_muestra

RUTA_DATOS = RAIZ_PROYECTO / "data" / "entrenamiento.csv"
if not RUTA_DATOS.exists():
    RUTA_DATOS = RAIZ_PROYECTO / "data" / "entrenamiento.csv" # fallback if sample not there
TAMANIO_TEST = 0.2
SEMILLA = 42

resumen = relevar_hardware()
configurar_torch_cpu()
tamanio_muestra = sugerir_tamanio_muestra(resumen.memoria_disponible_gb)

df_muestra, df_entrenamiento, df_prueba = preparar_corpus_para_modelado(
    ruta_datos=RUTA_DATOS,
    tamanio_muestra=tamanio_muestra,
    tamanio_test=TAMANIO_TEST,
    semilla=SEMILLA,
)

# Convert all text to lower case
df_entrenamiento['descripcion'] = df_entrenamiento['descripcion'].astype(str).str.lower()

# Casa
df_casa = df_entrenamiento[df_entrenamiento['property_type'] == 'Casa']
total_casa = len(df_casa)
casa_with_keyword = df_casa['descripcion'].str.contains(r'\bcasa\b', regex=True, na=False).sum()
pct_casa = (casa_with_keyword / total_casa) * 100 if total_casa > 0 else 0
print(f"Clase Casa: {pct_casa:.2f}% contienen 'casa'")

# Departamento
df_depto = df_entrenamiento[df_entrenamiento['property_type'] == 'Departamento']
total_depto = len(df_depto)
depto_with_keyword = df_depto['descripcion'].str.contains(r'\b(departamento|depto|dpto|depto\.|dpto\.)\b', regex=True, na=False).sum()
pct_depto = (depto_with_keyword / total_depto) * 100 if total_depto > 0 else 0
print(f"Clase Departamento: {pct_depto:.2f}% contienen 'departamento', 'depto', 'dpto', 'depto.', o 'dpto.'")

# PH
df_ph = df_entrenamiento[df_entrenamiento['property_type'] == 'PH']
total_ph = len(df_ph)
ph_with_keyword = df_ph['descripcion'].str.contains(r'\b(ph|horizontal)\b', regex=True, na=False).sum()
pct_ph = (ph_with_keyword / total_ph) * 100 if total_ph > 0 else 0
print(f"Clase PH: {pct_ph:.2f}% contienen 'ph' u 'horizontal'")

