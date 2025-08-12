def convert_unit(valor: float, from_unit: str, to_unit: str) -> float:
    # TODO: Implementar conversión unidad energía (kcal/MJ)
    return valor

def check_range(valor: float, vmin: float, vmax: float) -> bool:
    return vmin <= valor <= vmax

def convert_asfed_ms(valor: float, ms: float, from_base: str, to_base: str) -> float:
    """Convierte entre base MS y as-fed dado el %MS."""
    if from_base == to_base:
        return valor
    if from_base == "MS" and to_base == "as-fed":
        return valor * (ms/1000)
    elif from_base == "as-fed" and to_base == "MS":
        return valor * (1000/ms)
    else:
        return valor

def show_cheatsheet(familia:str):
    # TODO: Mostrar variables mínimas sugeridas por familia
    if familia.lower().startswith("cereal"):
        st.info("Variables mínimas recomendadas: CP, EE, CF, Ash, Starch/NFE")
    elif familia.lower().startswith("oleaginosas"):
        st.info("Variables mínimas: CP, EE, CF, Ash, antinutrientes si aplica")
    # ...
