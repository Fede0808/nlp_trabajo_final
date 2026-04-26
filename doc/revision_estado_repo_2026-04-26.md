# Revision del Estado del Repo - 2026-04-26

## Resumen Ejecutivo

El repositorio está limpio en Git y representa un entregable funcional del trabajo final. La base reusable en `src/`, los notebooks por fase y la API con presentación muestran avance real y coordinación efectiva del equipo. El principal problema no es falta de desarrollo sino **cierre apurado**: quedaron artefactos auxiliares versionados, la documentación de análisis estaba vieja y algunas validaciones del flujo Transformer no están alineadas con la narrativa metodológica.

## Estado Actual

- Rama actual: `main`
- Estado local: sin cambios pendientes
- Relación con remoto: `main...origin/main`
- Commits totales: `14`
- Ventana de actividad observada: `2026-04-19` a `2026-04-25`
- Contribuyentes visibles: `Federico Blasco` (`12` commits) y `Juan Salgado Salter` (`2` commits)
- Merge commits visibles: `1`

## Lectura del Trabajo del Equipo

### Federico Blasco

Se ve un rol de conducción técnica y de empaquetado final:

- scaffold inicial;
- incorporación de consigna y documentos de gestión;
- construcción del pipeline reusable en `src/`;
- centralización de configuración reproducible;
- README, contingencias y documentos de cierre;
- API local y presentación final.

### Juan Salgado Salter

Su intervención es más corta, pero impacta sobre puntos metodológicos relevantes:

- balanceo de train/test;
- censura de leakage;
- explicabilidad;
- guardado de modelos;
- crecimiento de notebooks;
- comparativa y análisis final.

### Patrón de colaboración

No aparece un trabajo paralelo prolongado por ramas. Se observa más bien un esquema de ráfagas: Federico arma estructura y entrega, Juan entra sobre zonas metodológicas y notebooks, y el cierre vuelve a concentrarse en Federico con la demo y el merge final.

## Hallazgos Principales

### 1. Los documentos de análisis del repo estaban desactualizados

`REPOSITORY_SUMMARY.md` y `THE_STORY_OF_THIS_REPO.md` describían un estado anterior del repositorio: hablaban de `7` commits, `1` contribuyente y `0` merges, cuando Git hoy muestra `14` commits, `2` contribuyentes y `1` merge. Además mencionaban “uncommitted changes” inexistentes.

Impacto:

- reduce credibilidad del repositorio como evidencia de trabajo;
- distorsiona la lectura del aporte del equipo;
- contamina cualquier defensa basada en esos documentos.

Acción tomada:

- ambos archivos fueron actualizados para reflejar el estado real al 26 de abril de 2026.

### 2. Hay residuos de edición y patching versionados en la raíz

Archivos como `diff.patch`, `pyproject.toml.rej`, `debug.py`, `add_cells.py`, `fix_notebook.py`, `fix_nb3.py`, `modify_notebook.py`, `modify_notebook_distilbert.py` y `split_notebook.py` no forman parte del flujo descrito en `README.md` ni aparecen referenciados por el resto del código.

Impacto:

- aumentan ruido cognitivo;
- dificultan distinguir herramientas de entrega de restos accidentales;
- en el caso de `diff.patch`, inflan innecesariamente el repositorio.

Recomendación:

- moverlos a una carpeta `tools/` si siguen siendo útiles;
- o eliminarlos del versionado si fueron temporales.

### 3. La verificación del Transformer usa la columna equivocada

En `notebooks/00_cpu_shared_cleaning.py`, la tokenización de prueba del Transformer se ejecuta con `columna_texto=COLUMNA_TEXTO_LIMPIO` y luego imprime esa misma columna como si fuera la del Transformer. Eso contradice la existencia de `COLUMNA_TEXTO_LIMPIO_TRANSFORMER` como limpieza específica.

Impacto:

- la smoke test no valida realmente el camino textual del Transformer;
- puede enmascarar diferencias entre limpieza para SVM y limpieza para Transformer;
- debilita la defensa de la comparación metodológica.

Recomendación:

- usar explícitamente la columna Transformer en esa sección;
- imprimir ambas columnas cuando se quiera evidenciar la diferencia.

### 4. El flujo de test automatizado no está operativo

En el entorno local existe `.venv`, pero `pytest` no está instalado y los archivos `test_sample.py` y `test_infer.py` no están estructurados como tests de `pytest`; son scripts manuales.

Impacto:

- no hay validación automática reproducible;
- los nombres `test_*.py` pueden inducir a pensar que hay suite de tests cuando no la hay.

Recomendación:

- decidir si esos archivos son scripts de exploración o tests reales;
- si son scripts, renombrarlos y moverlos a `tools/` o `scripts/`;
- si deben ser tests, agregar `pytest` y reescribirlos como suite ejecutable.

### 5. La narrativa offline del Transformer es incompleta en ejecución

`src/transformer_cpu.py` documenta contingencia offline, pero `cargar_tokenizador_transformer()` usa `local_files_only=False` cuando no existe snapshot local. En ese escenario el código intentará resolver por red, lo que no encaja del todo con una narrativa de ejecución local controlada.

Impacto:

- el comportamiento real depende del entorno de red;
- la contingencia no falla de forma inmediata y explícita;
- la reproducibilidad offline queda parcialmente implícita.

Recomendación:

- decidir entre política estrictamente offline o política “offline si existe cache”;
- codificar esa decisión en mensajes y comportamiento.

## Validaciones Hechas

- `src.api_local.salud()` respondió `{'estado': 'ok'}` usando `.venv\\Scripts\\python.exe`.
- No fue posible ejecutar `pytest` porque el entorno local no tiene el módulo instalado.
- No se validó entrenamiento ni notebooks completos porque los datasets no están versionados.

## Archivos Mas Tocadas en el Historial Reciente

Los archivos con más recurrencia en cambios durante la ventana activa fueron:

- `.gitignore`
- `src/corpus_inmuebles.py`
- `notebooks/01_fases_1_a_3_corpus_y_svm.ipynb`
- `notebooks/02_fase_4_transformer_cpu.ipynb`
- `README.md`
- `src/evaluacion_modelos.py`
- `src/property_text_pipeline.py`
- `src/transformer_cpu.py`

Eso confirma que el esfuerzo del equipo estuvo concentrado en corpus, notebooks y comparación metodológica.

## Evaluacion Final

El repo muestra trabajo genuino y suficiente para un entregable académico serio. La arquitectura central es defendible, la narrativa por fases está presente y la capa de demo suma mucho valor. La deuda principal es de **higiene técnica y consistencia documental**, no de ausencia de implementación.

Prioridad de limpieza sugerida:

1. ordenar o eliminar artefactos auxiliares de raíz;
2. corregir la smoke test del Transformer;
3. definir una política explícita para pruebas;
4. mantener los informes del repo sincronizados con Git.
