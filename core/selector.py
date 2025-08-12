from typing import List, Dict, Any

def list_applicable_equations(especie:str, familia:str, comp_df) -> List[str]:
    """Devuelve lista de ecuaciones disponibles para especie/familia según las variables presentes."""
    # TODO: Implementar lógica real
    return ["Ecuación A (CP, EE, NFE)", "Ecuación B (CP, EE, Ash, Starch)", "Ecuación C (genérica, menos precisa)"]

def select_equation(especie:str, familia:str, comp_df) -> str:
    """Devuelve el nombre de la mejor ecuación aplicable (stub)."""
    # TODO: Implementar árbol de decisión real
    return "Ecuación A (CP, EE, NFE)"
