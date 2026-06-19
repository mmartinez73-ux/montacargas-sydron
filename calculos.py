# ============================================
# MÓDULO 7: APP WEB CON STREAMLIT
# ============================================

import streamlit as st
import pandas as pd
from PIL import Image
from calculos import resumen_calculo
from datetime import datetime

# ---- CONFIGURACIÓN ----
st.set_page_config(
    page_title="SYDRON Lift Systems",
    page_icon="🏭",
    layout="wide"
)

# ---- SESSION STATE ----
if "pagina" not in st.session_state:
    st.session_state.pagina = "portada"
if "historial" not in st.session_state:
    st.session_state.historial = []

# ============================================
# PORTADA
# ============================================
if st.session_state.pagina == "portada":

    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] { background-color: #f4f7f6; }
        [data-testid="stHeader"] { background-color: #f4f7f6; }
        div.stButton {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
            margin: 20px 0 !important;
        }
        div.stButton > button {
            background-color: #2c3e50 !important;
            color: white !important;
            font-size: 1.3em !important;
            font-weight: bold !important;
            border-radius: 25px !important;
            padding: 12px 50px !important;
            border: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col_unica, col_vacio = st.columns([1, 5])
    with col_unica:
        try:
            st.image(Image.open("logo_unica.png"), width=120)
        except:
            st.markdown("<b style='color:#2c3e50;'>UNICA</b>", unsafe_allow_html=True)

    st.write("")

    col_iz, col_centro, col_der = st.columns([1, 1.5, 1])
    with col_centro:
        try:
            st.image(Image.open("logo_sydron.png"), width=420)
        except:
            st.markdown("<h1 style='text-align:center;'>🏭</h1>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center; padding: 10px 0;'>
            <h1 style='color:#2c3e50; font-size:3em; font-weight:900;'>
                CALCULADORA DE MONTACARGAS
            </h1>
            <p style='color:#d35400; font-size:1.4em; font-weight:700;'>
                Proyecto Integrador - Ingenieria Industrial
            </p>
            <hr style='border:1.5px solid #2c3e50; width:45%; margin:20px auto;'>
            <p style='color:#7f8c8d; font-size:0.95em;'>
                Universidad Cardenal Miguel Obando Bravo - UNICA | 2026
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("▶  INGRESAR"):
            st.session_state.pagina = "calculadora"
            st.rerun()

# ============================================
# CALCULADORA
# ============================================
else:
    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] { background-color: #1e1e2e; }
        [data-testid="stHeader"] { background-color: #1e1e2e; }
        h1, h2, h3, p, label { color: #ffffff !important; }
        </style>
    """, unsafe_allow_html=True)

    # ---- HEADER ----
    col_logo, col_titulo = st.columns([1, 6])
    with col_logo:
        try:
            st.image(Image.open("logo_unica.png"), width=70)
        except:
            st.write("🏭")
    with col_titulo:
        st.markdown("<h2 style='color:#ffffff; margin-top:10px;'>SYDRON Lift Systems</h2>", unsafe_allow_html=True)

    st.markdown("<​hr style='border:1px solid #444;'>", unsafe_allow_html=True)

    # ---- PESTAÑAS ----
    tab1, tab2, tab3, tab4 = st.tabs(["⚙️ Cálculos", "📋 Historial", "📊 Gráficas", "💾 Exportar"])

    # ============================================
    # TAB 1 — CÁLCULOS
    # ============================================
    with tab1:
        st.markdown("### Parámetros de la Operación")

        col1, col2 = st.columns(2)
        with col1:
            masa_kg         = st.number_input("Masa de la carga (kg)",        min_value=0.1, value=1000.0, step=10.0)
            carga_maxima    = st.number_input("Carga máxima permitida (kg)",   min_value=0.1, value=2000.0, step=10.0)
            distancia_m     = st.number_input("Distancia al centro de carga (m)", min_value=0.1, value=0.5, step=0.1)
            altura_m        = st.number_input("Altura de elevación (m)",       min_value=0.1, value=3.0,   step=0.1)
        with col2:
            tiempo_s        = st.number_input("Tiempo de elevación (s)",       min_value=0.1, value=5.0,   step=0.5)
            peso_contrapeso = st.number_input("Peso del contrapeso (kg)",      min_value=0.1, value=1500.0,step=10.0)
            dist_contrapeso = st.number_input("Distancia del contrapeso (m)",  min_value=0.1, value=1.0,   step=0.1)

        if st.button("⚡ CALCULAR"):
            try:
                resultado = resumen_calculo(
                    masa_kg, carga_maxima, distancia_m,
                    altura_m, tiempo_s, peso_contrapeso, dist_contrapeso
                )
                st.session_state.historial.append(resultado)

                st.markdown("---")
                st.markdown("### Resultados")

                c1, c2, c3 = st.columns(3)
                c1.metric("Peso", f"{resultado['peso_N']} N")
                c2.metric("Factor de Seguridad", resultado['factor_seguridad'])
                c3.metric("Estado", resultado['estado_carga'])

                c4, c5, c6 = st.columns(3)
                c4.metric("Torque", f"{resultado['torque_Nm']} Nm")
                c5.metric("Potencia", f"{resultado['potencia_W']} W")
                c6.metric("Potencia HP", f"{resultado['potencia_HP']} HP")

                st.metric("Estabilidad", resultado['estabilidad'])

            except Exception as e:
                st.error(f"Error: {e}")

    # ============================================
    # TAB 2 — HISTORIAL
    # ============================================
    with tab2:
        st.markdown("### Historial de Cálculos")
        if len(st.session_state.historial) == 0:
            st.info("No hay registros aún. Realizá un cálculo primero.")
        else:
            df = pd.DataFrame(st.session_state.historial)
            st.dataframe(df, use_container_width=True)

            st.markdown("### Estadísticas Descriptivas")
            nums = df.select_dtypes(include="number")
            if not nums.empty:
                st.dataframe(nums.describe().round(2), use_container_width=True)

        if st.button("🗑️ Limpiar historial"):
            st.session_state.historial = []
            st.rerun()

    # ============================================
    # TAB 3 — GRÁFICAS
    # ============================================
    with tab3:
        st.markdown("### Gráficas del Montacargas")
        if len(st.session_state.historial) == 0:
            st.info("No hay datos para graficar. Realizá al menos un cálculo.")
        else:
            df = pd.DataFrame(st.session_state.historial)
            df.index = [f"#{i+1}" for i in range(len(df))]

            opcion = st.selectbox("Seleccionar gráfica:", [
                "Barras — Peso (N)",
                "Líneas — Factor de Seguridad",
                "Barras — Potencia (W)",
                "Barras dobles — Potencia W vs HP"
            ])

            if opcion == "Barras — Peso (N)":
                st.bar_chart(df["peso_N"])
            elif opcion == "Líneas — Factor de Seguridad":
                st.line_chart(df["factor_seguridad"])
            elif opcion == "Barras — Potencia (W)":
                st.bar_chart(df["potencia_W"])
            elif opcion == "Barras dobles — Potencia W vs HP":
                st.bar_chart(df[["potencia_W", "potencia_HP"]])

    # ============================================
    # TAB 4 — EXPORTAR
    # ============================================
    with tab4:
        st.markdown("### Exportar Historial")
        if len(st.session_state.historial) == 0:
            st.info("No hay registros para exportar.")
        else:
            df = pd.DataFrame(st.session_state.historial)

            csv = df.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                label="⬇️ Descargar CSV",
                data=csv,
                file_name=f"historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

            txt = f"REPORTE HISTORIAL - SYDRON\nFecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
            txt += f"Total registros: {len(df)}\n\n"
            for i, r in enumerate(st.session_state.historial, 1):
                txt += f"--- Registro #{i} ---\n"
                for k, v in r.items():
                    txt += f"  {k}: {v}\n"
                txt += "\n"

            st.download_button(
                label="⬇️ Descargar TXT",
                data=txt,
                file_name=f"historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
