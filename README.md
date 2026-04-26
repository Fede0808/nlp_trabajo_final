# TIF NLP: Clasificacion de Inmuebles (SVM vs. Transformers)

## Objetivo
Comparar modelos de clasificacion (SVM vs. Transformer destilado) para categorizar propiedades en Argentina (`Casa`, `Departamento`, `PH`) usando descripciones textuales y respetando una restriccion fuerte de CPU-only.

## Datos
- Fuente principal: `data/entrenamiento.csv`. No se versiona; ver `data/README.md`.
- Fuente de validacion: `data/venta_descripcion.csv`. No se versiona; ver `data/README.md`.
- Columnas criticas esperadas: `description` y `property_type`.
- Clases objetivo congeladas para todo el proyecto: `Departamento`, `Casa` y `PH`.
- Parametros reproducibles compartidos: `semilla=42`, `test_size=0.2`, `max_features=5000`, `max_length=128`, `batch_size=4`.

## Flujo hibrido
- `src/`: fuente de verdad reusable para hardware, corpus, limpieza, entrenamiento, evaluacion y API.
- `notebooks/`: narrativa academica, experimentos y visualizaciones por fase.
- `notebooks/00_cpu_shared_cleaning.py`: script de control reproducible para smoke tests tecnicos.

## Estado actual
- Fase 0: implementada en notebook y helpers (`src/infraestructura_cpu.py`).
- Fase 1: muestreo estratificado real implementado (`src/corpus_inmuebles.py`).
- Fase 2: limpieza unificada compartida entre SVM y Transformer (`src/property_text_pipeline.py`).
- Fase 3: baseline SVM con metricas, validacion cruzada y matriz de confusion.
- Fase 4: snapshots locales de DistilBERT integrados en `artifacts/` y evaluables en CPU-only.
- Fase 5: benchmark final corrido localmente en CPU, comparativa completa servida por `GET /benchmark` y mini-API alineada con el mejor modelo censurado.

## Entregable final esperado
- Fase 0: auditoria de hardware y politica CPU-only justificable.
- Fase 1: corpus trazable con muestreo estratificado reproducible.
- Fase 2: pipeline compartido con columna canonica `texto_limpio`.
- Fase 3: baseline `TF-IDF + LinearSVC` con validacion cruzada, matriz de confusion y artefacto serializado.
- Fase 4: enfoque profundo reproducible en CPU a partir de snapshots locales integrados.
- Fase 5: tabla comparativa final, analisis del guardrail de censura y recomendacion tecnica defendible.

## Plan Maestro e Hitos Academicos
| Fase | Tarea | Hito de la Consigna |
| :--- | :--- | :--- |
| **0** | Auditoria de Hardware | Factibilidad y entorno. |
| **1** | Curaduria del Corpus | Analisis descriptivo. |
| **2** | NLP Pipeline | Preprocesamiento de texto. |
| **3** | Baseline Clasico (SVM) | Modelo de Machine Learning. |
| **4** | Modelo Profundo (DistilBERT) | Arquitecturas de Atención. |
| **5** | Evaluacion y Auditoria | Discusion de resultados. |

## Requisitos
- venv `nlp`
- Entorno de ejecucion: CPU
- Ver `instructions.md` para detalles de implementación técnica.

## Ejecucion rapida
- Script de control: `python notebooks/00_cpu_shared_cleaning.py`
- Recalculo del benchmark final y artefacto de API: `python tools/manual_checks/benchmark_final_cpu.py`
- Notebook Fase 0: `notebooks/00_fase_0_auditoria_cpu.ipynb`
- Notebook Fases 1-3: `notebooks/01_fases_1_a_3_corpus_y_svm.ipynb`
- Notebook Fase 4: `notebooks/02_fase_4_transformer_cpu.ipynb`
- Configuracion compartida: `src/configuracion_proyecto.py`

## Guia de uso de notebooks
- Si queres rehacer el flujo completo, ejecuta `notebooks/01_fases_1_a_3_corpus_y_svm.ipynb`.
- Luego ejecuta `notebooks/02_fase_4_transformer_cpu.ipynb`.
- Sin reiniciar el kernel ni cerrar la sesion, ejecuta `notebooks/03_fase_5_comparacion_y_explicabilidad.ipynb`.
- La fase 5 reutiliza predicciones y objetos que la fase 4 deja cargados en memoria; si no estan disponibles, reconstruye las predicciones desde los snapshots locales en `artifacts/`.
- Si reinicias la sesion, verifica que los snapshots de la fase 4 sigan disponibles antes de correr la fase 5.

## Benchmark final en CPU

La corrida local consolidada el **26 de abril de 2026** arrojo estos hitos:

- Mejor modelo base por `F1 macro`: `DistilBERT` (`accuracy=0.9035`, `f1_macro=0.8292`).
- Mejor modelo base por `accuracy`: `Reg Log` (`accuracy=0.9085`, `f1_macro=0.8161`).
- Mejor modelo censurado para la API: `Reg Log` (`accuracy=0.8515`, `f1_macro=0.7483`).
- Hallazgo metodologico: la censura **no** mejoro el rendimiento frente a los modelos base; se conserva como control de leakage y queda explicitada como tension del guardrail.

## Presentacion interactiva

La presentación contiene 6 slides con resumen ejecutivo, métricas dinámicas, comparación completa base/censurado y **demo en vivo** que consulta el mejor modelo censurado del benchmark final.

### Requisitos previos

Asegúrate de haber recalculado el benchmark final local para generar el artefacto de la API en `artifacts/modelo_censurado_final.joblib`. Si no existe, ejecuta:

```bash
python tools/manual_checks/benchmark_final_cpu.py
```

Si además querés regenerar el baseline o revisar la fase clasica, podés ejecutar:

```bash
jupyter notebook notebooks/01_fases_1_a_3_corpus_y_svm.ipynb
```

### Paso 1: Lanza la API local

Desde la raíz del proyecto, abre la terminal con el entorno activado:

```bash
uvicorn src.api_local:app --reload --port 8000
```

Verás un mensaje como:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
```

**Nota importante**: La API sirve tanto la presentación como los endpoints de benchmark/predicción. No necesitas un servidor HTTP adicional.

### Paso 2: Abre la presentación en tu navegador

Ve a tu navegador favorito y accede a:

```
http://localhost:8000/presentacion
```

### Paso 3: Navega y usa la demo

- **Navegar entre slides**: Usa los botones "Anterior" y "Siguiente" o las flechas del teclado (`←` y `→`).
- **Demo en vivo**: En el panel derecho puedes ingresar una descripción de inmueble y consultar la predicción del mejor modelo censurado en tiempo real.
- **Barra de progreso**: Sigue tu avance en las 6 slides.
- **Cargar ejemplo**: Usa el botón "Cargar ejemplo" para rellenar una descripción de muestra.

### Solución de problemas

**Si ves errores 404 en CSS/JS:**
- Asegúrate de acceder por `http://localhost:8000/presentacion` (no por `file://`).
- Las rutas están configuradas para servirse desde la API.

**Si la demo dice "No disponible":**
- Verifica que el servidor FastAPI está corriendo (`uvicorn src.api_local:app...`).
- Asegúrate de que `artifacts/modelo_censurado_final.joblib` existe.
- Prueba accediendo a `http://localhost:8000/salud` - debe responder `{"estado": "ok"}`.
- Prueba accediendo a `http://localhost:8000/benchmark` - debe devolver la tabla comparativa final.

**Para detener el servidor:**

Presiona `Ctrl+C` en la terminal donde corre la API.

## Gestion del proyecto
- Contexto funcional y academico: `doc/consigna_context.md`
- Flujo de gestion seguro: `doc/project_management.md`
- Plan por fases del TIF: `doc/project_phase_plan.md`
- Contingencia del transformer: `doc/transformer_contingencia.md`
- Skills externas bajo auditoria: `doc/skill_audit_shortlist.md`
