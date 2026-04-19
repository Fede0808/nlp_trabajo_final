# Plan por fases del TIF

## Estado general

- Fase 0: implementada en helpers y notebook; falta fijar conclusiones finales del hardware local
- Fase 1: implementada con muestreo estratificado reproducible
- Fase 2: implementada con limpieza compartida y validaciones
- Fase 3: implementada para SVM; falta consolidar resultados finales para informe
- Fase 4: preparada en codigo y notebook; bloqueada offline por ausencia de pesos locales del modelo
- Fase 5: mini-API SVM disponible; comparativa final pendiente de correr el transformer

## Fase 0 - Auditoria de hardware

**Objetivo:** relevar limites reales de CPU y RAM para fijar parametros seguros.

**Entregables:**
- `src/infraestructura_cpu.py`
- notebook `notebooks/00_fase_0_auditoria_cpu.ipynb`
- politica de threads y limpieza de memoria
- decision documentada sobre tamano de muestra inicial

**Criterio de cierre:**
- el entorno CPU-only queda caracterizado y con defaults razonables
- se puede justificar academicamente por que esos defaults protegen la maquina

## Fase 1 - Curaduria del corpus

**Objetivo:** cargar y delimitar el corpus objetivo para `Departamento`, `Casa` y `PH`.

**Entregables:**
- descripcion del dataset principal
- muestreo estratificado reproducible
- split train/test documentado
- notebook `notebooks/01_fases_1_a_3_corpus_y_svm.ipynb`

**Criterio de cierre:**
- la clase `PH` queda representada de forma suficiente
- el sampling es repetible y defendible

## Fase 2 - Pipeline NLP

**Objetivo:** limpiar y normalizar el texto con un pipeline eficiente en CPU.

**Entregables:**
- funciones de limpieza y normalizacion
- validaciones sobre nulos y columnas criticas
- configuracion de vectorizacion para baseline
- columna canonica `texto_limpio`

**Criterio de cierre:**
- el texto final queda listo para entrenar ambos enfoques
- el pipeline se puede explicar y repetir

## Fase 3 - Baseline clasico

**Objetivo:** construir una linea base fuerte y barata en CPU.

**Entregables:**
- `TfidfVectorizer`
- `LinearSVC`
- metricas base y validacion cruzada
- matriz de confusion
- artefacto serializable del SVM para API local

**Criterio de cierre:**
- existe una referencia cuantitativa clara para comparar el transformer

## Fase 4 - Modelo profundo

**Objetivo:** entrenar un transformer destilado compatible con CPU.

**Entregables:**
- modelo distilado entrenado
- configuracion de `max_length`, batch size y epochs
- inferencia cuantizada para CPU
- notebook `notebooks/02_fase_4_transformer_cpu.ipynb`
- chequeo explicito de pesos locales del modelo

**Criterio de cierre:**
- el modelo corre sin bloquear la maquina
- se puede comparar contra la baseline en el mismo esquema de evaluacion

## Fase 5 - Evaluacion y auditoria

**Objetivo:** cerrar la comparacion tecnica y academica entre ambos enfoques.

**Entregables:**
- precision, recall y F1 por modelo
- matriz de confusion
- analisis de errores, con foco en `PH`
- mini-API local del baseline SVM (`src/api_local.py`)

**Criterio de cierre:**
- hay conclusiones tecnicas defendibles
- la recomendacion final esta alineada con la consigna y el entorno CPU-only

## Checkpoints transversales

- reproducibilidad del entorno y de los resultados
- decisiones tecnicas justificadas en terminos de CPU y memoria
- calidad comunicacional para el informe
- consideraciones eticas y de uso responsable del lenguaje
