import pandas as pd

def load_ingredients_map(path:str) -> pd.DataFrame:
    # Retorna un DataFrame vacío si no existe el archivo, para evitar errores al arrancar la app.
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame({"ingrediente":[], "familia":[]})

def get_ingredient_defaults(nombre:str, familia:str, especie:str) -> dict:
    # Retorna una composición de ejemplo genérica.
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
    """Stub para validación futura"""
    def __init__(self, comp):
        self.data = comp
