from pathlib import Path
import sys
import time

RAIZ_PROYECTO = Path.cwd().resolve()
if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from src.corpus_inmuebles import preparar_corpus_para_modelado
from src.infraestructura_cpu import configurar_torch_cpu, relevar_hardware, sugerir_tamanio_muestra
from src.transformer_cpu import (
    cargar_modelo_transformer_para_clasificacion,
    cargar_tokenizador_transformer,
    construir_mapeo_etiquetas,
    crear_dataloaders_transformer,
    predecir_con_transformer,
    cuantizar_modelo_dinamicamente
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

modelo_normal = cargar_modelo_transformer_para_clasificacion(
    cantidad_etiquetas=len(etiqueta_a_id),
    etiqueta_a_id=etiqueta_a_id,
    id_a_etiqueta=id_a_etiqueta,
)

dl_train, dl_test = crear_dataloaders_transformer(
    df_entrenamiento,
    df_prueba,
    tokenizador,
    etiqueta_a_id=etiqueta_a_id,
    batch_size=4,
)

print("Starting prediction...")
start = time.time()
pred_ids = predecir_con_transformer(modelo_normal, dl_test)
print(f"Prediction took {time.time() - start:.2f} seconds")
