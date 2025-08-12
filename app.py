import streamlit as st
import pandas as pd
from models.energy import PigGrowEnergy
from models.scale import scale_nutrients
from helpers import energy_unit_convert

# Cargar parámetros precargados
pig_grow_df = pd.read_csv("params/pig_grow.csv")
nutrients_df = pd.read_csv("params/nutrients_requirements.csv")

st.set_page_config(page_title="Requerimientos energéticos animales", layout="wide")

st.sidebar.title("Configuración")
especie = st.sidebar.selectbox("Especie", ["porcino", "ave"])
if especie == "porcino":
    etapa = st.sidebar.selectbox("Categoría", ["crecimiento/cebo", "gestación", "lactación"])
elif especie == "ave":
    etapa = st.sidebar.selectbox("Categoría", ["broiler", "ponedora"])

unidad_energia = st.sidebar.selectbox("Unidad de energía", ["kcal", "kJ", "MJ"])

# Inputs dinámicos según especie/etapa
if especie == "porcino" and etapa == "crecimiento/cebo":
    categoria = st.sidebar.selectbox("Categoría sexo/edad", pig_grow_df["categoria"].unique())
    PV = st.sidebar.number_input("Peso vivo (kg)", min_value=1.0, value=50.0)
    ADG = st.sidebar.number_input("Ganancia diaria (g/d)", min_value=0.0, value=700.0)
    f_P = st.sidebar.number_input("Fracción proteica (f_P)", min_value=0.0, max_value=1.0, value=0.17)
    f_G = st.sidebar.number_input("Fracción grasa (f_G)", min_value=0.0, max_value=1.0, value=0.15)
    T_amb = st.sidebar.number_input("Temp. ambiente (°C)", min_value=0.0, value=20.0)
    AME_dieta = st.sidebar.number_input("AME dieta (kcal/kg)", min_value=1000.0, value=3100.0)
    FI = st.sidebar.number_input("Ingesta diaria (kg/d)", min_value=0.1, value=2.2)
    params = pig_grow_df[pig_grow_df["categoria"] == categoria].iloc[0].to_dict()
    energy_model = PigGrowEnergy(params, unidad_energia)
    ME_total = energy_model.me_total(PV, ADG, f_P, f_G, T_amb)
    # Conversión de unidad si aplica
    ME_total = energy_unit_convert(ME_total, "kcal", unidad_energia)
    if FI > 0:
        AME_requerida = ME_total / FI
    else:
        AME_requerida = AME_dieta
    # Filtrar nutrientes base
    nutr_stage = nutrients_df[(nutrients_df["especie"] == "broiler") & (nutrients_df["etapa"] == "engorde")]
    scaled_nutr = scale_nutrients(nutr_stage, AME_requerida)

    # Resultados
    st.markdown("## Resultados")
    st.metric(f"Energía total requerida (ME_total)", f"{ME_total:.1f} {unidad_energia}/día")
    st.metric("Densidad energética requerida (AME)", f"{AME_requerida:.0f} {unidad_energia}/kg")
    st.metric("FI utilizada (kg/d)", f"{FI:.2f}")

    st.markdown("### Nutrientes escalados por kg")
    st.dataframe(scaled_nutr[["nutriente", "valor_por_kg", "unidad"]])

    csv_out = scaled_nutr.to_csv(index=False).encode()
    st.download_button("Descargar CSV nutrientes", data=csv_out, file_name="nutrientes_escalados.csv")

    # Validaciones
    if AME_requerida > 3600:
        st.warning("AME_requerida excede el rango típico para esta etapa. Revisar parámetros o FI.")
    if FI < 0.5:
        st.warning("La FI es muy baja para cerdos en crecimiento. Revisar.")

# (Agregar lógica análoga para otras especies/etapas)
st.sidebar.markdown("---")
st.sidebar.info("Todos los coeficientes son calibrables desde CSV en /params. Consulte NRC/FEDNA para ajustar.")
