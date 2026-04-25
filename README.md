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
- Fase 4: flujo CPU-only preparado, pero el entrenamiento completo requiere pesos locales del modelo.
- Fase 5: mini-API local para el SVM disponible en `src/api_local.py`; la comparativa final queda sujeta a correr el transformer.

## Entregable final esperado
- Fase 0: auditoria de hardware y politica CPU-only justificable.
- Fase 1: corpus trazable con muestreo estratificado reproducible.
- Fase 2: pipeline compartido con columna canonica `texto_limpio`.
- Fase 3: baseline `TF-IDF + LinearSVC` con validacion cruzada, matriz de confusion y artefacto serializado.
- Fase 4: transformer destilado en CPU o contingencia formal documentada si faltan pesos locales.
- Fase 5: tabla comparativa final, analisis de errores por clase y recomendacion tecnica defendible.

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
- Notebook Fase 0: `notebooks/00_fase_0_auditoria_cpu.ipynb`
- Notebook Fases 1-3: `notebooks/01_fases_1_a_3_corpus_y_svm.ipynb`
- Notebook Fase 4: `notebooks/02_fase_4_transformer_cpu.ipynb`
- Configuracion compartida: `src/configuracion_proyecto.py`

## Presentacion interactiva

La presentación contiene 6 slides con resumen ejecutivo, métricas, comparación de modelos y **demo en vivo** que consulta el modelo SVM.

### Requisitos previos

Asegúrate de que el modelo SVM ha sido entrenado y está disponible en `artifacts/modelo_svm.joblib`. Si no existe, ejecuta primero:

```bash
python notebooks/00_cpu_shared_cleaning.py
```

O abre y ejecuta el notebook:

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

**Nota importante**: La API sirve tanto la presentación como los endpoints de predicción. No necesitas un servidor HTTP adicional.

### Paso 2: Abre la presentación en tu navegador

Ve a tu navegador favorito y accede a:

```
http://localhost:8000/presentacion
```

### Paso 3: Navega y usa la demo

- **Navegar entre slides**: Usa los botones "Anterior" y "Siguiente" o las flechas del teclado (`←` y `→`).
- **Demo en vivo**: En el panel derecho puedes ingresar una descripción de inmueble y consultar la predicción del modelo SVM en tiempo real.
- **Barra de progreso**: Sigue tu avance en las 6 slides.
- **Cargar ejemplo**: Usa el botón "Cargar ejemplo" para rellenar una descripción de muestra.

### Solución de problemas

**Si ves errores 404 en CSS/JS:**
- Asegúrate de acceder por `http://localhost:8000/presentacion` (no por `file://`).
- Las rutas están configuradas para servirse desde la API.

**Si la demo dice "No disponible":**
- Verifica que el servidor FastAPI está corriendo (`uvicorn src.api_local:app...`).
- Asegúrate de que `artifacts/modelo_svm.joblib` existe.
- Prueba accediendo a `http://localhost:8000/salud` - debe responder `{"estado": "ok"}`.

**Para detener el servidor:**

Presiona `Ctrl+C` en la terminal donde corre la API.

## Gestion del proyecto
- Contexto funcional y academico: `doc/consigna_context.md`
- Flujo de gestion seguro: `doc/project_management.md`
- Plan por fases del TIF: `doc/project_phase_plan.md`
- Contingencia del transformer: `doc/transformer_contingencia.md`
- Skills externas bajo auditoria: `doc/skill_audit_shortlist.md`
