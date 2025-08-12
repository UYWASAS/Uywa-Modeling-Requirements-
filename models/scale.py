import pandas as pd

def scale_nutrients(nutr_df, AME_requerida, AME_base_col="referencia_AME_kcalkg"):
    nutr_df = nutr_df.copy()
    for idx, row in nutr_df.iterrows():
        base = row["valor_por_kg"]
        escalable = row["escalable"]
        min_abs = row.get("min_absoluto", None)
        max_abs = row.get("max", None)
        ref_AME = row[AME_base_col]

        if pd.isna(ref_AME) or ref_AME == 0:
            nutr_df.at[idx, "valor_por_kg"] = base  # No hay energía de referencia, no escalar.
            continue

        if escalable is True:
            nuevo_valor = base * (AME_requerida / ref_AME)
            # Limita por mínimo y máximo si están definidos
            if pd.notnull(min_abs):
                nuevo_valor = max(nuevo_valor, float(min_abs))
            if pd.notnull(max_abs):
                nuevo_valor = min(nuevo_valor, float(max_abs))
            nutr_df.at[idx, "valor_por_kg"] = nuevo_valor
        else:
            # No escalable, pero respeta mínimo absoluto si existe
            if pd.notnull(min_abs):
                nutr_df.at[idx, "valor_por_kg"] = max(base, float(min_abs))
            else:
                nutr_df.at[idx, "valor_por_kg"] = base
    return nutr_df
