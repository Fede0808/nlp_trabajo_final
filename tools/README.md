# Tools

Scripts auxiliares usados durante el cierre y mantenimiento del repositorio.

- `manual_checks/`: verificaciones manuales o exploratorias que no forman parte de la suite de `pytest`.
- `manual_checks/benchmark_final_cpu.py`: recalcula el benchmark final en CPU y regenera `artifacts/modelo_censurado_final.joblib`.
- `notebook_maintenance/`: utilitarios ad hoc para inspeccionar, dividir o parchear notebooks.
- `notebook_maintenance/sanitizar_notebooks_finales.py`: reemplaza rutas personales y alinea mensajes de cierre en notebooks.
- `metricas_estaticas/`: apoyo para cargar o revisar métricas congeladas sin reentrenar modelos.

Estos archivos no forman parte del flujo principal documentado en `README.md` y se preservan solo como soporte técnico de mantenimiento.
