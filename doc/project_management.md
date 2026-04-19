# Project management seguro

## Objetivo

Establecer una forma de gestion del TIF que sea:

- segura respecto de herramientas externas
- persistente entre sesiones
- trazable para decisiones tecnicas y academicas
- compatible con el trabajo diario en Codex, VSCode y GitHub

## Principios de trabajo

- No instalar skills externas de gestion hasta pasar una auditoria manual.
- Usar como base solo herramientas ya presentes en la sesion:
  - `doc/consigna_context.md` como contexto academico persistente
  - Plan Mode para bajar cada hito a un plan ejecutable
  - `brainstorming` para definir specs cuando haya decisiones de diseno
  - plugin de GitHub para issues, PRs y seguimiento operativo si hace falta
- Registrar decisiones tecnicas clave antes de implementar cambios grandes.
- Mantener el proyecto alineado con la restriccion principal: ejecucion CPU-only.

## Artefactos fuente de verdad

- `doc/consigna_context.md`: requisitos obligatorios del TIF y riesgos frecuentes.
- `doc/project_phase_plan.md`: fases del proyecto, entregables y criterios de cierre.
- `doc/skill_audit_shortlist.md`: skills externas candidatas y estado de auditoria.
- `README.md`: vista rapida del proyecto y enlaces de entrada.

## Flujo de trabajo recomendado

1. Revisar `doc/consigna_context.md` antes de abrir una linea de trabajo nueva.
2. Traducir el siguiente hito a un plan concreto en Plan Mode.
3. Si el trabajo requiere decisiones de arquitectura o alcance, usar `brainstorming`.
4. Implementar solo despues de tener criterios de exito claros.
5. Actualizar la documentacion de gestion si cambia una decision importante.
6. Si el cambio necesita coordinacion externa, bajar el trabajo a GitHub.

## Trazabilidad de decisiones tecnicas

Registrar al menos estas decisiones cuando se confirmen:

- texto de entrada principal del modelo
- estrategia de muestreo y representatividad de `PH`
- limites de CPU, RAM, threads y batch size
- modelo clasico baseline y modelo transformer final
- metricas de comparacion y criterio principal de exito

## Checklist de cierre por sesion

- Queda claro el siguiente paso del proyecto.
- Las decisiones nuevas quedaron reflejadas en algun artefacto del repo.
- No se incorporaron herramientas externas no auditadas.
- Los riesgos o bloqueos quedaron visibles para la siguiente sesion.
