import nbformat

nb_path = "notebooks/03_fase_5_comparacion_y_explicabilidad.ipynb"
with open(nb_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

codigo_celda_1 = """import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Resultados extraídos directamente de la Fase 4 para evitar re-ejecutar el transformer
RESULTADOS_TRANSFORMER = {
    "DistilBERT 1 epoch_Base": {"accuracy": 0.8897, "f1_macro": 0.7847},
    "DistilBERT 1 epoch_Censurado": {"accuracy": 0.8163, "f1_macro": 0.6901},
    "DistilBERT 2 epoch_Censurado": {"accuracy": 0.8353, "f1_macro": 0.7225},
}

def metricas_globales(y_true, y_pred, modelo, escenario):
    clave = f"{modelo}_{escenario}"
    if clave in RESULTADOS_TRANSFORMER:
        return RESULTADOS_TRANSFORMER[clave]
        
    if y_true is None or y_pred is None:
        return {"accuracy": "N/A", "f1_macro": "N/A"}
    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "f1_macro": round(float(precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)[2]), 4),
    }

def _entrenar_modelos_clasicos_si_falta():
    if "df_prueba" not in globals() or "df_entrenamiento" not in globals(): return
    from src.property_text_pipeline import COLUMNA_OBJETIVO, COLUMNA_TEXTO_LIMPIO, COLUMNA_TEXTO_LIMPIO_CENSURADO, entrenar_modelo_base_svm, entrenar_modelo_bayes, entrenar_modelo_logistica
    if COLUMNA_OBJETIVO not in df_entrenamiento.columns or COLUMNA_OBJETIVO not in df_prueba.columns: return

    etiquetas_entrenamiento = df_entrenamiento[COLUMNA_OBJETIVO]

    def _entrenar_y_guardar(nombre_variable, funcion_entrenamiento, columna_texto):
        if globals().get(nombre_variable, None) is not None: return
        if columna_texto not in df_entrenamiento.columns or columna_texto not in df_prueba.columns: return
        modelo = funcion_entrenamiento(df_entrenamiento, etiquetas_entrenamiento, columna_texto=columna_texto)
        globals()[nombre_variable] = modelo.predict(df_prueba[columna_texto])

    _entrenar_y_guardar("predicciones_bayes", entrenar_modelo_bayes, COLUMNA_TEXTO_LIMPIO)
    _entrenar_y_guardar("predicciones_svm", entrenar_modelo_base_svm, COLUMNA_TEXTO_LIMPIO)
    _entrenar_y_guardar("predicciones_logistica", entrenar_modelo_logistica, COLUMNA_TEXTO_LIMPIO)
    _entrenar_y_guardar("predicciones_bayes_censurado", entrenar_modelo_bayes, COLUMNA_TEXTO_LIMPIO_CENSURADO)
    _entrenar_y_guardar("predicciones_svm_censurado", entrenar_modelo_base_svm, COLUMNA_TEXTO_LIMPIO_CENSURADO)
    _entrenar_y_guardar("predicciones_logistica_censurado", entrenar_modelo_logistica, COLUMNA_TEXTO_LIMPIO_CENSURADO)

def buscar_prediccion(nombre):
    return globals().get(nombre, None)

y_real = df_prueba["property_type"] if "df_prueba" in globals() else None
if y_real is not None:
    _entrenar_modelos_clasicos_si_falta()

modelos = [
    ("Bayes", "Base", "predicciones_bayes"),
    ("SVM", "Base", "predicciones_svm"),
    ("Reg Log", "Base", "predicciones_logistica"),
    ("DistilBERT 1 epoch", "Base", None),
    ("Bayes", "Censurado", "predicciones_bayes_censurado"),
    ("SVM", "Censurado", "predicciones_svm_censurado"),
    ("Reg Log", "Censurado", "predicciones_logistica_censurado"),
    ("DistilBERT 1 epoch", "Censurado", None),
    ("DistilBERT 2 epoch", "Censurado", None),
]

tabla = []
for modelo, escenario, variable in modelos:
    y_pred = buscar_prediccion(variable) if variable else None
    tabla.append({
        "Modelo": modelo,
        "Escenario": escenario,
        **metricas_globales(y_real, y_pred, modelo, escenario),
    })

_df_tabla1 = pd.DataFrame(tabla)[["Modelo", "Escenario", "accuracy", "f1_macro"]]
df_tabla1 = _df_tabla1.rename(columns={"accuracy": "Accuracy global", "f1_macro": "F1 macro"})
print("Tabla 1: Resumen global de métricas")
display(df_tabla1)
if y_real is None:
    print("⚠️ df_prueba no está definido en el espacio de ejecución. Ejecuta previamente las celdas de carga y evaluación.")
"""

codigo_celda_2 = """import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

# Resultados extraídos directamente de la Fase 4
RESULTADOS_TRANSFORMER_CLASE = {
    "DistilBERT 1 epoch_Base": {"F1 Casa": 0.8646, "F1 Departamento": 0.9327, "F1 PH": 0.5569},
    "DistilBERT 1 epoch_Censurado": {"F1 Casa": 0.8223, "F1 Departamento": 0.8923, "F1 PH": 0.3556},
    "DistilBERT 2 epoch_Censurado": {"F1 Casa": 0.8507, "F1 Departamento": 0.8903, "F1 PH": 0.4265},
}

def f1_por_clase(y_true, y_pred, etiquetas, modelo, escenario):
    clave = f"{modelo}_{escenario}"
    if clave in RESULTADOS_TRANSFORMER_CLASE:
        return RESULTADOS_TRANSFORMER_CLASE[clave]
        
    if y_true is None or y_pred is None:
        return {f"F1 {etiq}": "N/A" for etiq in etiquetas}
        
    _, _, f1_scores, _ = precision_recall_fscore_support(y_true, y_pred, labels=etiquetas, average=None, zero_division=0)
    return {f"F1 {etiq}": round(float(v), 4) for etiq, v in zip(etiquetas, f1_scores)}

def _entrenar_modelos_clasicos_si_falta():
    if "df_prueba" not in globals() or "df_entrenamiento" not in globals(): return
    from src.property_text_pipeline import COLUMNA_OBJETIVO, COLUMNA_TEXTO_LIMPIO, COLUMNA_TEXTO_LIMPIO_CENSURADO, entrenar_modelo_base_svm, entrenar_modelo_bayes, entrenar_modelo_logistica
    if COLUMNA_OBJETIVO not in df_entrenamiento.columns or COLUMNA_OBJETIVO not in df_prueba.columns: return

    etiquetas_entrenamiento = df_entrenamiento[COLUMNA_OBJETIVO]

    def _entrenar_y_guardar(nombre_variable, funcion_entrenamiento, columna_texto):
        if globals().get(nombre_variable, None) is not None: return
        if columna_texto not in df_entrenamiento.columns or columna_texto not in df_prueba.columns: return
        modelo = funcion_entrenamiento(df_entrenamiento, etiquetas_entrenamiento, columna_texto=columna_texto)
        globals()[nombre_variable] = modelo.predict(df_prueba[columna_texto])

    _entrenar_y_guardar("predicciones_bayes", entrenar_modelo_bayes, COLUMNA_TEXTO_LIMPIO)
    _entrenar_y_guardar("predicciones_svm", entrenar_modelo_base_svm, COLUMNA_TEXTO_LIMPIO)
    _entrenar_y_guardar("predicciones_logistica", entrenar_modelo_logistica, COLUMNA_TEXTO_LIMPIO)
    _entrenar_y_guardar("predicciones_bayes_censurado", entrenar_modelo_bayes, COLUMNA_TEXTO_LIMPIO_CENSURADO)
    _entrenar_y_guardar("predicciones_svm_censurado", entrenar_modelo_base_svm, COLUMNA_TEXTO_LIMPIO_CENSURADO)
    _entrenar_y_guardar("predicciones_logistica_censurado", entrenar_modelo_logistica, COLUMNA_TEXTO_LIMPIO_CENSURADO)

etiquetas_clase = ["Casa", "Departamento", "PH"]
y_real = df_prueba["property_type"] if "df_prueba" in globals() else None
if y_real is not None:
    _entrenar_modelos_clasicos_si_falta()

modelos_a_evaluar = [
    ("Bayes", "Base", "predicciones_bayes"),
    ("SVM", "Base", "predicciones_svm"),
    ("Reg Log", "Base", "predicciones_logistica"),
    ("DistilBERT 1 epoch", "Base", None),
    ("Bayes", "Censurado", "predicciones_bayes_censurado"),
    ("SVM", "Censurado", "predicciones_svm_censurado"),
    ("Reg Log", "Censurado", "predicciones_logistica_censurado"),
    ("DistilBERT 1 epoch", "Censurado", None),
    ("DistilBERT 2 epoch", "Censurado", None),
]

tabla = []
for modelo, escenario, variable in modelos_a_evaluar:
    y_pred = globals().get(variable, None) if variable else None
    clase_f1 = f1_por_clase(y_real, y_pred, etiquetas_clase, modelo, escenario)
    tabla.append({
        "Modelo": modelo,
        "Escenario": escenario,
        "F1 Casa": clase_f1.get("F1 Casa", "N/A"),
        "F1 Departamento": clase_f1.get("F1 Departamento", "N/A"),
        "F1 PH": clase_f1.get("F1 PH", "N/A"),
    })

_df_tabla2 = pd.DataFrame(tabla)[["Modelo", "Escenario", "F1 Casa", "F1 Departamento", "F1 PH"]]
print("Tabla 2: F1 por clase")
display(_df_tabla2)
if y_real is None:
    print("⚠️ df_prueba no está definido en el espacio de ejecución. Ejecuta previamente las celdas de carga y evaluación.")
"""

for cell in nb.cells:
    if cell.cell_type == "code" and "def metricas_globales(" in cell.source:
        cell.source = codigo_celda_1
    elif cell.cell_type == "code" and "def f1_por_clase(" in cell.source:
        cell.source = codigo_celda_2

with open(nb_path, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print("✅ Notebook 03 actualizado: Las tablas ahora cargan las métricas estáticas verificadas de la Fase 4.")