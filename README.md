# TIF NLP: Clasificacion de Inmuebles (SVM vs. Transformers)

## Objetivo
Comparar modelos de clasificacion (SVM vs. Transformer destilado) para categorizar propiedades en Argentina (`Casa`, `Departamento`, `PH`) usando descripciones textuales y respetando una restriccion fuerte de CPU-only.

## Datos
- Fuente principal: `data/entrenamiento.csv`. No se versiona; ver `data/README.md`.
- Fuente de validacion: `data/venta_descripcion.csv`. No se versiona; ver `data/README.md`.

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
- API local del SVM: `uvicorn src.api_local:app --reload`

## Gestion del proyecto
- Contexto funcional y academico: `doc/consigna_context.md`
- Flujo de gestion seguro: `doc/project_management.md`
- Plan por fases del TIF: `doc/project_phase_plan.md`
- Skills externas bajo auditoria: `doc/skill_audit_shortlist.md`
