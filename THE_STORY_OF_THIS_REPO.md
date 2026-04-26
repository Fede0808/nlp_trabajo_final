# The Story of nlp_trabajo_final

## The Build Window

Este repositorio no creció lentamente. Se armó en una ventana muy corta y muy intensa entre el **19 y el 25 de abril de 2026**. En esos siete días quedó definido casi todo: estructura, consigna, pipeline reutilizable, notebooks, controles de reproducibilidad, fase Transformer y una presentación final servida por API.

El historial no muestra una evolución larga; muestra un cierre académico con varias capas superpuestas en pocos días.

## A Year in Numbers

- Commits totales: `14`
- Commits en el último año: `14`
- Contribuyentes visibles: `2`
- Meses activos en el último año: `1`
- Mes más activo: `2026-04`
- Merge commits visibles: `1`

Distribución por autor:

- `Federico Blasco`: `12` commits
- `Juan Salgado Salter`: `2` commits

## Cast of Characters

### Federico Blasco

Federico aparece como responsable del armazón del repositorio y de su capa de entrega:

- crea el scaffold inicial;
- incorpora la consigna y el contexto;
- ordena la higiene de Git y la planificación;
- sube los módulos CPU-only en `src/`;
- documenta fases y configuración reproducible;
- agrega la API local y la presentación final.

Su firma domina la arquitectura y la narrativa del proyecto.

### Juan Salgado Salter

Juan interviene menos veces, pero en zonas metodológicas importantes:

- balanceo y redefinición de `train/test`;
- censura de leakage por clase;
- explicabilidad;
- guardado de modelos;
- ampliación de notebooks y comparativa final.

También introduce bastante tooling ad hoc en la raíz, lo que sugiere trabajo práctico de ajuste rápido sobre notebooks, con costo posterior de prolijidad.

## The Main Themes

### 1. CPU-only as a real design constraint

La historia principal del repo no es “entrenar un clasificador”, sino “hacerlo defendible en hardware común”. Esa restricción aparece en:

- relevamiento de hardware;
- tamaño de muestra guiado por RAM;
- batch size conservador;
- contingencia explícita para el Transformer.

### 2. Fair comparison between model families

El equipo intentó que la comparación entre SVM y Transformer no se apoye en pipelines incompatibles. Eso explica la aparición de columnas canónicas de texto limpio, métricas comparables y análisis por clase.

### 3. Documentation became part of the deliverable

La documentación no llegó al final como agregado superficial. Hay una secuencia clara:

- primero contexto y reglas;
- después módulos reutilizables;
- luego notebooks;
- finalmente README, contingencias y presentación.

Eso es consistente con un trabajo final que necesita ser mostrado, no solo ejecutado.

## Turning Points

### April 19, 2026: scaffold to system

El commit `feat: add cpu-only nlp pipeline modules` es el punto donde el repositorio deja de ser carpeta de trabajo y pasa a ser sistema. Desde ahí ya existen hardware helpers, corpus, limpieza, evaluación, artefactos y API.

### April 22-24, 2026: methodological hardening

Entre los commits de Federico y Juan aparecen los cambios más académicamente sensibles:

- balanceo de entrenamiento;
- redefinición de train/test;
- control de leakage;
- métricas ampliadas;
- notas de contingencia del Transformer.

Ese tramo es el corazón técnico del trabajo del equipo.

### April 25, 2026: delivery layer

El cierre con `src/static/presentacion.*` y `src/api_local.py` convierte el proyecto en una demo navegable. Ese paso no mejora el modelo, pero sí mejora mucho la defensa del entregable.

## Where the Repo Stands Now

El estado actual es sólido como entrega académica, pero mixto como repositorio técnico. Lo mejor está en:

- la separación entre código reusable y notebooks;
- la conciencia explícita sobre restricciones de hardware;
- la capacidad de mostrar una demo local.

La deuda aparece en:

- residuos de edición versionados;
- scripts de “test” que no son tests automatizados;
- documentos de análisis que habían quedado viejos;
- validaciones parciales del flujo Transformer.

## Bottom Line

La historia de este repo es la de un equipo pequeño que logró pasar de consigna a demo funcional en menos de una semana. Federico empujó la arquitectura y la narrativa general; Juan aportó ajustes metodológicos de alto impacto. El resultado no está desordenado por falta de trabajo: está desordenado por velocidad de cierre. Esa diferencia importa, porque la base técnica existe, pero necesita un último barrido de higiene para que el repositorio esté a la altura del entregable.
