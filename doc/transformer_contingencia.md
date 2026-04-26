# Estado del transformer CPU-only

## Estado actual

El proyecto usa `distilbert-base-multilingual-cased` como modelo profundo compatible con CPU. El codigo ya diferencia entre:

- snapshots locales integrados en `artifacts/`;
- disponibilidad del tokenizador y de los pesos (`model.safetensors`);
- cache local de Hugging Face como fallback tecnico, pero no como ruta principal del cierre.

## Regla de decision

- Si existe snapshot completo en `artifacts/`: la Fase 4 puede ejecutarse y compararse contra los modelos clasicos sin depender de rutas personales.
- Si faltan archivos del snapshot: la Fase 4 queda bloqueada para el cierre academico offline estricto.
- La comparacion final del trabajo no depende de entrenamiento nuevo en esta maquina; depende de evaluar localmente los snapshots ya integrados.

## Politica de tokenizador

- Los notebooks de cierre y la documentacion operan en `modo_offline=True`.
- En ese modo, la carga del tokenizador debe fallar de forma explicita si no existe snapshot local ni artefacto del proyecto.
- El modulo reusable conserva `modo_offline=False` como opcion explicita para permitir resolucion remota fuera del cierre academico.

## Parametros congelados para Fase 4

- Modelo: `distilbert-base-multilingual-cased`
- `max_length=128`
- `batch_size=4`
- `epochs=1`
- Cuantizacion dinamica para inferencia CPU

## Criterio academico de cierre

La entrega sigue siendo defendible si:

- la evaluacion del transformer corre integramente en esta CPU desde snapshots locales integrados;
- la mini-API local funciona con el mejor modelo censurado del benchmark final;
- la comparacion final identifica que el enfoque profundo estaba preparado para el mismo split, mismas clases y columnas canonicas del proyecto (`texto_limpio` para SVM y `texto_limpio_transformer` para el enfoque profundo);
- el escenario censurado se presenta como control metodologico del data leakage y no como garantia automatica de mejora empirica.

## Regla de comunicacion final

Para el cierre del repositorio, el mensaje tecnico debe ser consistente:

- el modelo operativo de la API es `Reg Log` censurado porque es el mejor modelo dentro del subconjunto censurado (`accuracy=0.8515`, `f1_macro=0.7483`);
- DistilBERT queda como enfoque profundo reproducible bajo presupuesto CPU restringido y alcanza el mejor `F1 macro` global entre los modelos base (`0.8292`);
- la comparacion final concluye explicitamente que la censura no mejoro las metricas respecto de los modelos base en esta corrida local del 26 de abril de 2026;
- la contingencia solo invalida la comparacion final si faltan snapshots locales o si la evaluacion no puede correrse en modo offline estricto.
