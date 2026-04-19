# Shortlist de skills externas bajo auditoria

## Politica actual

- No instalar skills externas de gestion del proyecto sin auditoria manual previa.
- `planning-with-files` queda descartada por no cumplir la barra de seguridad requerida.
- Hasta nuevo aviso, la gestion del proyecto se sostiene con tooling nativo del entorno.

## Candidatas en revision

### `addyosmani/agent-skills@planning-and-task-breakdown`

- Estado: pendiente de auditoria
- Uso potencial: descomponer trabajo en tareas concretas
- Motivo para shortlist: mejor senal relativa que otras skills de planning general
- Bloqueo actual: falta revisar origen real, contenido y side effects

### `deanpeters/product-manager-skills@roadmap-planning`

- Estado: pendiente de auditoria
- Uso potencial: roadmap tecnico y orden de hitos
- Motivo para shortlist: puede servir para milestone planning del TIF
- Bloqueo actual: falta revisar origen real, contenido y side effects

## Criterio de auditoria previa

Antes de aprobar una skill externa, verificar:

1. repositorio fuente real y responsable del paquete
2. contenido de `SKILL.md`
3. presencia de scripts, comandos o binarios asociados
4. permisos y side effects posibles
5. dependencia de red, instaladores o tooling adicional no controlado
6. alineacion con la politica del proyecto y con CPU-only

## Regla de decision

- Si la skill pasa la auditoria, se mueve a estado `aprobada`.
- Si la skill no pasa la auditoria, se mueve a estado `rechazada`.
- Si la evidencia no alcanza, la skill queda `pendiente` y no se instala.
