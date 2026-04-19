# Contexto de consigna TIF (NLP)

## Objetivo general

Desarrollar un proyecto completo de NLP sobre un problema real, aplicando los contenidos del seminario de forma tecnica, reproducible y bien comunicada.

## Alcance minimo obligatorio

1. Formulacion del problema
- Definir un caso real (empresa, institucion u open data).
- Explicar objetivo y relevancia.

2. Construccion y analisis del corpus
- Describir fuentes y caracteristicas de datos.
- Documentar preprocesamiento de forma replicable.

3. Modelado (minimo 2 enfoques distintos)
- Incluir al menos un enfoque clasico (ejemplo: TF-IDF + SVM).
- Incluir al menos un enfoque profundo (ejemplo: LSTM o Transformer).

4. Comparacion de enfoques
- Reportar metricas y validacion cruzada.
- Discutir resultados tecnicamente.
- Incluir interpretacion linguistica del desempeno.

5. Implementacion
- Entregar mini-API para consultar el modelo, generar predicciones o correr un LLM local.
- Opcional: dashboard o demo web.

## Criterios de evaluacion (a maximizar)

- Profundidad tecnica.
- Rigor en preprocesamiento del lenguaje.
- Justificacion metodologica.
- Calidad comunicacional.
- Reproducibilidad.
- Etica y responsabilidad en el uso del lenguaje.

## Checklist de cumplimiento rapido

- [ ] Problema real definido y bien justificado.
- [ ] Dataset trazable (fuentes, versionado, supuestos).
- [ ] Pipeline de preprocesamiento reproducible (scripts y parametros).
- [ ] Dos modelos implementados (clasico + profundo).
- [ ] Comparacion con metricas consistentes y validacion cruzada.
- [ ] Analisis linguistico de errores/desempeno.
- [ ] Mini-API funcionando localmente.
- [ ] Resultados y decisiones tecnicas bien comunicadas.
- [ ] Consideraciones eticas explicitas.

## Implicancias para este repositorio

- `src/`: pipeline de datos, entrenamiento, evaluacion y servicio API.
- `notebooks/`: EDA, experimentos y analisis comparativo.
- `doc/`: consigna original y documentacion de decisiones.
- `pyproject.toml`: entorno reproducible con `uv`.

## Riesgos frecuentes a evitar

- Quedarse en un unico modelo (incumple consigna).
- Preprocesamiento no replicable o no documentado.
- Comparaciones injustas por metricas/configuraciones distintas.
- Falta de interpretacion linguistica (solo numeros).
- API incompleta o no ejecutable en local.

