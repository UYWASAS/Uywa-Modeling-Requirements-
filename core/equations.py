import numpy as np
from typing import Optional, Literal, Dict, Any

# =========================
# BLOQUE 1: Helpers conversión base
# =========================

def asfed_to_dm(value_asfed: float, DM_pct: float, decimals: int = 0) -> float:
    """
    Convierte un valor en base as-fed a base materia seca (MS).
    value_asfed: valor en as-fed (kcal/kg as-fed)
    DM_pct: % materia seca (0–100)
    return: valor en base MS (kcal/kg MS)
    """
    if DM_pct is None or DM_pct <= 0 or DM_pct > 100:
        raise ValueError("DM_pct debe estar entre 0 y 100")
    result = value_asfed * 100 / DM_pct
    return round(result, decimals)

def dm_to_asfed(value_dm: float, DM_pct: float, decimals: int = 0) -> float:
    """
    Convierte un valor en base MS a as-fed.
    value_dm: valor en base MS (kcal/kg MS)
    DM_pct: % materia seca (0–100)
    return: valor en base as-fed (kcal/kg as-fed)
    """
    if DM_pct is None or DM_pct <= 0 or DM_pct > 100:
        raise ValueError("DM_pct debe estar entre 0 y 100")
    result = value_dm * DM_pct / 100
    return round(result, decimals)

# ============================================================
# BLOQUE 2: AVES — MEn (kcal/kg MS)
# ============================================================

# Las fórmulas NRC esperan insumos en % (g/100g MS). 
# Por lo tanto, aquí se divide cada insumo recibido (en g/kg MS) por 10.

def men_corn(CP, EE, NFE, decimals=0) -> float:
    """NRC. MEn (maíz): 36.21·CP + 85.44·EE + 37.26·NFE -- todos en %"""
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 36.21*(CP/10) + 85.44*(EE/10) + 37.26*(NFE/10)
    return round(men, decimals)

def men_sorghum_low_tannin(CP, EE, NFE, decimals=0) -> float:
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 31.02*(CP/10) + 77.03*(EE/10) + 37.67*(NFE/10)
    return round(men, decimals)

def men_sorghum_high_tannin(CP, EE, NFE, decimals=0) -> float:
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 21.98*(CP/10) + 54.75*(EE/10) + 35.18*(NFE/10)
    return round(men, decimals)

def men_wheat(CP, EE, NFE, decimals=0) -> float:
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 34.92*(CP/10) + 63.10*(EE/10) + 36.42*(NFE/10)
    return round(men, decimals)

def men_triticale(CP, EE, NFE, decimals=0) -> float:
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 34.49*(CP/10) + 62.16*(EE/10) + 35.61*(NFE/10)
    return round(men, decimals)

def men_barley(CF, Starch, decimals=0) -> float:
    if CF is None or Starch is None:
        raise ValueError("Se requieren CF y Starch en g/kg MS.")
    men = 3078 - 90.4*(CF/10) + 9.2*(Starch/10)
    return round(men, decimals)

def men_oats(CF, EE, decimals=0) -> float:
    if CF is None or EE is None:
        raise ValueError("Se requieren CF y EE en g/kg MS.")
    men = 2970 - 59.7*(CF/10) + 116.9*(EE/10)
    return round(men, decimals)

def men_rice_bran(DM_pct, Ash, CP, EE, CF, decimals=0) -> float:
    for v in [DM_pct, Ash, CP, EE, CF]:
        if v is None:
            raise ValueError("Se requieren DM_pct (%), Ash, CP, EE, CF en g/kg MS.")
    men = 46.7*DM_pct - 46.7*(Ash/10) - 69.55*(CP/10) + 42.95*(EE/10) - 81.95*(CF/10)
    return round(men, decimals)

def men_bakery_generic(CP, EE, NFE, decimals=0) -> float:
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 34.49*(CP/10) + 76.10*(EE/10) + 37.67*(NFE/10)
    return round(men, decimals)

def tmen_bakery_alt(CF, Ash, CP, EE, decimals=0) -> float:
    for v in [CF, Ash, CP, EE]:
        if v is None:
            raise ValueError("Se requieren CF, Ash, CP y EE en g/kg MS.")
    tmen = 4340 - 100*(CF/10) - 40*(Ash/10) - 30*(CP/10) + 10*(EE/10)
    return round(tmen, decimals)

def men_wheat_bran(DM_pct, Ash, CF, decimals=0) -> float:
    for v in [DM_pct, Ash, CF]:
        if v is None:
            raise ValueError("Se requieren DM_pct (%), Ash y CF en g/kg MS.")
    men = 40.1*DM_pct - 40.1*(Ash/10) - 165.39*(CF/10)
    return round(men, decimals)

def men_wheat_flour(CF, decimals=0) -> float:
    if CF is None:
        raise ValueError("Se requiere CF en g/kg MS.")
    men = 3985 - 205*(CF/10)
    return round(men, decimals)

def men_wheat_flour_pelleted(CF, decimals=0) -> float:
    if CF is None:
        raise ValueError("Se requiere CF en g/kg MS.")
    men = 3926 - 181*(CF/10)
    return round(men, decimals)

# ... (las demás funciones de AVES que correspondan NRC: dividir insumos en g/kg por 10 si esperan %)

# ============================================================
# BLOQUE 3: CERDOS — ME y NE (kcal/kg MS)
# ============================================================

def me_from_de_and_cp(DE, CP, decimals=0) -> float:
    if DE is None or CP is None:
        raise ValueError("Se requieren DE (kcal/kg) y CP (g/kg MS).")
    me = (1.00*DE) - 0.68*CP
    return round(me, decimals)

def me_noblet_perez(Ash, CP, EE, NDF, decimals=0) -> float:
    for v in [Ash, CP, EE, NDF]:
        if v is None:
            raise ValueError("Se requieren Ash, CP, EE y NDF en g/kg MS.")
    me = 4194 - 9.2*Ash + 1.0*CP + 4.1*EE - 3.5*NDF
    return round(me, decimals)

def ne_from_me_and_comp(ME, EE, Starch, CP, ADF, decimals=0) -> float:
    for v in [ME, EE, Starch, CP, ADF]:
        if v is None:
            raise ValueError("Se requieren ME (kcal/kg MS), EE, Starch, CP, ADF (g/kg MS).")
    ne = 0.726*ME + 1.33*EE + 0.39*Starch - 0.62*CP - 0.83*ADF
    return round(ne, decimals)

def ne_from_de_and_comp(DE, EE, Starch, CP, ADF, decimals=0) -> float:
    for v in [DE, EE, Starch, CP, ADF]:
        if v is None:
            raise ValueError("Se requieren DE (kcal/kg MS), EE, Starch, CP, ADF (g/kg MS).")
    ne = 0.700*DE + 1.61*EE + 0.48*Starch - 0.91*CP - 0.87*ADF
    return round(ne, decimals)

def ne_from_digestibles(DCP, DEE, Starch, DRES, DOM=None, DADF=None, decimals=0) -> float:
    if DRES is None:
        if DOM is not None and DCP is not None and DEE is not None and Starch is not None and DADF is not None:
            DRES = DOM - (DCP + DEE + Starch + DADF)
        else:
            raise ValueError("Debe proveer DRES o DOM, DCP, DEE, Starch, DADF (g/kg MS).")
    for v in [DCP, DEE, Starch, DRES]:
        if v is None:
            raise ValueError("Se requieren DCP, DEE, Starch, DRES en g/kg MS.")
    ne = 2.73*DCP + 8.37*DEE + 3.44*Starch + 2.89*DRES
    return round(ne, decimals)

def ne_from_functional_digestibles(DCP, DEEh, Starcham, Suge, FCH, decimals=0) -> float:
    for v in [DCP, DEEh, Starcham, Suge, FCH]:
        if v is None:
            raise ValueError("Se requieren DCP, DEEh, Starcham, Suge y FCH en g/kg MS.")
    ne = 2.80*DCP + 8.54*DEEh + 3.38*Starcham + 3.05*Suge + 2.33*FCH
    return round(ne, decimals)

# ============================================================
# BLOQUE 4: Wrapper universal compute_energy
# ============================================================

def compute_energy(
    species: Literal["poultry", "swine"],
    family: str,
    method: Optional[str],
    inputs: Dict[str, Any],
    return_asfed: bool = False,
    DM_pct: Optional[float] = None,
    decimals: int = 0
    ) -> Dict[str, Any]:
    """
    Wrapper universal. Devuelve dict:
      {'value': float, 'basis': 'DM'|'as-fed', 'equation': str, 'notes': list[str]}
    Internamente usa la función y método adecuado.
    """
    notes = []
    if species == "poultry":
        # Ejemplo para maíz NRC
        if family.lower() == "cereales y subproductos" and (method is None or method == "men_corn"):
            for v in ["CP", "EE", "NFE"]:
                if v not in inputs:
                    raise ValueError(f"Falta la variable {v} (g/kg MS) para maíz NRC.")
            val = men_corn(inputs["CP"], inputs["EE"], inputs["NFE"], decimals=decimals)
            equation = "men_corn"
        elif method == "men_barley":
            for v in ["CF", "Starch"]:
                if v not in inputs:
                    raise ValueError(f"Falta la variable {v} (g/kg MS) para cebada NRC.")
            val = men_barley(inputs["CF"], inputs["Starch"], decimals=decimals)
            equation = "men_barley"
        # ...agrega más elif para más métodos soportados...
        else:
            raise ValueError("La familia/método no está soportada aún.")
    elif species == "swine":
        if method == "me_noblet_perez" or (method is None and all(x in inputs for x in ["Ash", "CP", "EE", "NDF"])):
            val = me_noblet_perez(inputs["Ash"], inputs["CP"], inputs["EE"], inputs["NDF"], decimals=decimals)
            equation = "me_noblet_perez"
        elif method == "me_from_de_and_cp" or (method is None and all(x in inputs for x in ["DE", "CP"])):
            val = me_from_de_and_cp(inputs["DE"], inputs["CP"], decimals=decimals)
            equation = "me_from_de_and_cp"
        # ...agrega más elif para más métodos soportados...
        else:
            raise ValueError("No hay método adecuado ni suficientes variables para cerdos.")
    else:
        raise ValueError("Especie no soportada.")

    # conversión as-fed
    value_out = val
    basis = "DM"
    if return_asfed:
        if DM_pct is None:
            raise ValueError("Se requiere DM_pct para conversión as-fed.")
        value_out = dm_to_asfed(val, DM_pct, decimals=decimals)
        basis = "as-fed"
    return dict(
        value=value_out,
        basis=basis,
        equation=equation,
        notes=notes
    )

# =========================
# FIN DE ARCHIVO
# =========================
