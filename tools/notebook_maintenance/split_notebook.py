import nbformat
import os
import sys

input_notebook = "notebooks/02_fase_4_transformer_cpu.ipynb"
output_notebook_1 = "notebooks/02_fase_4_transformer_cpu.ipynb"
output_notebook_2 = "notebooks/03_fase_5_comparacion_y_explicabilidad.ipynb"

try:
    with open(input_notebook, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
except Exception as e:
    print(f"Error reading notebook: {e}")
    sys.exit(1)

split_index = -1
for i, cell in enumerate(nb.cells):
    if cell.cell_type == "markdown" and "Comparacion final entre enfoque clasico y profundo" in cell.source:
        split_index = i
        break

if split_index == -1:
    print("Could not find the split point.")
    sys.exit(1)

nb1_cells = nb.cells[:split_index]
nb2_cells = nb.cells[split_index:]

# For notebook 2, we should probably add some basic imports if it's going to be a separate notebook
# Or we just split it as requested. I'll just split it as requested.

nb1 = nbformat.v4.new_notebook(cells=nb1_cells, metadata=nb.metadata)
nb2 = nbformat.v4.new_notebook(cells=nb2_cells, metadata=nb.metadata)

try:
    with open(output_notebook_1, "w", encoding="utf-8") as f:
        nbformat.write(nb1, f)
    with open(output_notebook_2, "w", encoding="utf-8") as f:
        nbformat.write(nb2, f)
    print("Notebook split successfully.")
except Exception as e:
    print(f"Error writing notebooks: {e}")
    sys.exit(1)
