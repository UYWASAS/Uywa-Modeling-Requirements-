import pandas as pd

def scale_nutrients(nutr_df, AME_requerida, AME_base_col="referencia_AME_kcalkg"):
    """
    Escala los nutrientes proporcionalmente a la nueva AME requerida.
    Solo escala los marcados como 'escalable', el resto usa min_absoluto si aplica.
    """
    nutr_df = nutr_df.copy()
    for idx, row in nutr_df.iterrows():
        if row["escalable"] == True or row["escalable"] == "True":
            nutr_df.at[idx, "valor_por_kg"] = row["valor_por_kg"] * (AME_requerida / row[AME_base_col])
        else:
            # Si hay min_absoluto, usarlo como mínimo.
            min_abs = row.get("min_absoluto", None)
            if min_abs is not None:
                nutr_df.at[idx, "valor_por_kg"] = max(row["valor_por_kg"], min_abs)
    return nutr_df
