import nbformat as nbf
from nbformat.v4 import new_code_cell, new_markdown_cell

# 1. MODIFICAR NOTEBOOK 01
path_01 = "notebooks/01_fases_1_a_3_corpus_y_svm.ipynb"
with open(path_01) as f:
    nb01 = nbf.read(f, as_version=4)

# Agregar la celda de calculo de leakage
markdown_leakage = new_markdown_cell("## Análisis de Data Leakage\nCalculamos la cantidad de registros que contienen palabras clave que delatan su clase directamente en la descripción original.")
codigo_leakage = new_code_cell("""import pandas as pd
import re

keywords = {
    'Casa': r'\\bcasa\\b',
    'Departamento': r'\\b(?:departamento|depto|dpto)\\b',
    'PH': r'\\b(?:ph|horizontal)\\b'
}

resultados = []

for clase, patron in keywords.items():
    df_clase = df_muestra[df_muestra['property_type'] == clase]
    total = len(df_clase)
    
    con_palabra = df_clase['description'].str.lower().str.contains(patron, regex=True, na=False).sum()
    porcentaje = (con_palabra / total * 100) if total > 0 else 0
    
    resultados.append({
        'Clase': clase,
        'Total Registros': total,
        'Contienen Palabra Clave': con_palabra,
        'Porcentaje (%)': round(porcentaje, 2)
    })

df_res = pd.DataFrame(resultados)
display(df_res)""")

# Buscar donde insertarlo (luego de preparar el corpus)
insert_idx = -1
for i, cell in enumerate(nb01.cells):
    if "df_muestra, df_entrenamiento, df_prueba =" in cell.source:
        insert_idx = i + 1
        break

if insert_idx != -1:
    nb01.cells.insert(insert_idx, markdown_leakage)
    nb01.cells.insert(insert_idx + 1, codigo_leakage)

# Agregar entrenamiento de modelos censurados al final del notebook 01
markdown_censurado = new_markdown_cell("## Modelos con Datos Censurados (Sin Data Leakage)\nEntrenamos los mismos modelos pero usando la columna sin las palabras clave que delatan la clase.")
codigo_censurado = new_code_cell("""from src.property_text_pipeline import COLUMNA_TEXTO_LIMPIO_CENSURADO

# SVM Censurado
print("Entrenando SVM Censurado...")
modelo_svm_censurado = entrenar_modelo_svm(
    df=df_entrenamiento,
    etiquetas=df_entrenamiento[COLUMNA_OBJETIVO],
    columna_texto=COLUMNA_TEXTO_LIMPIO_CENSURADO,
)
predicciones_svm_censurado = modelo_svm_censurado.predict(df_prueba[COLUMNA_TEXTO_LIMPIO_CENSURADO])
print("SVM Censurado:")
display(construir_tabla_metricas(df_prueba[COLUMNA_OBJETIVO], predicciones_svm_censurado))

# Naive Bayes Censurado
print("Entrenando Naive Bayes Censurado...")
modelo_bayes_censurado = entrenar_modelo_bayes(
    df=df_entrenamiento,
    etiquetas=df_entrenamiento[COLUMNA_OBJETIVO],
    columna_texto=COLUMNA_TEXTO_LIMPIO_CENSURADO,
)
predicciones_bayes_censurado = modelo_bayes_censurado.predict(df_prueba[COLUMNA_TEXTO_LIMPIO_CENSURADO])
print("Naive Bayes Censurado:")
display(construir_tabla_metricas(df_prueba[COLUMNA_OBJETIVO], predicciones_bayes_censurado))

# Regresion Logistica Censurada
print("Entrenando Regresión Logística Censurada...")
modelo_logistica_censurado = entrenar_modelo_logistica(
    df=df_entrenamiento,
    etiquetas=df_entrenamiento[COLUMNA_OBJETIVO],
    columna_texto=COLUMNA_TEXTO_LIMPIO_CENSURADO,
)
predicciones_logistica_censurado = modelo_logistica_censurado.predict(df_prueba[COLUMNA_TEXTO_LIMPIO_CENSURADO])
print("Regresión Logística Censurada:")
display(construir_tabla_metricas(df_prueba[COLUMNA_OBJETIVO], predicciones_logistica_censurado))""")

nb01.cells.append(markdown_censurado)
nb01.cells.append(codigo_censurado)

with open(path_01, 'w') as f:
    nbf.write(nb01, f)


# 2. MODIFICAR NOTEBOOK 02 (Transformer)
path_02 = "notebooks/02_fase_4_transformer_cpu.ipynb"
with open(path_02) as f:
    nb02 = nbf.read(f, as_version=4)

markdown_transformer_censurado = new_markdown_cell("## DistilBERT con Datos Censurados (Sin Data Leakage)\nEntrenamos el transformer usando la columna sin las palabras clave.")
codigo_transformer_censurado = new_code_cell("""from src.property_text_pipeline import COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO

# Crear dataloaders con texto censurado
dataloader_train_censurado, dataloader_prueba_censurado = crear_dataloaders_transformer(
    df_entrenamiento=df_entrenamiento,
    df_prueba=df_prueba,
    tokenizador=tokenizador,
    etiqueta_a_id=etiqueta_a_id,
    columna_texto=COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO,
)

# Cargar un modelo fresco
modelo_censurado = cargar_modelo_transformer_para_clasificacion(
    cantidad_etiquetas=len(etiqueta_a_id),
    etiqueta_a_id=etiqueta_a_id,
    id_a_etiqueta=id_a_etiqueta,
)

if True: # Cambiar a True para entrenar localmente o simular
    modelo_entrenado_censurado, historial_censurado = entrenar_transformer_en_cpu(
        modelo=modelo_censurado,
        dataloader_entrenamiento=dataloader_train_censurado,
        epocas=1,  # 1 epoca para demostracion
        lr=2e-5
    )

    predicciones_censurado = predecir_con_transformer(modelo_entrenado_censurado, dataloader_prueba_censurado)
    print("Transformer Censurado:")
    print(construir_reporte_clasificacion(df_prueba['property_type'], predicciones_censurado))
    display(construir_tabla_metricas(df_prueba['property_type'], predicciones_censurado))""")

nb02.cells.append(markdown_transformer_censurado)
nb02.cells.append(codigo_transformer_censurado)

with open(path_02, 'w') as f:
    nbf.write(nb02, f)

print("Celdas agregadas a los notebooks exitosamente.")
