# %%
from pathlib import Path
import sys

import pandas as pd
from transformers import AutoTokenizer

try:
    from IPython.display import display as ipy_display
    from IPython import get_ipython
except ImportError:
    ipy_display = None
    get_ipython = None

# %%
if "__file__" in globals():
    RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
else:
    RAIZ_PROYECTO = Path.cwd()

if str(RAIZ_PROYECTO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROYECTO))

from src.corpus_inmuebles import (
    COLUMNA_OBJETIVO,
    construir_tabla_distribucion_clases,
    preparar_corpus_para_modelado,
)
from src.artefactos_modelos import guardar_modelo_svm
from src.evaluacion_modelos import (
    construir_matriz_confusion_tabla,
    construir_reporte_clasificacion,
    construir_tabla_metricas,
    evaluar_svm_con_validacion_cruzada,
)
from src.infraestructura_cpu import (
    configurar_torch_cpu,
    liberar_memoria,
    relevar_hardware,
    resumen_hardware_como_tabla,
    sugerir_tamanio_muestra,
)
from src.property_text_pipeline import (
    COLUMNA_TEXTO_LIMPIO,
    TERMINOS_CLAVE,
    construir_auditoria_terminos,
    construir_ejemplos_limpieza,
    entrenar_modelo_base_svm,
    tokenizar_para_transformer,
)
from src.transformer_cpu import (
    NOMBRE_MODELO_TRANSFORMER,
    relevar_estado_modelo_local,
    resolver_origen_tokenizador,
)


def mostrar_tabla(titulo: str, df: pd.DataFrame) -> None:
    print(titulo)
    if ipy_display is not None and get_ipython is not None and get_ipython() is not None:
        ipy_display(df)
        return
    print(df.to_string(index=False))


# %%
RUTA_DATOS = RAIZ_PROYECTO / "data" / "entrenamiento.csv"
TAMANIO_TEST = 0.2
SEMILLA = 42


# %%
resumen_hardware = relevar_hardware()
mostrar_tabla("Auditoria de hardware", resumen_hardware_como_tabla(resumen_hardware))
hilos_torch = configurar_torch_cpu()
tamanio_muestra = sugerir_tamanio_muestra(resumen_hardware.memoria_disponible_gb)
print("Hilos configurados para torch:", hilos_torch)
print("Tamanio de muestra sugerido:", tamanio_muestra)

# %%
df_muestra, df_entrenamiento, df_prueba = preparar_corpus_para_modelado(
    ruta_datos=RUTA_DATOS,
    tamanio_muestra=tamanio_muestra,
    tamanio_test=TAMANIO_TEST,
    semilla=SEMILLA,
)

assert COLUMNA_TEXTO_LIMPIO in df_muestra.columns
assert df_muestra[COLUMNA_TEXTO_LIMPIO].isna().sum() == 0

ratio_vacios = (df_muestra[COLUMNA_TEXTO_LIMPIO].str.len() == 0).mean()
print(f"Proporcion de texto limpio vacio: {ratio_vacios:.4f}")
mostrar_tabla("Distribucion de clases en la muestra", construir_tabla_distribucion_clases(df_muestra))

# %%
ejemplos = construir_ejemplos_limpieza(df_muestra)
mostrar_tabla("Ejemplos (original -> limpio)", ejemplos)

# %%
auditoria_terminos = construir_auditoria_terminos(
    df_muestra, terminos_clave=TERMINOS_CLAVE
)
mostrar_tabla("Auditoria de terminos", auditoria_terminos)

assert COLUMNA_TEXTO_LIMPIO in df_entrenamiento.columns
assert COLUMNA_TEXTO_LIMPIO in df_prueba.columns

# %%
modelo_svm = entrenar_modelo_base_svm(
    df_entrenamiento,
    df_entrenamiento[COLUMNA_OBJETIVO],
    columna_texto=COLUMNA_TEXTO_LIMPIO,
)
predicciones_svm = modelo_svm.predict(df_prueba[COLUMNA_TEXTO_LIMPIO])

print(
    construir_reporte_clasificacion(
        df_prueba[COLUMNA_OBJETIVO],
        predicciones_svm,
    )
)
mostrar_tabla(
    "Metricas globales del SVM",
    construir_tabla_metricas(df_prueba[COLUMNA_OBJETIVO], predicciones_svm),
)
mostrar_tabla(
    "Validacion cruzada del SVM",
    evaluar_svm_con_validacion_cruzada(df_muestra),
)
mostrar_tabla(
    "Matriz de confusion del SVM",
    construir_matriz_confusion_tabla(
        df_prueba[COLUMNA_OBJETIVO],
        predicciones_svm,
        etiquetas_ordenadas=["Departamento", "Casa", "PH"],
    ),
)
ruta_modelo = guardar_modelo_svm(modelo_svm)
print("Artefacto SVM guardado en:", ruta_modelo)
liberar_memoria()

# %%
estado_transformer = relevar_estado_modelo_local(NOMBRE_MODELO_TRANSFORMER)
mostrar_tabla("Estado local del transformer", estado_transformer)

origen_tokenizador, tokenizador_es_local = resolver_origen_tokenizador(NOMBRE_MODELO_TRANSFORMER)
tokenizador = AutoTokenizer.from_pretrained(
    origen_tokenizador,
    local_files_only=tokenizador_es_local,
    fix_mistral_regex=True,
)
tokens_del_transformer = tokenizar_para_transformer(
    df_entrenamiento.head(8),
    tokenizador,
    columna_texto=COLUMNA_TEXTO_LIMPIO,
    longitud_maxima=128,
)

assert "input_ids" in tokens_del_transformer
assert len(tokens_del_transformer["input_ids"]) == 8

print("Columna de texto (SVM):", COLUMNA_TEXTO_LIMPIO)
print("Columna de texto (Transformer):", COLUMNA_TEXTO_LIMPIO)
print("Origen tokenizador:", origen_tokenizador)
