import nbformat

with open('notebooks/02_fase_4_transformer_cpu.ipynb', 'r') as f:
    nb = nbformat.read(f, as_version=4)

# We will modify the obtener_o_entrenar_distilbert to check if the global is actually a torch.nn.Module
for cell in nb.cells:
    if "def obtener_o_entrenar_distilbert" in cell.source:
        new_source = cell.source.replace(
            "if nombre_modelo_ram in globals() and nombre_tokenizador_ram in globals():",
            "if nombre_modelo_ram in globals() and isinstance(globals()[nombre_modelo_ram], torch.nn.Module) and nombre_tokenizador_ram in globals():"
        )
        cell.source = new_source
        
with open('notebooks/02_fase_4_transformer_cpu.ipynb', 'w') as f:
    nbformat.write(nb, f)
print("Notebook patched.")
