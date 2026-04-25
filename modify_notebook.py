import nbformat
import sys

nb_path = "notebooks/02_fase_4_transformer_cpu.ipynb"
with open(nb_path, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

for i, cell in enumerate(nb.cells):
    if cell.cell_type == "code" and "entrenar_transformer_en_cpu" in cell.source:
        print(f"Cell {i} has training code. Source:")
        print("---")
        print(cell.source)
        print("---")
