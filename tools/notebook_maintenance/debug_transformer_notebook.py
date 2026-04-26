import nbformat
with open("notebooks/02_fase_4_transformer_cpu.ipynb", "r") as f:
    nb = nbformat.read(f, as_version=4)

for i, cell in enumerate(nb.cells):
    if "modelo_temp" in cell.source:
        print(f"Cell {i}:\n{cell.source}")
