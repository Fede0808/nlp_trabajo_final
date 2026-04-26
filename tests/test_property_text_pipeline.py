from __future__ import annotations

import pandas as pd

from src.property_text_pipeline import (
    COLUMNA_TEXTO_LIMPIO,
    COLUMNA_TEXTO_LIMPIO_CENSURADO,
    COLUMNA_TEXTO_LIMPIO_TRANSFORMER,
    COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO,
    agregar_columna_texto_limpio,
    limpiar_texto,
)


def test_limpiar_texto_normaliza_y_conserva_tokens_utiles() -> None:
    texto = "Departamento 3 amb. con balcón y 45 m2 _x000d_"

    resultado = limpiar_texto(texto)

    assert "departamento" in resultado
    assert "balcon" in resultado
    assert "45_m2" in resultado
    assert "_x000d_" not in resultado


def test_agregar_columna_texto_limpio_genera_columnas_canonicas() -> None:
    df = pd.DataFrame(
        {
            "description": [
                "Casa con patio y 2 dorm.",
                "PH al frente con entrada independiente.",
            ],
            "property_type": ["Casa", "PH"],
        }
    )

    resultado = agregar_columna_texto_limpio(df)

    for columna in (
        COLUMNA_TEXTO_LIMPIO,
        COLUMNA_TEXTO_LIMPIO_TRANSFORMER,
        COLUMNA_TEXTO_LIMPIO_CENSURADO,
        COLUMNA_TEXTO_LIMPIO_TRANSFORMER_CENSURADO,
    ):
        assert columna in resultado.columns
        assert resultado[columna].isna().sum() == 0

    assert "casa" not in resultado.loc[0, COLUMNA_TEXTO_LIMPIO_CENSURADO]
    assert "entrada independiente" in resultado.loc[1, COLUMNA_TEXTO_LIMPIO_TRANSFORMER]
