# Plan por fases del TIF

## Estado general

- Fase 0: pendiente
- Fase 1: pendiente
- Fase 2: pendiente
- Fase 3: pendiente
- Fase 4: pendiente
- Fase 5: pendiente

## Fase 0 - Auditoria de hardware

**Objetivo:** relevar limites reales de CPU y RAM para fijar parametros seguros.

**Entregables:**
- script o notebook con deteccion de hardware
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

**Criterio de cierre:**
- la clase `PH` queda representada de forma suficiente
- el sampling es repetible y defendible

## Fase 2 - Pipeline NLP

**Objetivo:** limpiar y normalizar el texto con un pipeline eficiente en CPU.

**Entregables:**
- funciones de limpieza y normalizacion
- validaciones sobre nulos y columnas criticas
- configuracion de vectorizacion para baseline

**Criterio de cierre:**
- el texto final queda listo para entrenar ambos enfoques
- el pipeline se puede explicar y repetir

## Fase 3 - Baseline clasico

**Objetivo:** construir una linea base fuerte y barata en CPU.

**Entregables:**
- `TfidfVectorizer`
- `LinearSVC`
- metricas base y validacion cruzada

**Criterio de cierre:**
- existe una referencia cuantitativa clara para comparar el transformer

## Fase 4 - Modelo profundo

**Objetivo:** entrenar un transformer destilado compatible con CPU.

**Entregables:**
- modelo distilado entrenado
- configuracion de `max_length`, batch size y epochs
- inferencia cuantizada para CPU

**Criterio de cierre:**
- el modelo corre sin bloquear la maquina
- se puede comparar contra la baseline en el mismo esquema de evaluacion

## Fase 5 - Evaluacion y auditoria

**Objetivo:** cerrar la comparacion tecnica y academica entre ambos enfoques.

**Entregables:**
- precision, recall y F1 por modelo
- matriz de confusion
- analisis de errores, con foco en `PH`

**Criterio de cierre:**
- hay conclusiones tecnicas defendibles
- la recomendacion final esta alineada con la consigna y el entorno CPU-only

## Checkpoints transversales

- reproducibilidad del entorno y de los resultados
- decisiones tecnicas justificadas en terminos de CPU y memoria
- calidad comunicacional para el informe
- consideraciones eticas y de uso responsable del lenguaje
