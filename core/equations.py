import numpy as np
from typing import Optional, Literal, Dict, Any

# ------------------------
# Helpers: conversión base
# ------------------------

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
# 1) AVES — MEn (kcal/kg MS)
# ============================================================

# ----- 1.1 Cereales y subproductos -----

def men_corn(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. MEn (maíz) = 36.21·CP + 85.44·EE + 37.26·NFE
    Entradas: CP, EE, NFE (g/kg MS)
    Salida: kcal/kg MS
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 36.21*CP + 85.44*EE + 37.26*NFE
    return round(men, decimals)

def men_sorghum_low_tannin(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Sorgo taninos <0.4%: MEn = 31.02·CP + 77.03·EE + 37.67·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 31.02*CP + 77.03*EE + 37.67*NFE
    return round(men, decimals)

def men_sorghum_high_tannin(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Sorgo taninos >1.0%: MEn = 21.98·CP + 54.75·EE + 35.18·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 21.98*CP + 54.75*EE + 35.18*NFE
    return round(men, decimals)

def men_wheat(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Trigo: MEn = 34.92·CP + 63.10·EE + 36.42·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 34.92*CP + 63.10*EE + 36.42*NFE
    return round(men, decimals)

def men_triticale(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Triticale: MEn = 34.49·CP + 62.16·EE + 35.61·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 34.49*CP + 62.16*EE + 35.61*NFE
    return round(men, decimals)

def men_barley(CF, Starch, decimals=0) -> float:
    """
    NRC. Cebada: MEn = 3078 – 90.4·CF + 9.2·Starch
    CF y Starch en g/kg MS
    """
    if CF is None or Starch is None:
        raise ValueError("Se requieren CF y Starch en g/kg MS.")
    men = 3078 - 90.4*CF + 9.2*Starch
    return round(men, decimals)

def men_oats(CF, EE, decimals=0) -> float:
    """
    NRC. Avena: MEn = 2970 – 59.7·CF + 116.9·EE
    """
    if CF is None or EE is None:
        raise ValueError("Se requieren CF y EE en g/kg MS.")
    men = 2970 - 59.7*CF + 116.9*EE
    return round(men, decimals)

def men_rice_bran(DM_pct, Ash, CP, EE, CF, decimals=0) -> float:
    """
    NRC. Pulido/polvillo arroz: MEn = 46.7·DM – 46.7·Ash – 69.55·CP + 42.95·EE – 81.95·CF
    DM_pct en %, resto en g/kg MS
    """
    for v in [DM_pct, Ash, CP, EE, CF]:
        if v is None:
            raise ValueError("Se requieren DM_pct (%), Ash, CP, EE, CF en g/kg MS.")
    men = 46.7*DM_pct - 46.7*Ash - 69.55*CP + 42.95*EE - 81.95*CF
    return round(men, decimals)

def men_bakery_generic(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Subproducto panadero: MEn = 34.49·CP + 76.10·EE + 37.67·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 34.49*CP + 76.10*EE + 37.67*NFE
    return round(men, decimals)

def tmen_bakery_alt(CF, Ash, CP, EE, decimals=0) -> float:
    """
    NRC. TMEn alternativa: TMEn = 4340 – 100·CF – 40·Ash – 30·CP + 10·EE
    """
    for v in [CF, Ash, CP, EE]:
        if v is None:
            raise ValueError("Se requieren CF, Ash, CP y EE en g/kg MS.")
    tmen = 4340 - 100*CF - 40*Ash - 30*CP + 10*EE
    return round(tmen, decimals)

def men_wheat_bran(DM_pct, Ash, CF, decimals=0) -> float:
    """
    NRC. Afrecho: MEn = 40.1·DM – 40.1·Ash – 165.39·CF
    """
    for v in [DM_pct, Ash, CF]:
        if v is None:
            raise ValueError("Se requieren DM_pct (%), Ash y CF en g/kg MS.")
    men = 40.1*DM_pct - 40.1*Ash - 165.39*CF
    return round(men, decimals)

def men_wheat_flour(CF, decimals=0) -> float:
    """
    NRC. Harina de trigo: MEn = 3985 – 205·CF
    """
    if CF is None:
        raise ValueError("Se requiere CF en g/kg MS.")
    men = 3985 - 205*CF
    return round(men, decimals)

def men_wheat_flour_pelleted(CF, decimals=0) -> float:
    """
    NRC. Harina de trigo pellet: MEn = 3926 – 181·CF
    """
    if CF is None:
        raise ValueError("Se requiere CF en g/kg MS.")
    men = 3926 - 181*CF
    return round(men, decimals)

# ----- 1.2 Subproductos industriales -----

def men_corn_wet_milling(CP, CF, EE, decimals=0) -> float:
    """
    NRC. Maíz molienda húmeda: MEn = 4240 – 34.4·CP – 159.6·CF + 13.5·EE
    """
    for v in [CP, CF, EE]:
        if v is None:
            raise ValueError("Se requieren CP, CF y EE en g/kg MS.")
    men = 4240 - 34.4*CP - 159.6*CF + 13.5*EE
    return round(men, decimals)

def men_corn_gluten_meal_65(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Gluten meal 65% PB: MEn = 40.94·CP + 88.17·EE + 33.13·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 40.94*CP + 88.17*EE + 33.13*NFE
    return round(men, decimals)

def men_corn_gluten_meal_40(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Gluten meal 40% PB: MEn = 36.64·CP + 73.30·EE + 25.67·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 36.64*CP + 73.30*EE + 25.67*NFE
    return round(men, decimals)

def men_corn_gluten_feed(DM_pct, Ash, CP, EE, CF, decimals=0) -> float:
    """
    NRC. Gluten feed 20% PB: MEn = 42.35·DM – 42.35·Ash – 23.74·CP + 28.03·EE – 165.72·CF
    """
    for v in [DM_pct, Ash, CP, EE, CF]:
        if v is None:
            raise ValueError("Se requieren DM_pct (%), Ash, CP, EE y CF en g/kg MS.")
    men = 42.35*DM_pct - 42.35*Ash - 23.74*CP + 28.03*EE - 165.72*CF
    return round(men, decimals)

def men_ddgs_generic(DM_pct, Ash, CP, CF, decimals=0) -> float:
    """
    NRC. DDGS/cervecería: MEn = 39.15·DM – 39.15·Ash – 9.72·CP – 63.81·CF
    """
    for v in [DM_pct, Ash, CP, CF]:
        if v is None:
            raise ValueError("Se requieren DM_pct (%), Ash, CP y CF en g/kg MS.")
    men = 39.15*DM_pct - 39.15*Ash - 9.72*CP - 63.81*CF
    return round(men, decimals)

# ----- 1.3 Raíces/almidones -----

def men_sweet_potato(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Camote deshidratado: MEn = 8.62·CP + 50.12·EE + 37.67·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 8.62*CP + 50.12*EE + 37.67*NFE
    return round(men, decimals)

def men_cassava_formula1(DM_pct, Ash, CF, decimals=0) -> float:
    """
    NRC. Yuca/tapioca: MEn = 39.14·DM – 39.14·Ash – 82.78·CF
    """
    for v in [DM_pct, Ash, CF]:
        if v is None:
            raise ValueError("Se requieren DM_pct (%), Ash y CF en g/kg MS.")
    men = 39.14*DM_pct - 39.14*Ash - 82.78*CF
    return round(men, decimals)

def men_cassava_formula2(Ash, CF, decimals=0) -> float:
    """
    NRC. Yuca/tapioca: MEn = 4054 – 43.4·Ash – 103·CF
    """
    for v in [Ash, CF]:
        if v is None:
            raise ValueError("Se requieren Ash y CF en g/kg MS.")
    men = 4054 - 43.4*Ash - 103*CF
    return round(men, decimals)

# ----- 1.4 Oleaginosas y harinas proteicas -----

def men_cottonseed_meal(DM_pct, EE, CF, decimals=0) -> float:
    """
    NRC. Harina de algodón: MEn = 21.26·DM + 47.13·EE – 30.85·CF
    """
    for v in [DM_pct, EE, CF]:
        if v is None:
            raise ValueError("Se requieren DM_pct (%), EE y CF en g/kg MS.")
    men = 21.26*DM_pct + 47.13*EE - 30.85*CF
    return round(men, decimals)

def men_peanut_meal(DM_pct, EE, CF, decimals=0) -> float:
    """
    NRC. Harina de maní: MEn = 29.68·DM + 60.95·EE – 60.87·CF
    """
    for v in [DM_pct, EE, CF]:
        if v is None:
            raise ValueError("Se requieren DM_pct (%), EE y CF en g/kg MS.")
    men = 29.68*DM_pct + 60.95*EE - 60.87*CF
    return round(men, decimals)

def men_canola_high_glucosinolate(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Canola alto glucosinolate: MEn = 29.73·CP + 46.39·EE + 7.87·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 29.73*CP + 46.39*EE + 7.87*NFE
    return round(men, decimals)

def men_canola_double_zero(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Canola doble cero: MEn = 32.76·CP + 64.96·EE + 13.24·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 32.76*CP + 64.96*EE + 13.24*NFE
    return round(men, decimals)

def men_soybean_meal_expeller(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Soya expeller: MEn = 37.50·CP + 70.52·EE + 14.90·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 37.50*CP + 70.52*EE + 14.90*NFE
    return round(men, decimals)

# ----- 1.5 Origen animal -----

def men_skim_milk_powder(CP, EE, NFE, decimals=0) -> float:
    """
    NRC. Leche descremada polvo: MEn = 40.94·CP + 77.96·EE + 19.04·NFE
    """
    for v in [CP, EE, NFE]:
        if v is None:
            raise ValueError("Se requieren CP, EE y NFE en g/kg MS.")
    men = 40.94*CP + 77.96*EE + 19.04*NFE
    return round(men, decimals)

def men_blood_meal_spray(CP, EE, decimals=0) -> float:
    """
    NRC. Harina de sangre (spray): MEn = 34.49·CP + 64.96·EE
    """
    for v in [CP, EE]:
        if v is None:
            raise ValueError("Se requieren CP y EE en g/kg MS.")
    men = 34.49*CP + 64.96*EE
    return round(men, decimals)

def men_blood_meal_drum(CP, EE, decimals=0) -> float:
    """
    NRC. Harina de sangre (drum): MEn = 31.88·CP + 60.32·EE
    """
    for v in [CP, EE]:
        if v is None:
            raise ValueError("Se requieren CP y EE en g/kg MS.")
    men = 31.88*CP + 60.32*EE
    return round(men, decimals)

def men_feather_meal(CP, EE, decimals=0) -> float:
    """
    NRC. Harina de pluma (pepsina dig. ≥80%): MEn = 33.20·CP + 57.53·EE
    """
    for v in [CP, EE]:
        if v is None:
            raise ValueError("Se requieren CP y EE en g/kg MS.")
    men = 33.20*CP + 57.53*EE
    return round(men, decimals)

def men_poultry_by_product_meal(CP, EE, high_fat=False, decimals=0) -> float:
    """
    NRC. Harina subproductos aviares: 
    alta grasa: MEn = 31.02·CP + 78.87·EE; normal: MEn = 31.02·CP + 74.23·EE
    """
    if CP is None or EE is None:
        raise ValueError("Se requieren CP y EE en g/kg MS.")
    if high_fat:
        men = 31.02*CP + 78.87*EE
    else:
        men = 31.02*CP + 74.23*EE
    return round(men, decimals)

def men_meat_and_bone_meal(DM_pct, Ash, EE, decimals=0) -> float:
    """
    NRC. Harina de carne y hueso: MEn = 35.87·DM – 34.08·Ash + 42.09·EE
    """
    for v in [DM_pct, Ash, EE]:
        if v is None:
            raise ValueError("Se requieren DM_pct (%), Ash y EE en g/kg MS.")
    men = 35.87*DM_pct - 34.08*Ash + 42.09*EE
    return round(men, decimals)

# ----- 1.6 Grasas y aceites -----

def men_fat_by_IV_and_saturates(IV, C16_0, C18_0, decimals=0) -> float:
    """
    NRC. Grasas/aceites: MEn = 20041 – 23.0·IV – 319.1·C16:0 – 153.4·C18:0
    Entradas: IV, C16_0, C18_0 (IV en unidades, C16:0 y C18:0 en % de FA)
    Salida: kcal/kg MS
    """
    for v in [IV, C16_0, C18_0]:
        if v is None:
            raise ValueError("Se requieren IV, C16_0 y C18_0.")
    men = 20041 - 23.0*IV - 319.1*C16_0 - 153.4*C18_0
    return round(men, decimals)

def men_fat_by_US_ratio(US_ratio, decimals=0) -> float:
    """
    NRC. Grasas/aceites: MEn = 8227 – 10318·(−1.1685·US_ratio)
    US_ratio: insaturados/saturados
    Salida: kcal/kg MS
    """
    if US_ratio is None:
        raise ValueError("Se requiere US_ratio (insat/sat).")
    men = 8227 - 10318 * (-1.1685 * US_ratio)
    return round(men, decimals)

# TODO: Añadir más variantes si hay datos de oleico+linoleico.

# ============================================================
# 2) CERDOS — ME y NE (kcal/kg MS)
# ============================================================

def me_from_de_and_cp(DE, CP, decimals=0) -> float:
    """
    Puente DE → ME: me_from_de_cp(de_kcal_per_kg, CP) = (1.00*DE) - 0.68*CP
    DE en kcal/kg, CP en g/kg MS.
    """
    if DE is None or CP is None:
        raise ValueError("Se requieren DE (kcal/kg) y CP (g/kg MS).")
    me = (1.00*DE) - 0.68*CP
    return round(me, decimals)

def me_noblet_perez(Ash, CP, EE, NDF, decimals=0) -> float:
    """
    Noblet & Pérez. ME = 4194 − 9.2·Ash + 1.0·CP + 4.1·EE − 3.5·NDF
    Todos en g/kg MS
    """
    for v in [Ash, CP, EE, NDF]:
        if v is None:
            raise ValueError("Se requieren Ash, CP, EE y NDF en g/kg MS.")
    me = 4194 - 9.2*Ash + 1.0*CP + 4.1*EE - 3.5*NDF
    return round(me, decimals)

def ne_from_me_and_comp(ME, EE, Starch, CP, ADF, decimals=0) -> float:
    """
    Eq. 1-7. NE = 0.726·ME + 1.33·EE + 0.39·Starch − 0.62·CP − 0.83·ADF
    ME en kcal/kg MS; resto en g/kg MS.
    """
    for v in [ME, EE, Starch, CP, ADF]:
        if v is None:
            raise ValueError("Se requieren ME (kcal/kg MS), EE, Starch, CP, ADF (g/kg MS).")
    ne = 0.726*ME + 1.33*EE + 0.39*Starch - 0.62*CP - 0.83*ADF
    return round(ne, decimals)

def ne_from_de_and_comp(DE, EE, Starch, CP, ADF, decimals=0) -> float:
    """
    Eq. 1-8. NE = 0.700·DE + 1.61·EE + 0.48·Starch − 0.91·CP − 0.87·ADF
    """
    for v in [DE, EE, Starch, CP, ADF]:
        if v is None:
            raise ValueError("Se requieren DE (kcal/kg MS), EE, Starch, CP, ADF (g/kg MS).")
    ne = 0.700*DE + 1.61*EE + 0.48*Starch - 0.91*CP - 0.87*ADF
    return round(ne, decimals)

def ne_from_digestibles(DCP, DEE, Starch, DRES, DOM=None, DADF=None, decimals=0) -> float:
    """
    Eq. 1-9. NE = 2.73·DCP + 8.37·DEE + 3.44·Starch + 2.89·DRES
    DCP, DEE, Starch, DRES en g/kg MS
    Si DRES no se pasa, puede calcularse como DOM − (DCP + DEE + Starch + DADF)
    """
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
    """
    Eq. 1-10 (Blok, 2006). NE = 2.80·DCP + 8.54·DEEh + 3.38·Starcham + 3.05·Suge + 2.33·FCH
    Todos en g/kg MS.
    """
    for v in [DCP, DEEh, Starcham, Suge, FCH]:
        if v is None:
            raise ValueError("Se requieren DCP, DEEh, Starcham, Suge y FCH en g/kg MS.")
    ne = 2.80*DCP + 8.54*DEEh + 3.38*Starcham + 3.05*Suge + 2.33*FCH
    return round(ne, decimals)

# ============================================================
# Wrapper universal
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
    # Este árbol debe ser sincronizado con core/selector.py
    notes = []
    if species == "poultry":
        # Ejemplo para maíz:
        if family.lower() == "cereales y subproductos" and (method is None or method == "men_corn"):
            for v in ["CP", "EE", "NFE"]:
                if v not in inputs:
                    raise ValueError(f"Falta la variable {v} (g/kg MS) para maíz NRC.")
            val = men_corn(inputs["CP"], inputs["EE"], inputs["NFE"], decimals=decimals)
            equation = "men_corn"
        # Agrega aquí más familias y variantes
        else:
            raise ValueError("La familia/método no está soportada aún.")
    elif species == "swine":
        # ME desde composición
        if method == "me_noblet_perez" or (method is None and all(x in inputs for x in ["Ash", "CP", "EE", "NDF"])):
            val = me_noblet_perez(inputs["Ash"], inputs["CP"], inputs["EE"], inputs["NDF"], decimals=decimals)
            equation = "me_noblet_perez"
        elif method == "me_from_de_and_cp" or (method is None and all(x in inputs for x in ["DE", "CP"])):
            val = me_from_de_and_cp(inputs["DE"], inputs["CP"], decimals=decimals)
            equation = "me_from_de_and_cp"
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
