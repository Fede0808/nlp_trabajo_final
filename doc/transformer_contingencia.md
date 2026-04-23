# Contingencia del transformer CPU-only

## Estado actual

El proyecto usa `distilbert-base-multilingual-cased` como modelo profundo compatible con CPU. El codigo ya diferencia entre:

- disponibilidad del tokenizador en cache local;
- disponibilidad real de pesos del modelo (`model.safetensors` o `pytorch_model.bin`);
- imposibilidad de completar la fase offline cuando faltan esos pesos.

## Regla de decision

- Si hay tokenizador y pesos locales: la Fase 4 puede ejecutarse y compararse contra la baseline.
- Si hay tokenizador pero no pesos: la Fase 4 queda formalmente bloqueada; se mantiene el flujo preparado y la comparacion final debe declararse condicionada.
- Si no hay cache local: el proyecto conserva el pipeline y la configuracion final, pero no debe prometer entrenamiento reproducible offline hasta cargar el snapshot.

## Parametros congelados para Fase 4

- Modelo: `distilbert-base-multilingual-cased`
- `max_length=128`
- `batch_size=4`
- `epochs=1`
- Cuantizacion dinamica para inferencia CPU

## Criterio academico de cierre

La entrega sigue siendo defendible si:

- el baseline SVM esta completamente cerrado;
- la mini-API local funciona con el artefacto final del baseline;
- el bloqueo del transformer se documenta explicitamente como restriccion de disponibilidad local de pesos y no como falta de implementacion;
- la comparacion final identifica que el enfoque profundo estaba preparado para el mismo split, mismas clases y misma columna `texto_limpio`.
