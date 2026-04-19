# TIF NLP: Clasificación de Inmuebles (SVM vs. Transformers) 🏠🇦🇷

## 🎯 Objetivo
Comparar modelos de clasificación (SVM vs. BERT) para categorizar propiedades en Argentina (Casa, Departamento, PH) basándose en descripciones textuales. El foco está en la eficiencia bajo restricciones de hardware.

## 📊 Datos
- **Fuente Principal:** `data/entrenamiento.csv` (Muestra estratificada de Properati). No se versiona; ver `data/README.md`.
- **Fuente de Validación:** `data/venta_descripcion.csv` (Zonaprop). No se versiona; ver `data/README.md`.

## 🗺️ Plan Maestro e Hitos Académicos
| Fase | Tarea | Hito de la Consigna |
| :--- | :--- | :--- |
| **0** | Auditoría de Hardware | Factibilidad y entorno. |
| **1** | Curaduría del Corpus | Análisis descriptivo. |
| **2** | NLP Pipeline | Preprocesamiento de texto. |
| **3** | Baseline Clásico (SVM) | Modelo de Machine Learning. |
| **4** | Modelo Profundo (DistilBERT) | Arquitecturas de Atención. |
| **5** | Evaluación y Auditoría | Discusión de resultados. |

## 🚀 Requisitos
- venv. nlp
- Entorno de ejecución: CPU (Optimizado para hardware local).
- Ver `instructions.md` para detalles de implementación técnica.

## 🧭 Gestion del proyecto
- Contexto funcional y academico: `doc/consigna_context.md`
- Flujo de gestion seguro: `doc/project_management.md`
- Plan por fases del TIF: `doc/project_phase_plan.md`
- Skills externas bajo auditoria: `doc/skill_audit_shortlist.md`
