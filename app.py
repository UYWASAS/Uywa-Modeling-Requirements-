# ==========================================
# BLOQUE 1: IMPORTS, ESTILOS Y UTILIDADES
# ==========================================
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Importa tus modelos y helpers
from models.energy import PigGrowEnergy  # Completa con el resto de modelos según especies/etapas
from models.scale import scale_nutrients
from helpers import energy_unit_convert

# --- ESTILO CSS para cards, títulos, etc. ---
st.markdown("""
    <style>
    .main-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 2.1em !important;
        font-weight: 700;
        margin-bottom:0.1em;
    }
    .subtitle {
        font-size: 1.1em;
        color: #555;
    }
    div[data-testid="metric-container"] {
        background-color: #E0F7FA !important;
        border-radius: 8px;
        padding: 16px;
        margin: 4px;
    }
    .stDownloadButton>button {
        background-color: #00838F;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# BLOQUE 2: SIDEBAR - LOGO Y ENTRADAS GLOBALES
# ==========================================
logo_path = "assets/logo_empresa.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.markdown("**[Logo no encontrado]**")

st.sidebar.title("NutriEnergia")
st.sidebar.markdown("Modelador de requerimientos energéticos y dietarios\nDesarrollado por Uywa")

especie = st.sidebar.selectbox("Especie", ["Porcinos", "Aves"])
if especie == "Porcinos":
    etapa = st.sidebar.selectbox("Categoría", ["Crecimiento/Cebo", "Gestación", "Lactación"])
elif especie == "Aves":
    etapa = st.sidebar.selectbox("Categoría", ["Broiler", "Ponedora"])
else:
    etapa = None

st.sidebar.markdown("---")
unidad_energia = st.sidebar.radio("Unidad de energía", ["kcal", "kJ", "MJ"], horizontal=True)
archivo_req = st.sidebar.selectbox("Archivo de requerimientos", ["params/nutrients_requirements.csv"])
st.sidebar.info("Coeficientes y reglas editables en la carpeta `params/`.\nFuente: NRC/FEDNA/empresa.")

# ==========================================
# BLOQUE 3: CARGA DE DATOS Y PARÁMETROS SEGÚN ETAPA/ESPECIE
# (Puedes expandir cada especie/etapa en un bloque adicional)
# ==========================================
ME_total_disp = None
AME_requerida_disp = None
FI = None
scaled_nutr = None
csv_out = None

if especie == "Porcinos" and etapa == "Crecimiento/Cebo":
    # --- BLOQUE 3.1: PARÁMETROS Y ENTRADAS PARA PORCINOS CRECIMIENTO/CEBO ---
    pig_grow_df = pd.read_csv("params/pig_grow.csv")
    nutrients_df = pd.read_csv(archivo_req)
    categoria = st.sidebar.selectbox("Sexo/edad", pig_grow_df["categoria"].unique())
    PV = st.sidebar.number_input("Peso vivo (kg)", min_value=1.0, value=50.0, step=0.5)
    ADG = st.sidebar.number_input("Ganancia diaria (g/d)", min_value=0.0, value=700.0, step=1.0)
    f_P = st.sidebar.number_input("Fracción proteica (f_P)", min_value=0.0, max_value=1.0, value=0.17)
    f_G = st.sidebar.number_input("Fracción grasa (f_G)", min_value=0.0, max_value=1.0, value=0.15)
    T_amb = st.sidebar.number_input("Temperatura ambiente (°C)", min_value=0.0, value=20.0)
    AME_dieta = st.sidebar.number_input("AME dieta (kcal/kg)", min_value=1000.0, value=3100.0)
    FI = st.sidebar.number_input("Ingesta diaria (kg/d)", min_value=0.1, value=2.2)

    params = pig_grow_df[pig_grow_df["categoria"] == categoria].iloc[0].to_dict()
    energy_model = PigGrowEnergy(params, unidad_energia)
    # Cálculo energía total (devuelve en kcal)
    ME_total = energy_model.me_total(PV, ADG, f_P, f_G, T_amb)
    # Conversión a unidad elegida
    ME_total_disp = energy_unit_convert(ME_total, "kcal", unidad_energia)
    if FI > 0:
        AME_requerida = ME_total / FI
    else:
        AME_requerida = AME_dieta
    AME_requerida_disp = energy_unit_convert(AME_requerida, "kcal", unidad_energia)

    # Nutrientes escalados
    nutr_stage = nutrients_df[(nutrients_df["especie"] == "broiler") & (nutrients_df["etapa"] == "engorde")]
    scaled_nutr = scale_nutrients(nutr_stage, AME_requerida)
    csv_out = scaled_nutr.to_csv(index=False).encode()

# === BLOQUE 3.2: EJEMPLO PARA BROILER (añade tus modelos y lógica real) ===
elif especie == "Aves" and etapa == "Broiler":
    # Cargar parámetros y entradas específicas para broiler
    broiler_params_df = pd.read_csv("params/broiler.csv")
    nutrients_df = pd.read_csv(archivo_req)
    genetica = st.sidebar.selectbox("Genética", broiler_params_df["genetica"].unique())
    W = st.sidebar.number_input("Peso vivo (kg)", min_value=0.1, value=2.0, step=0.01)
    ADG = st.sidebar.number_input("Ganancia diaria (g/d)", min_value=0.0, value=60.0, step=1.0)
    T_amb = st.sidebar.number_input("Temperatura ambiente (°C)", min_value=0.0, value=22.0)
    FI = st.sidebar.number_input("Ingesta diaria (kg/d)", min_value=0.01, value=0.11)
    # Placeholder: Debes implementar BroilerEnergy en models/energy.py
    # from models.energy import BroilerEnergy
    # params = broiler_params_df[broiler_params_df["genetica"] == genetica].iloc[0].to_dict()
    # energy_model = BroilerEnergy(params, unidad_energia)
    # ME_total = energy_model.me_total(W, ADG, T_amb)
    # ME_total_disp = energy_unit_convert(ME_total, "kcal", unidad_energia)
    # if FI > 0:
    #     AME_requerida = ME_total / FI
    # else:
    #     AME_requerida = 3000
    # AME_requerida_disp = energy_unit_convert(AME_requerida, "kcal", unidad_energia)
    # nutr_stage = nutrients_df[(nutrients_df["especie"] == "broiler") & (nutrients_df["etapa"] == "engorde")]
    # scaled_nutr = scale_nutrients(nutr_stage, AME_requerida)
    # csv_out = scaled_nutr.to_csv(index=False).encode()

# ==========================================
# BLOQUE 4: HEADER PRINCIPAL Y DESCRIPCIÓN
# ==========================================
st.markdown("""
    <div style="display:flex;align-items:center;margin-bottom:8px;">
        <img src="https://cdn-icons-png.flaticon.com/512/616/616408.png" width="55"/>
        <div style="margin-left:18px">
            <span class="main-title">Modelador de Requerimientos Energéticos y Dietarios</span><br>
            <span class="subtitle">Calcula energía total, densidad energética y tabla de nutrientes ajustada por etapa y especie.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("")

# ==========================================
# BLOQUE 5: CARDS DE RESULTADO PRINCIPALES
# ==========================================
if ME_total_disp is not None and AME_requerida_disp is not None and FI is not None:
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Energía total requerida", value=f"{ME_total_disp:.1f} {unidad_energia}/día")
    col2.metric(label="Densidad energética requerida", value=f"{AME_requerida_disp:.0f} {unidad_energia}/kg")
    col3.metric(label="FI utilizada", value=f"{FI:.2f} kg/d")

    st.divider()

    # ==========================================
    # BLOQUE 6: TABLA DE NUTRIENTES ESCALADOS
    # ==========================================
    if scaled_nutr is not None:
        st.markdown("### Nutrientes escalados por kg de dieta")
        st.dataframe(scaled_nutr[["nutriente", "valor_por_kg", "unidad"]], use_container_width=True)
        st.download_button("Descargar CSV", data=csv_out, file_name="nutrientes_escalados.csv")

    # ==========================================
    # BLOQUE 7: GRÁFICO DE SENSIBILIDAD (OPCIONAL)
    # ==========================================
    with st.expander("Mostrar sensibilidad de AME requerida vs FI"):
        fi_range = [x/10 for x in range(10, 40)]
        ame_range = [ME_total_disp / fi for fi in fi_range]
        fig = px.line(x=fi_range, y=ame_range,
                      labels={"x": "FI (kg/d)", "y": f"AME requerida ({unidad_energia}/kg)"},
                      title="Sensibilidad de AME requerida según FI")
        st.plotly_chart(fig, use_container_width=True)

    # ==========================================
    # BLOQUE 8: VALIDACIONES Y MENSAJES
    # ==========================================
    if AME_requerida_disp > 3600 and isinstance(AME_requerida_disp, (int, float)):
        st.warning("AME requerida excede el rango típico para esta etapa. Revisar parámetros o FI.")
    if FI < 0.5:
        st.warning("La FI es muy baja para esta etapa. Revisar.")

# ==========================================
# BLOQUE 9: FOOTER Y CRÉDITOS
# ==========================================
st.markdown("""
<div style="text-align:center;color:gray;font-size:0.9em;margin-top:30px;">
    <em>App de modelado nutricional - v1.0 | Uywa | Coeficientes y reglas calibrables en <code>params/</code></em>
</div>
""", unsafe_allow_html=True)

# ==========================================
# FIN DEL APP.PY
# ==========================================

# NOTA: 
# - Cada bloque está numerado e identificado por nombre.
# - Para agregar nuevas especies/etapas, copia/expande el BLOQUE 3 y adapta los cálculos y entradas.
# - Si agregas nuevos archivos de parámetros, actualiza los selectbox y paths correspondientes.
# - Implementa los modelos restantes en models/energy.py.
