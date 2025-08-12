import pandas as pd
from typing import Dict, Any

def load_ingredients_map(path:str) -> pd.DataFrame:
    """Carga el mapa de ingredientes a familias."""
    return pd.read_csv(path)

def get_ingredient_defaults(nombre:str, familia:str, especie:str) -> Dict[str,Any]:
    """Devuelve composición default para el ingrediente (stub, puedes adaptar)."""
    # TODO: Leer de archivo data/ingredients_defaults.csv o similar.
    return {
        "DM": 880,
        "Ash": 50,
        "CP": 140,
        "EE": 40,
        "CF": 50,
        "NDF": 100,
        "ADF": 40,
        "Starch": 600,
        "Sugars": 40,
        "GE": 4000,
        "unidad": "g/kg MS"
    }

class IngredientInput:
    """Validador de entradas de ingrediente (puedes expandir con pydantic)."""
    # TODO: Implementar validaciones reales.
    def __init__(self, comp:Dict[str,Any]):
        self.data = comp
        # checks here
