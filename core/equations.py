import numpy as np
from typing import Dict, Any, Optional, Literal

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
# BLOQUE: Wrapper SOLO CERDOS
# ============================================================

def compute_energy(
    species: Literal["swine"],
    family: str,
    method: Optional[str],
    inputs: Dict[str, Any],
    return_asfed: bool = False,
    DM_pct: Optional[float] = None,
    decimals: int = 0
    ) -> Dict[str, Any]:
    """
    Wrapper SOLO CERDOS. Devuelve dict:
      {'value': float, 'basis': 'DM'|'as-fed', 'equation': str, 'notes': list[str]}
    Internamente usa la función y método adecuado.
    """
    notes = []
    if species == "swine":
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
        raise ValueError("Solo se soporta la especie 'swine' (cerdos).")

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
