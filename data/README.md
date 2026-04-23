# Datos locales (no versionados)

Esta carpeta contiene los datasets usados para entrenar, validar y defender academicamente el proyecto.

## Archivos esperados

- `entrenamiento.csv`: dataset principal para entrenamiento y evaluacion interna del baseline y del transformer.
- `venta_descripcion.csv`: dataset de validacion externa o contraste cualitativo.

## Columnas criticas

- `description`: texto base de cada aviso inmobiliario.
- `property_type`: etiqueta objetivo del clasificador.

## Clases del problema

- `Departamento`
- `Casa`
- `PH`

El pipeline filtra explicitamente esas tres clases y prioriza conservar representacion suficiente de `PH` mediante muestreo estratificado.

## Reproducibilidad

- El proyecto usa `semilla=42`, `test_size=0.2` y una muestra objetivo de `10000` registros cuando la memoria disponible lo permite.
- La columna canonica de modelado es `texto_limpio`.
- Si clonas el repo en otra maquina, copia los CSV a `data/` antes de ejecutar notebooks o scripts.

## Politica de versionado

- Todo `data/*` esta ignorado en `.gitignore` y no se sube al repositorio.
- La trazabilidad del corpus se documenta en `README.md` y `doc/project_phase_plan.md` para que el informe pueda explicarlo sin exponer los CSV.
