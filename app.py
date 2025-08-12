import streamlit as st
import pandas as pd
import plotly.express as px
import os

from models.energy import PigGrowEnergy
from models.scale import scale_nutrients
from helpers import energy_unit_convert
from auth import USERS_DB

# ==== NUEVO: Importar módulos para la pestaña de energía de materias primas ====
from core.ingredients import IngredientInput, get_ingredient_defaults, load_ingredients_map
from core.selector import select_equation, list_applicable_equations
from core.equations import compute_energy
from core.scaling import scale_nutrients as scale_nutrients_ingredientes
from core.utils import (
    convert_unit,
    check_range,
    convert_asfed_ms,
    show_cheatsheet,
)

# =========================
# BLOQUE 0: LOGIN Y SESIÓN
# =========================
def login():
    st.markdown(
        """
        <div style='display:flex;align-items:center;justify-content:center;margin-bottom:24px;'>
            <span style="font-size:2.2em;font-family:'Montserrat',sans-serif;font-weight:700;color:#19345c;">NutriEnergia</span><br>
            <span style="font-size:1.1em;color:#19345c;font-family:'Montserrat',sans-serif;">Plataforma de modelado nutricional</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.title("Iniciar sesión")
    username = st.text_input("Usuario", key="usuario_login")
    password = st.text_input("Contraseña", type="password", key="password_login")
    login_btn = st.button("Entrar", key="entrar_login")
    if login_btn:
        user = USERS_DB.get(username.strip().lower())
        if user and user["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["usuario"] = username.strip()
            st.session_state["user"] = user
            st.success(f"Bienvenido, {user['name']}!")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.stop()

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login()

USER_KEY = f"uywa_req_{st.session_state['usuario']}"
user = st.session_state["user"]

# ========================
# BLOQUE 1: ESTILO CSS
# ========================
st.markdown("""
    <style>
    html, body, .stApp, .main, .block-container {
        background: linear-gradient(120deg, #f4f7fa 0%, #e3ecf7 100%) !important;
    }
    section[data-testid="stSidebar"] {
        background: #19345c !important;
        color: #fff !important;
        border-right: 1.5px solid #14233c !important;
    }
    section[data-testid="stSidebar"] * {
        color: #fff !important;
        font-family: 'Montserrat', sans-serif !important;
    }
    .card-box {
        background: none !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin-bottom: 0 !important;
    }
    .main-title, h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif !important;
        color: #19345c !important;
        font-weight: 750 !important;
        margin-bottom:0.1em;
        letter-spacing: 0.01em;
    }
    .subtitle {
        font-size: 1.18em;
        color: #2e4771;
        font-family: 'Montserrat', sans-serif !important;
    }
    .stDownloadButton>button {
        background-color: #00838F;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    div[data-testid="metric-container"] {
        background-color: #f3fafd !important;
        border-radius: 8px;
        padding: 16px;
        margin: 4px;
        font-family: 'Montserrat', sans-serif !important;
        border: 1px solid #dde7f7 !important;
        color: #19345c !important;
    }
    .stDataFrame thead tr th { font-family: 'Montserrat', sans-serif !important; color: #19345c !important;}
    .stDataFrame tbody tr td { font-family: 'Montserrat', sans-serif !important;}
    hr, .stDivider {
        border: none;
        border-top: 2px solid #dde7f7 !important;
        margin: 32px 0 22px 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ========================
# BLOQUE 2: SIDEBAR
# ========================
with st.sidebar:
    logo_path = "assets/logo_empresa.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    st.markdown(
        """
        <div style='text-align: center; margin-bottom:10px;'>
            <div style='font-size:30px;font-family:Montserrat,Arial;color:#fff; margin-top: 10px;letter-spacing:1px; font-weight:700; line-height:1.1;'>
                NutriEnergia
            </div>
            <div style='font-size:15px;color:#fff; margin-top: 4px; font-family:Montserrat,Arial; line-height: 1.1;'>
                Modelador de requerimientos energéticos y dietarios
            </div>
            <hr style='border-top:1px solid #2e4771; margin: 14px 0;'>
            <div style='font-size:13px;color:#fff; margin-top: 6px;'>
                <b>Contacto:</b> uywasas@gmail.com<br>
                Desarrollado por Uywa
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ========================
# BLOQUE 3: PESTAÑAS PRINCIPALES
# ========================

tabs = st.tabs([
    "Modelador de requerimientos",
    "Energía de materias primas"
])

# ========== PESTAÑA 1: MODELO DE REQUERIMIENTOS ==========
with tabs[0]:
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
      <div>
        <div class="main-title" style="margin-bottom:0.25em; font-size:1.35em;">
          Modelador de Requerimientos Energéticos y Dietarios
        </div>
        <div class="subtitle" style="font-size:1.05em;">
          Calcula energía total, densidad energética y tabla de nutrientes ajustada por etapa y especie.
        </div>
      </div>
      <div style="font-size:1em; color:#233a61;">Usuario: <b>{st.session_state['usuario']}</b></div>
    </div>
    <hr style="border-top:2px solid #dde7f7; margin: 18px 0 20px 0;">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown('<div class="main-title" style="font-size:1.18em; margin-bottom:0.35em;">1. Seleccione especie y etapa</div>', unsafe_allow_html=True)
        especie = st.selectbox("Especie", ["Porcinos", "Aves"], key="especie_main")
        if especie == "Porcinos":
            etapa = st.selectbox("Categoría", ["Crecimiento/Cebo", "Gestación", "Lactación"], key="etapa_porcino")
        elif especie == "Aves":
            etapa = st.selectbox("Categoría", ["Broiler", "Ponedora"], key="etapa_ave")
        else:
            etapa = None
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown('<div class="main-title" style="font-size:1.18em; margin-bottom:0.35em;">2. Configuración general</div>', unsafe_allow_html=True)
        unidad_energia = st.radio("Unidad de energía", ["kcal", "kJ", "MJ"], horizontal=True, key="unidad_energia_main")
        archivo_req = st.selectbox("Archivo de requerimientos", ["params/nutrients_requirements.csv"], key="archivo_req_main")
        st.info("Todos los coeficientes y reglas son editables desde la carpeta `params/`.\nFuente: NRC/FEDNA/empresa.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    # -------- BLOQUE DE PORCINOS CRECIMIENTO/CEBO CON ESCALAMIENTO REAL --------
    ME_total_disp = None
    AME_requerida_disp = None
    FI = None
    scaled_nutr = None
    csv_out = None

    if especie == "Porcinos" and etapa == "Crecimiento/Cebo":
        st.markdown('<div class="main-title" style="font-size:1.12em; margin-bottom:0.3em;">Parámetros productivos - Crecimiento/Cebo</div>', unsafe_allow_html=True)
        pig_grow_df = pd.read_csv("params/pig_grow.csv")
        nutrients_df = pd.read_csv(archivo_req)
        categoria = st.selectbox("Sexo/edad", pig_grow_df["categoria"].unique(), key="categoria_porcino")
        PV = st.number_input("Peso vivo (kg)", min_value=1.0, value=50.0, step=0.5, key="pv_porcino")
        ADG = st.number_input("Ganancia diaria (g/d)", min_value=0.0, value=700.0, step=1.0, key="adg_porcino")
        f_P = st.number_input("Fracción proteica (f_P)", min_value=0.0, max_value=1.0, value=0.17, key="fp_porcino")
        f_G = st.number_input("Fracción grasa (f_G)", min_value=0.0, max_value=1.0, value=0.15, key="fg_porcino")
        T_amb = st.number_input("Temperatura ambiente (°C)", min_value=0.0, value=20.0, key="tamb_porcino")
        AME_dieta = st.number_input("AME dieta (kcal/kg)", min_value=1000.0, value=3100.0, key="amedieta_porcino")
        FI = st.number_input("Ingesta diaria (kg/d)", min_value=0.1, value=2.2, key="fi_porcino")

        params = pig_grow_df[pig_grow_df["categoria"] == categoria].iloc[0].to_dict()
        energy_model = PigGrowEnergy(params, unidad_energia)
        ME_total = energy_model.me_total(PV, ADG, f_P, f_G, T_amb)
        ME_total_disp = energy_unit_convert(ME_total, "kcal", unidad_energia)
        if FI > 0:
            AME_requerida = ME_total / FI
        else:
            AME_requerida = AME_dieta
        AME_requerida_disp = energy_unit_convert(AME_requerida, "kcal", unidad_energia)

        # Selección de ETAPA según peso vivo
        if PV < 60:
            etapa_nutr = "20-60"
        elif PV < 100:
            etapa_nutr = "60-100"
        else:
            etapa_nutr = ">100"

        nutr_stage = nutrients_df[(nutrients_df["especie"] == "porcino") & (nutrients_df["etapa"] == etapa_nutr)].copy()

        # --- Normaliza columnas y tipos:
        nutr_stage["valor_por_kg"] = pd.to_numeric(nutr_stage["valor_por_kg"], errors='coerce')
        nutr_stage["referencia_AME_kcalkg"] = pd.to_numeric(nutr_stage["referencia_AME_kcalkg"], errors='coerce')
        nutr_stage["escalable"] = nutr_stage["escalable"].astype(str).str.lower().map({"true": True, "false": False})

        # Haz el escalamiento:
        scaled_nutr = scale_nutrients(nutr_stage, AME_requerida)
        csv_out = scaled_nutr.to_csv(index=False).encode()

        energia_ref = nutr_stage["referencia_AME_kcalkg"].iloc[0]
        st.caption(f"Energía estándar de referencia para la etapa: {energia_ref} kcal/kg")

    elif especie == "Aves" and etapa == "Broiler":
        st.markdown('<div class="main-title" style="font-size:1.12em; margin-bottom:0.3em;">Parámetros productivos - Broiler</div>', unsafe_allow_html=True)
        broiler_params_df = pd.read_csv("params/broiler.csv")
        nutrients_df = pd.read_csv(archivo_req)
        genetica = st.selectbox("Genética", broiler_params_df["genetica"].unique(), key="genetica_broiler")
        W = st.number_input("Peso vivo (kg)", min_value=0.1, value=2.0, step=0.01, key="w_broiler")
        ADG = st.number_input("Ganancia diaria (g/d)", min_value=0.0, value=60.0, step=1.0, key="adg_broiler")
        T_amb = st.number_input("Temperatura ambiente (°C)", min_value=0.0, value=22.0, key="tamb_broiler")
        FI = st.number_input("Ingesta diaria (kg/d)", min_value=0.01, value=0.11, key="fi_broiler")
        # Placeholder lógica, implementar modelo real

    st.markdown('<hr>', unsafe_allow_html=True)

    if ME_total_disp is not None and AME_requerida_disp is not None and FI is not None:
        st.markdown('<div class="card-box">', unsafe_allow_html=True)
        st.markdown('<div class="main-title" style="font-size:1.12em; margin-bottom:0.3em;">Resultados principales</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Energía total requerida", value=f"{ME_total_disp:.1f} {unidad_energia}/día")
        col2.metric(label="Densidad energética requerida", value=f"{AME_requerida_disp:.0f} {unidad_energia}/kg")
        col3.metric(label="FI utilizada", value=f"{FI:.2f} kg/d")
        st.markdown('</div>', unsafe_allow_html=True)

        if scaled_nutr is not None:
            st.markdown('<div class="card-box">', unsafe_allow_html=True)
            st.markdown('<div class="main-title" style="font-size:1.12em; margin-bottom:0.3em;">Nutrientes escalados por kg de dieta</div>', unsafe_allow_html=True)
            st.dataframe(scaled_nutr[["nutriente", "valor_por_kg", "unidad"]], use_container_width=True)
            st.download_button("Descargar CSV", data=csv_out, file_name="nutrientes_escalados.csv")
            st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("Mostrar sensibilidad de AME requerida vs FI"):
            fi_range = [x/10 for x in range(10, 40)]
            ame_range = [ME_total_disp / fi for fi in fi_range]
            fig = px.line(
                x=fi_range, y=ame_range,
                labels={"x": "FI (kg/d)", "y": f"AME requerida ({unidad_energia}/kg)"},
                title="Sensibilidad de AME requerida según FI",
                template="simple_white",
                color_discrete_sequence=["#19345c"]
            )
            fig.update_layout(font=dict(family="Montserrat, Arial", size=14, color="#19345c"))
            st.plotly_chart(fig, use_container_width=True)

        if AME_requerida_disp > 3600 and isinstance(AME_requerida_disp, (int, float)):
            st.warning("AME requerida excede el rango típico para esta etapa. Revisar parámetros o FI.")
        if FI < 0.5:
            st.warning("La FI es muy baja para esta etapa. Revisar.")

    st.markdown("""
    <div style="text-align:center;color:gray;font-size:0.97em;margin-top:40px;font-family:Montserrat,Arial;">
        <em>App de modelado nutricional - v1.0 | Uywa | Todos los coeficientes y reglas calibrables en <code>params/</code></em>
    </div>
    """, unsafe_allow_html=True)

# ========== PESTAÑA 2: ENERGÍA DE MATERIAS PRIMAS ==========
with tabs[1]:
    st.markdown(f"""
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
      <div>
        <div class="main-title" style="margin-bottom:0.25em; font-size:1.35em;">
          Estimador y Ajustador Energético de Materias Primas
        </div>
        <div class="subtitle" style="font-size:1.05em;">
          Calcula el valor energético estimado de ingredientes para aves (MEn) y cerdos (ME/NE), con ajuste de nutrientes por kg de dieta.
        </div>
      </div>
      <div style="font-size:1em; color:#233a61;">Usuario: <b>{st.session_state['usuario']}</b></div>
    </div>
    <hr style="border-top:2px solid #dde7f7; margin: 18px 0 20px 0;">
    """, unsafe_allow_html=True)

    # ------ BLOQUE 2.1: Selección de especie y materia prima ------
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    colmp1, colmp2, colmp3 = st.columns([1,1.2,1])
    # Cargar el mapa de ingredientes (solo una vez)
    if "ingredients_map" not in st.session_state:
        st.session_state["ingredients_map"] = load_ingredients_map("data/ingredients_map.csv")
    ingredients_map = st.session_state["ingredients_map"]
    with colmp1:
        especie_mp = st.selectbox("Especie", ["Aves", "Cerdos"], key="especie_mp")
        unidad_energia_mp = st.radio("Unidad de energía", ["kcal/kg", "MJ/kg"], horizontal=True, key="unidad_energia_mp")
        unidad_base_mp = st.radio("Base análisis", ["MS", "as-fed"], horizontal=True, key="unidad_base_mp")
    with colmp2:
        familia_options = ingredients_map["familia"].unique()
        familia = st.selectbox("Familia de ingrediente", familia_options, key="familia_mp")
    with colmp3:
        matprima_options = ingredients_map[ingredients_map["familia"]==familia]["ingrediente"].tolist()
        matprima_options.append("Ingrediente genérico")
        materia_prima = st.selectbox("Materia prima", matprima_options, key="materia_prima_mp")
    st.markdown('</div>', unsafe_allow_html=True)

    # ------ BLOQUE 2.2: Entrada/carga de composición ------
    st.subheader("Composición del ingrediente (editable o carga CSV)")
    if "data_upload" not in st.session_state:
        st.session_state["data_upload"] = None
    uploaded = st.file_uploader("Cargar composición desde CSV", type="csv")
    if uploaded:
        comp_df = pd.read_csv(uploaded)
        st.session_state["data_upload"] = comp_df
    else:
        defaults = get_ingredient_defaults(materia_prima, familia, especie_mp)
        comp_df = pd.DataFrame([defaults])
    comp_edit = st.data_editor(comp_df, num_rows="fixed", key="edit_comp")

    # ------ BLOQUE 2.3: Selección de ecuación ------
    st.subheader("Selección de ecuación energética")
    eq_mode = st.radio("Modo de selección de ecuación", ["Automática", "Manual"], key="modo_ecuacion_mp")
    available_eqs = list_applicable_equations(especie_mp, familia, comp_edit)
    if eq_mode == "Manual":
        eq_choice = st.selectbox("Ecuación (manual)", available_eqs, key="ec_manual_mp")
        # Aquí podrías mostrar requisitos de entrada de la ecuación seleccionada
        st.info(f"Requiere: {available_eqs[0] if isinstance(available_eqs, list) and available_eqs else 'N/A'}")
    else:
        eq_choice = select_equation(especie_mp, familia, comp_edit)
        st.info(f"Ecuación seleccionada automáticamente: {eq_choice}")

# ========================
# BLOQUE 2.4: Cálculo energético (corregido para NRC)
# ========================
st.subheader("Resultado energético estimado")

# Recopilación de inputs del DataFrame editable
inputs_dict = {}
for col in comp_edit.columns:
    try:
        val = float(comp_edit.iloc[0][col])
        # --- CORRECCIÓN DE UNIDADES ---
        # Si el valor está en g/kg y es un nutriente principal, conviértelo a %
        if col in ["Ash", "CP", "EE", "CF", "NDF", "ADF", "Starch", "Sugars", "GE"]:
            val = val / 10  # g/kg -> %
    except Exception:
        val = None
    inputs_dict[col] = val

# Calcular NFE (%) si falta y hay datos suficientes
if "NFE" not in inputs_dict or inputs_dict["NFE"] is None:
    required = ["Ash", "CP", "EE", "CF"]
    if all(inputs_dict.get(x) is not None for x in required):
        inputs_dict["NFE"] = 100 - (
            inputs_dict.get("Ash", 0)
            + inputs_dict.get("CP", 0)
            + inputs_dict.get("EE", 0)
            + inputs_dict.get("CF", 0)
        )

method_name = None
if eq_mode == "Manual":
    method_name = eq_choice.split()[0] if isinstance(eq_choice, str) else None

try:
    result = compute_energy(
        species="poultry" if especie_mp == "Aves" else "swine",
        family=familia,
        method=method_name,
        inputs=inputs_dict,
        return_asfed=(unidad_base_mp == "as-fed"),
        DM_pct=inputs_dict.get("DM", None),
        decimals=1
    )
    energia = result["value"]
    ecuacion_usada = result["equation"]
    variables_usadas = list(inputs_dict.keys())
    advertencias = result.get("notes", [])
    st.metric(label="Energía estimada", value=f"{energia:.1f} {unidad_energia_mp}")
    st.caption(f"Ecuación usada: {ecuacion_usada}")
    st.caption(f"Variables usadas: {variables_usadas}")
    if advertencias:
        st.warning(" | ".join(advertencias))
except Exception as e:
    st.error(f"Error en el cálculo energético: {e}")
    
    # ------ BLOQUE 2.5: Ajuste a dieta y escalado de nutrientes ------
    st.subheader("Ajuste a dieta y escalado de nutrientes")
    FI_mp = st.number_input("Consumo diario orientativo (kg/d)", min_value=0.01, value=1.0, key="fi_mp")
    req_file = "requirements/req_nutrients.csv"
    req_df = pd.read_csv(req_file)
    out_df = scale_nutrients_ingredientes(req_df, energia)
    st.dataframe(out_df)

    # ------ BLOQUE 2.6: Descarga y log ------
    st.download_button("Descargar resultados (CSV)", data=out_df.to_csv(index=False).encode(), file_name="ajuste_nutrientes.csv")
    with st.expander("Log de decisiones y advertencias"):
        st.write({
            "ecuacion_usada": ecuacion_usada,
            "variables_usadas": variables_usadas,
            "advertencias": advertencias
        })

    # ------ BLOQUE 2.7: Cheat-sheet ------
    show_cheatsheet(familia)

    # Mensaje UX
    st.info("Todos los cálculos se realizan sobre base de materia seca (MS); asegúrate de que la composición esté en la base correcta.")

# ========================
# BLOQUE FINAL: FOOTER
# ========================
st.markdown("""
<div style="text-align:center;color:gray;font-size:0.97em;margin-top:40px;font-family:Montserrat,Arial;">
    <em>App de modelado nutricional - v1.0 | Uywa | Todos los coeficientes y reglas calibrables en <code>params/</code> y <code>requirements/</code></em>
</div>
""", unsafe_allow_html=True)
