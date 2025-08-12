import pandas as pd

def scale_nutrients(req_df: pd.DataFrame, energia: float) -> pd.DataFrame:
    """
    Escala nutrientes proporcionalmente a la energía.
    Regla base: nutriente_obj_kg = nutriente_base_kg * (E_obj / E_base)
    Respeta flags de no escalables y mínimos/máximos.
    """
    req_df = req_df.copy()
    for idx, row in req_df.iterrows():
        base = row["valor_por_kg"]
        escalable = row.get("escalable", False)
        min_abs = row.get("min_absoluto", None)
        max_abs = row.get("max", None)
        ref_energia = row.get("referencia_AME_kcalkg", 3000)
        if escalable:
            nuevo = base * (energia / ref_energia)
            if pd.notnull(min_abs):
                nuevo = max(nuevo, float(min_abs))
            if pd.notnull(max_abs):
                nuevo = min(nuevo, float(max_abs))
            req_df.at[idx, "valor_por_kg"] = nuevo
        else:
            if pd.notnull(min_abs):
                req_df.at[idx, "valor_por_kg"] = max(base, float(min_abs))
            else:
                req_df.at[idx, "valor_por_kg"] = base
    return req_df
