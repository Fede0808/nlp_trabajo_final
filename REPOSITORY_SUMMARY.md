# Repository Analysis: nlp_trabajo_final

## Overview

`nlp_trabajo_final` es un proyecto académico de NLP orientado a clasificar avisos inmobiliarios de Argentina en tres clases (`Casa`, `Departamento`, `PH`) a partir de descripciones textuales. El objetivo técnico del repositorio es comparar un baseline clásico (`TF-IDF + LinearSVC`) contra un flujo Transformer destilado bajo una restricción explícita de ejecución `CPU-only`.

El repositorio combina código reusable, notebooks por fase y documentación de entrega. La intención metodológica es buena: congelar configuración, compartir limpieza textual entre experimentos y mantener una narrativa reproducible para la defensa del trabajo final.

## Architecture

La estructura real del proyecto queda dividida en cuatro capas:

- `src/`: fuente de verdad del pipeline reusable.
- `notebooks/`: ejecución narrativa por fases y experimentación.
- `doc/`: contexto académico, planificación y cierre.
- `data/` y `artifacts/`: insumos y salidas locales no versionadas.

Los módulos más importantes son:

- `src/configuracion_proyecto.py`: parámetros compartidos de reproducibilidad.
- `src/infraestructura_cpu.py`: relevamiento de hardware y política CPU-only.
- `src/corpus_inmuebles.py`: carga, filtrado, muestreo y split train/test.
- `src/property_text_pipeline.py`: limpieza, censura de leakage y pipelines clásicos.
- `src/evaluacion_modelos.py`: métricas, validación cruzada y matrices de confusión.
- `src/transformer_cpu.py`: disponibilidad offline del modelo, tokenización y entrenamiento CPU.
- `src/artefactos_modelos.py`: persistencia e inferencia del SVM.
- `src/api_local.py`: API local y frontend de presentación.

## Current Repository Shape

El árbol versionado mezcla tres categorías distintas:

- activos centrales del proyecto: `src/`, `README.md`, notebooks principales y documentación de fase;
- activos de entrega: presentación HTML/CSS/JS servida por FastAPI;
- artefactos auxiliares de edición: `diff.patch`, `pyproject.toml.rej`, `add_cells.py`, `fix_notebook.py`, `fix_nb3.py`, `modify_notebook.py`, `modify_notebook_distilbert.py`, `split_notebook.py`, `debug.py`, `test_sample.py`, `test_infer.py`.

Ese tercer grupo no está integrado al flujo documentado y hoy agrega ruido técnico.

## Technologies Used

- Python 3.11+
- `pandas`
- `scikit-learn`
- `torch`
- `transformers`
- `fastapi`
- `uvicorn`
- `matplotlib`
- `seaborn`
- `uv`

## Data Flow

El flujo principal es:

1. Se carga `data/entrenamiento.csv`.
2. Se filtran las tres clases objetivo.
3. Se construye una muestra estratificada condicionada por hardware.
4. Se separa train/test.
5. Se agregan columnas limpias para SVM y Transformer.
6. El baseline SVM se entrena, evalúa y serializa.
7. La API reutiliza el artefacto SVM para inferencia local.
8. El flujo Transformer depende de la disponibilidad offline del tokenizador y de los pesos.

## Team and Ownership

El historial visible muestra trabajo de dos personas:

- **Federico Blasco**: 12 commits. Lidera el scaffold, la documentación, los módulos base en `src/`, la API local y la presentación final.
- **Juan Salgado Salter**: 2 commits. Su aporte está concentrado en ajustes metodológicos relevantes: balanceo de train/test, censura de leakage, explicabilidad, guardado de modelos y expansión de notebooks.

El patrón de colaboración no es el de un equipo paralelo sostenido, sino el de una integración corta sobre `main`, con un pico de actividad entre el 19 y el 25 de abril de 2026 y un merge final el 25 de abril de 2026.

## Technical Assessment

Fortalezas:

- Hay una separación razonable entre lógica reusable y narrativa de notebook.
- La restricción CPU-only está explicitada y atraviesa diseño, documentación y API.
- La fase de cierre incorporó una presentación navegable y una demo local.

Debilidades:

- Hay artefactos accidentales versionados en la raíz.
- Los archivos `REPOSITORY_SUMMARY.md` y `THE_STORY_OF_THIS_REPO.md` estaban desactualizados y describían un repo distinto.
- No hay un flujo de tests automatizados operativo en el entorno actual.
- La verificación “smoke test” del Transformer usa la columna SVM en lugar de la columna específica del Transformer.
- El tokenizador puede intentar descargar recursos de red cuando no existe caché local, lo que contradice parcialmente la narrativa offline.

## Current State

Al 26 de abril de 2026, el repo está limpio desde Git (`main` sincronizado con `origin/main`) y representa un entregable funcional, pero con deuda de prolijidad. El baseline SVM y la API local parecen estar en estado utilizable; el camino Transformer está preparado conceptualmente, aunque todavía tiene dependencia operativa de caché/pesos locales y señales de verificación incompleta.
