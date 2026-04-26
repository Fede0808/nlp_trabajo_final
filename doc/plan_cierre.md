# Plan de Cierre del Trabajo Final

## Objetivo

Cerrar el repositorio con evidencia academica defendible, sin reabrir entrenamiento del transformer ni introducir exploracion nueva. El foco es que el estado final quede consistente entre notebooks, API local y documentacion de limites.

## Criterio de cierre

El trabajo se considera cerrado cuando se cumplan estas condiciones:

- los modelos base y censurados quedan evaluados localmente en CPU bajo el mismo split;
- la mini-API local puede consultarse contra el mejor modelo censurado del benchmark final;
- el enfoque profundo con DistilBERT queda mostrado como ejecutado en CPU-only bajo parametros congelados;
- la comparacion clasico vs profundo queda explicita en los notebooks y no dispersa en salidas aisladas;
- los limites metodologicos, sesgos y contingencias quedan declarados por escrito.

## Checklist operativo

### Notebook 01 - corpus y baseline clasico

- [x] agregar trazabilidad del dataset: archivo fuente, columnas usadas, clases objetivo, supuestos y limites;
- [x] mantener la limpieza reproducible y la validacion cruzada del SVM;
- [x] guardar el artefacto final del baseline en `artifacts/modelo_svm.joblib`;
- [x] documentar el uso minimo de la mini-API local con `uvicorn`, `GET /salud`, `GET /benchmark` y `POST /predecir`;
- [x] incorporar un bloque corto de etica y sesgos: ambiguedad semantica, leakage, desbalance y limites de generalizacion.

### Notebook 02 - transformer CPU-only

- [x] mantener `distilbert-base-multilingual-cased` como enfoque profundo congelado;
- [x] documentar que el `LOAD REPORT` con `UNEXPECTED` y `MISSING` es esperable en fine-tuning;
- [x] dejar explicito el setup restringido: `max_length=128`, `batch_size=4`, `epochs=1`, CPU-only y cuantizacion dinamica para inferencia;
- [x] cerrar con comparacion narrativa y tabular contra los modelos clasicos usando la corrida local consolidada;
- [x] presentar el escenario censurado como analisis metodologico del leakage, explicando que en esta corrida no mejora las metricas.

### Documentacion de cierre

- [x] consolidar en `doc/transformer_contingencia.md` el criterio academico de cierre del enfoque profundo;
- [x] alinear este archivo con una lista de tareas ejecutables y criterio de aceptacion;
- [x] revisar consistencia final entre ambos notebooks y la documentacion.

## Validacion final

Antes de considerar cerrada la entrega, verificar:

- que ambos notebooks abran sin romper su JSON;
- que las metricas citadas en las conclusiones coincidan con la corrida local consolidada del 26 de abril de 2026;
- que la explicacion del `LOAD REPORT` no lo describa como bug;
- que la referencia a la mini-API sea ejecutable localmente con `artifacts/modelo_censurado_final.joblib`;
- que ningun bloque de conclusiones prometa que la censura mejoro el rendimiento si la evidencia local no lo sostiene.

## Estado esperado del repositorio

Al finalizar, el repositorio debe dejar un mensaje tecnico coherente:

- `Notebook 01` muestra corpus, limpieza, baseline, leakage, API local y limites;
- `Notebook 02` muestra enfoque profundo con snapshots locales y comparacion final;
- la API local queda asociada al mejor modelo censurado realmente medido en CPU;
- la documentacion explica que el guardrail de censura sirve como control metodologico aunque no mejore las metricas en esta corrida.
