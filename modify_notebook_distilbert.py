import nbformat
import sys

nb_path = "notebooks/02_fase_4_transformer_cpu.ipynb"
with open(nb_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

caching_cell_source = """import torch
from pathlib import Path
from transformers import AutoModelForSequenceClassification, AutoTokenizer

def obtener_o_entrenar_distilbert(
    nombre_modelo_ram, 
    nombre_tokenizador_ram,
    carpeta_destino, 
    dataloader, 
    epochs, 
    learning_rate=5e-5,
    etiqueta_a_id=None,
    id_a_etiqueta=None
):
    carpeta = Path("modelos_guardados") / carpeta_destino
    
    # Capa 1: RAM
    if nombre_modelo_ram in globals() and nombre_tokenizador_ram in globals():
        print(f"✅ Cargando {nombre_modelo_ram} desde la memoria RAM...")
        return globals()[nombre_modelo_ram], globals()[nombre_tokenizador_ram]
    
    # Capa 2: Disco
    if carpeta.exists():
        print(f"✅ Cargando {nombre_modelo_ram} desde el disco ({carpeta})...")
        modelo = AutoModelForSequenceClassification.from_pretrained(carpeta)
        tokenizador = AutoTokenizer.from_pretrained(carpeta)
        return modelo, tokenizador
    
    # Capa 3: Entrenamiento
    print(f"⏳ No se encontró {nombre_modelo_ram} localmente. Iniciando entrenamiento...")
    modelo = cargar_modelo_transformer_para_clasificacion(
        cantidad_etiquetas=len(etiqueta_a_id),
        etiqueta_a_id=etiqueta_a_id,
        id_a_etiqueta=id_a_etiqueta,
    )
    tokenizador = cargar_tokenizador_transformer()
    
    historial = entrenar_transformer_en_cpu(
        modelo=modelo, 
        dataloader_entrenamiento=dataloader, 
        epochs=epochs, 
        learning_rate=learning_rate
    )
    display(historial)
    
    print(f"💾 Guardando modelo y tokenizador en {carpeta}...")
    carpeta.mkdir(parents=True, exist_ok=True)
    modelo.save_pretrained(carpeta)
    tokenizador.save_pretrained(carpeta)
    
    return modelo, tokenizador
"""

caching_cell = nbformat.v4.new_code_cell(caching_cell_source)

# We want to insert the caching cell right before Cell 6 (index 6).
nb.cells.insert(6, caching_cell)

# Now we need to modify what were previously cells 6, 8, 10
# Now they are at index 7, 9, 11

cell_6_new = """if hay_pesos_locales:
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

    dl_train, dl_test = crear_dataloaders_transformer(
        df_entrenamiento,
        df_prueba,
        tokenizador,
        etiqueta_a_id=etiqueta_a_id,
        batch_size=4,
        longitud_maxima=128,
    )

    modelo_temp, tokenizador_temp = obtener_o_entrenar_distilbert(
        nombre_modelo_ram="modelo",
        nombre_tokenizador_ram="tokenizador",
        carpeta_destino="distilbert_normal",
        dataloader=dl_train,
        epochs=1,
        learning_rate=5e-5,
        etiqueta_a_id=etiqueta_a_id,
        id_a_etiqueta=id_a_etiqueta
    )
    globals()["modelo"] = modelo_temp
    globals()["tokenizador"] = tokenizador_temp

    modelo_cuantizado = cuantizar_modelo_dinamicamente(modelo)
    pred_ids = predecir_con_transformer(modelo_cuantizado, dl_test)
    predicciones = [id_a_etiqueta[indice] for indice in pred_ids]

    print("=== Evaluación del Modelo Transformer (DistilBERT) ===")
    print(construir_reporte_clasificacion(df_prueba['property_type'], predicciones))
    display(construir_tabla_metricas(df_prueba['property_type'], predicciones))

    dibujar_matriz_confusion_profesional(
        df_prueba['property_type'],
        predicciones,
        etiquetas_ordenadas=['Departamento', 'Casa', 'PH'],
        titulo='Matriz de Confusión - DistilBERT (Transformer)'
    )
else:
    print("⚠️  No hay pesos locales del modelo.")
    print()
    print("PASOS PARA RESOLVER:")
    print("1. Ejecuta la celda anterior: 'Descargar pesos del modelo'")
    print("2. Luego ejecuta esta celda nuevamente")
    print()
    print("Primera vez: La descarga toma ~2-3 minutos (se cachea automáticamente)")
    print("Siguientes veces: Será instantáneo")
"""

cell_8_new = """from src.property_text_pipeline import COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO

# Crear dataloaders con texto censurado
dataloader_train_censurado, dataloader_prueba_censurado = crear_dataloaders_transformer(
    df_entrenamiento=df_entrenamiento,
    df_prueba=df_prueba,
    tokenizador=tokenizador,
    etiqueta_a_id=etiqueta_a_id,
    columna_texto=COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO,
)

if hay_pesos_locales: # Cambiar a True para entrenar localmente o simular
    modelo_censurado_temp, tokenizador_temp = obtener_o_entrenar_distilbert(
        nombre_modelo_ram="modelo_censurado",
        nombre_tokenizador_ram="tokenizador",
        carpeta_destino="distilbert_censurado_1ep",
        dataloader=dataloader_train_censurado,
        epochs=1,
        learning_rate=2e-5,
        etiqueta_a_id=etiqueta_a_id,
        id_a_etiqueta=id_a_etiqueta
    )
    globals()["modelo_censurado"] = modelo_censurado_temp
    globals()["tokenizador"] = tokenizador_temp

    pred_ids_censurado = predecir_con_transformer(modelo_censurado, dataloader_prueba_censurado)
    predicciones_censurado = [id_a_etiqueta[indice] for indice in pred_ids_censurado]
    print("Transformer Censurado:")
    print(construir_reporte_clasificacion(df_prueba['property_type'], predicciones_censurado))
    display(construir_tabla_metricas(df_prueba['property_type'], predicciones_censurado))
"""

cell_10_new = """# Reentrenamiento censurado con 2 epochs
if hay_pesos_locales:
    modelo_censurado_2ep_temp, tokenizador_temp = obtener_o_entrenar_distilbert(
        nombre_modelo_ram="modelo_censurado_2ep",
        nombre_tokenizador_ram="tokenizador",
        carpeta_destino="distilbert_censurado_2ep",
        dataloader=dataloader_train_censurado,
        epochs=2,
        learning_rate=2e-5,
        etiqueta_a_id=etiqueta_a_id,
        id_a_etiqueta=id_a_etiqueta
    )
    globals()["modelo_censurado_2ep"] = modelo_censurado_2ep_temp
    globals()["tokenizador"] = tokenizador_temp

    pred_ids_censurado_2ep = predecir_con_transformer(modelo_censurado_2ep, dataloader_prueba_censurado)
    predicciones_censurado_2ep = [id_a_etiqueta[indice] for indice in pred_ids_censurado_2ep]
    print("Transformer Censurado (2 epochs):")
    print(construir_reporte_clasificacion(df_prueba["property_type"], predicciones_censurado_2ep))
    display(construir_tabla_metricas(df_prueba["property_type"], predicciones_censurado_2ep))
"""

nb.cells[7].source = cell_6_new
nb.cells[9].source = cell_8_new
nb.cells[11].source = cell_10_new

with open(nb_path, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("Notebook updated successfully.")
