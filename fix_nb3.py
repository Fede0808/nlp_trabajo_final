import nbformat as nbf

path_03 = "notebooks/03_fase_5_comparacion_y_explicabilidad.ipynb"
with open(path_03) as f:
    nb03 = nbf.read(f, as_version=4)

markdown_setup = nbf.v4.new_markdown_cell("## Inicialización de Variables\nEsta celda carga las variables necesarias para que el notebook se ejecute correctamente de forma independiente.")
codigo_setup = nbf.v4.new_code_cell("""from pathlib import Path
import sys

RAIZ_PROYECTO = Path.cwd().resolve().parents[0] if Path.cwd().name == 'notebooks' else Path.cwd()
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from src.corpus_inmuebles import preparar_corpus_para_modelado
from src.infraestructura_cpu import configurar_torch_cpu, relevar_hardware, sugerir_tamanio_muestra
from src.transformer_cpu import (
    cargar_modelo_transformer_para_clasificacion,
    cargar_tokenizador_transformer,
    construir_mapeo_etiquetas,
    crear_dataloaders_transformer,
    predecir_con_transformer
)
from src.property_text_pipeline import COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO

RUTA_DATOS = RAIZ_PROYECTO / 'data' / 'entrenamiento.csv'
resumen = relevar_hardware()
configurar_torch_cpu()
tamanio_muestra = sugerir_tamanio_muestra(resumen.memoria_disponible_gb)

df_muestra, df_entrenamiento, df_prueba = preparar_corpus_para_modelado(
    ruta_datos=RUTA_DATOS,
    tamanio_muestra=tamanio_muestra,
    tamanio_test=0.2,
    semilla=42,
)

etiqueta_a_id, id_a_etiqueta = construir_mapeo_etiquetas(df_muestra['property_type'])
tokenizador = cargar_tokenizador_transformer()

modelo_censurado = cargar_modelo_transformer_para_clasificacion(
    cantidad_etiquetas=len(etiqueta_a_id),
    etiqueta_a_id=etiqueta_a_id,
    id_a_etiqueta=id_a_etiqueta,
)

# Cargar también un modelo normal para que no de error si lo necesita
modelo_normal = cargar_modelo_transformer_para_clasificacion(
    cantidad_etiquetas=len(etiqueta_a_id),
    etiqueta_a_id=etiqueta_a_id,
    id_a_etiqueta=id_a_etiqueta,
)""")

# Add to top (after the first markdown cell which is the title)
# Let's insert it at index 1
nb03.cells.insert(1, markdown_setup)
nb03.cells.insert(2, codigo_setup)

with open(path_03, 'w') as f:
    nbf.write(nb03, f)

print("Notebook 03 modificado con éxito.")
