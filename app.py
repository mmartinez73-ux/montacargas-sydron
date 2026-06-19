# ============================================
# MÓDULO 7: APP WEB CON STREAMLIT
# ============================================

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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
        [data-testid="stBottom"] { background-color: #f4f7f6; }
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
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1) !important;
        }
        div.stButton > button:hover {
            background-color: #1a252f !important;
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
            st.markdown("<h1 style='text-align:center; color:#2c3e50;'>🏭</h1>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align:center; padding: 10px 0;'>
            <h1 style='color:#2c3e50; font-size:3.4em; font-weight:900;
                       letter-spacing:2px; margin-bottom:10px;'>
                CALCULADORA DE MONTACARGAS
            </h1>
            <p style='color:#d35400; font-size:1.5em; font-weight:700; margin-bottom:5px;'>
                Proyecto Integrador - Ingenieria Industrial
            </p>
            <hr style='border:1.5px solid #2c3e50; width:45%; margin:20px auto;'>
            <p style='color:#7f8c8d; font-size:0.95em;'>
                Universidad Cardenal Miguel Obando Bravo - UNICA | 2026
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        @keyframes subir {
            0%   { transform: translateY(10px); }
            50%  { transform: translateY(-25px); }
            100% { transform: translateY(10px); }
        }
        @keyframes mover {
            0%   { transform: translateX(-20px); }
            50%  { transform: translateX(20px); }
            100% { transform: translateX(-20px); }
        }
        .montacargas {
            font-size: 5em;
            display: inline-block;
            animation: mover 4s ease-in-out infinite;
        }
        .carga {
            font-size: 2.2em;
            display: inline-block;
            animation: mover 4s ease-in-out infinite, subir 2s ease-in-out infinite;
            margin-right: -45px;
            vertical-align: top;
            position: relative;
            z-index: 2;
        }
        </style>
        <div style="text-align:center; margin:15px auto; padding:15px;
                    background:rgba(44,62,80,0.03); border-radius:20px; width:50%;">
            <span class="carga">📦</span>
            <span class="montacargas">🚜</span>
            <p style="color:#7f8c8d; font-size:1em; font-weight:500; margin-top:15px;">
                Sistema de simulacion y calculo profesional
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("")

    col_b1, col_b2, col_b3 = st.columns([2, 1, 2])
    with col_b2:
        if st.button("▶  INGRESAR"):
            st.session_state.pagina = "app"
            st.rerun()

    st.markdown("""
        <div style='text-align:center; margin-top:40px;'>
            <p style='color:#bdc3c7; font-size:0.85em;'>
                2026 - SYDRON Lift Systems | Proyecto Montacargas UNICA
            </p>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# APP PRINCIPAL
# ============================================
elif st.session_state.pagina == "app":

    st.markdown("""
        <style>
        [data-testid="stAppViewContainer"] { background-color: #dff3fb; }
        [data-testid="stHeader"] { background-color: #dff3fb; }
        [data-testid="stBottom"] { background-color: #dff3fb; }
        h1, h2, h3, h4, p, label, div { color: #000000 !important; }
        [data-testid="stMetricLabel"] > div { color: #000000 !important; }
        [data-testid="stMetricValue"] > div { color: #000000 !important; }
        div.stButton > button {
            background-color: #e74c3c !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            font-size: 1.1em !important;
            width: 100% !important;
            padding: 12px !important;
        }
        div.stButton > button:hover { background-color: #c0392b !important; }
        [data-testid="stNumberInput"] input { color: #000000 !important; }
        .stTabs [data-baseweb="tab"] { color: #000000 !important; }
        [data-testid="stTabsContent"] > div:nth-child(1) {
            background-color: #dff3fb !important;
            border-radius: 10px; padding: 15px;
        }
        [data-testid="stTabsContent"] > div:nth-child(2) {
            background-color: #fef9e7 !important;
            border-radius: 10px; padding: 15px;
        }
        [data-testid="stTabsContent"] > div:nth-child(3) {
            background-color: #eafaf1 !important;
            border-radius: 10px; padding: 15px;
        }
        [data-testid="stTabsContent"] > div:nth-child(4) {
            background-color: #fdf2f8 !important;
            border-radius: 10px; padding: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        try:
            st.image(Image.open("logo_sydron.png"), width=180)
        except:
            pass
    with col2:
        st.markdown("""
            <div style='text-align:center;'>
                <h1 style='color:#000000 !important; font-size:2.2em;
                           font-weight:900; margin-bottom:0;'>
                    CALCULADORA DE MONTACARGAS
                </h1>
                <p style='color:#333333 !important; margin-top:5px; font-size:1em;'>
                    Proyecto Integrador - Ingenieria Industrial
                </p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        try:
            st.image(Image.open("logo_unica.png"), width=110)
        except:
            pass

    st.divider()

    if st.button("← Volver al Inicio"):
        st.session_state.pagina = "portada"
        st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs([
        "⚙️ Calculos",
        "📋 Historial",
        "📊 Graficas",
        "💾 Exportar"
    ])

    # ============================================
    # PESTAÑA 1: CÁLCULOS
    # ============================================
    with tab1:
        st.subheader("🔧 Datos de Entrada")
        col1, col2 = st.columns(2)
        with col1:
            masa_kg         = st.number_input("Masa de carga (kg):",         min_value=0.0, step=1.0, value=800.0)
            carga_maxima    = st.number_input("Carga maxima (kg):",           min_value=0.0, step=1.0, value=2000.0)
            distancia_m     = st.number_input("Distancia al pivote (m):",    min_value=0.0, step=0.1, value=1.5)
            altura_m        = st.number_input("Altura de elevacion (m):",    min_value=0.0, step=0.1, value=3.0)
        with col2:
            tiempo_s        = st.number_input("Tiempo de elevacion (s):",    min_value=0.1, step=0.1, value=10.0)
            peso_contrapeso = st.number_input("Peso contrapeso (kg):",       min_value=0.0, step=1.0, value=1500.0)
            dist_contrapeso = st.number_input("Distancia contrapeso (m):",   min_value=0.0, step=0.1, value=1.2)

        st.write("")
        if st.button("⚙️ CALCULAR"):
            try:
                resultado = resumen_calculo(
                    masa_kg=masa_kg,
                    carga_maxima=carga_maxima,
                    distancia_m=distancia_m,
                    altura_m=altura_m,
                    tiempo_s=tiempo_s,
                    peso_contrapeso=peso_contrapeso,
                    dist_contrapeso=dist_contrapeso
                )
                st.session_state.historial.append(resultado)
                st.success("Calculo realizado exitosamente!")
                st.divider()
                st.subheader("Resultados")
                m1, m2, m3 = st.columns(3)
                m1.metric("Peso (N)",            resultado["peso_N"])
                m2.metric("Factor de Seguridad", resultado["factor_seguridad"])
                m3.metric("Estado",              resultado["estado_carga"])
                m4, m5, m6 = st.columns(3)
                m4.metric("Torque (Nm)",  resultado["torque_Nm"])
                m5.metric("Potencia (W)", resultado["potencia_W"])
                m6.metric("Estabilidad",  resultado["estabilidad"])
            except ValueError as e:
                st.error(f"Error de entrada: {e}")
            except Exception as e:
                st.error(f"Error inesperado: {e}")

    # ============================================
    # PESTAÑA 2: HISTORIAL
    # ============================================
    with tab2:
        st.subheader("📋 Historial de Calculos")
        if len(st.session_state.historial) == 0:
            st.info("No hay registros aun. Realiza un calculo primero.")
        else:
            df = pd.DataFrame(st.session_state.historial)
            st.dataframe(df, use_container_width=True)
            st.divider()
            st.subheader("Estadisticas")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total registros",    len(df))
            c2.metric("Masa promedio (kg)", round(df["masa_kg"].mean(), 2))
            c3.metric("Peso maximo (N)",    round(df["peso_N"].max(), 2))
            c4.metric("F. Seguridad min",   round(df["factor_seguridad"].min(), 2))
        if st.button("🗑️ Limpiar historial"):
            st.session_state.historial.clear()
            st.rerun()

    # ============================================
    # PESTAÑA 3: GRÁFICAS
    # ============================================
    with tab3:
        st.subheader("📊 Visualizacion de Datos")
        if len(st.session_state.historial) == 0:
            st.info("No hay datos para graficar. Realiza al menos un calculo.")
        else:
            df = pd.DataFrame(st.session_state.historial)
            registros = list(range(1, len(df) + 1))
            opcion = st.selectbox("Selecciona una grafica", [
                "Barras - Peso (N)",
                "Lineas - Factor de Seguridad",
                "Pastel - Estados de Carga",
                "Barras dobles - Potencia W vs HP"
            ])
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor("#eafaf1")
            ax.set_facecolor("#eafaf1")
            ax.tick_params(colors="black", labelsize=11)
            for spine in ax.spines.values():
                spine.set_edgecolor("#cccccc")

            if opcion == "Barras - Peso (N)":
                colores_barras = ["#0077cc","#e74c3c","#2ecc71","#f39c12","#9b59b6","#1abc9c","#e67e22","#3498db"]
                bars = ax.bar(registros, df["peso_N"],
                              color=colores_barras[:len(registros)],
                              edgecolor="white", linewidth=1.2)
                ax.set_title("Peso por Registro (N)", color="black", fontsize=14, fontweight="bold")
                ax.set_xlabel("Registro #", color="black", fontsize=12)
                ax.set_ylabel("Peso (N)", color="black", fontsize=12)
                for bar, val in zip(bars, df["peso_N"]):
                    ax.text(bar.get_x() + bar.get_width()/2,
                            bar.get_height() + max(df["peso_N"]) * 0.01,
                            f"{val:.1f}", ha="center", va="bottom",
                            color="black", fontsize=10, fontweight="bold")

            elif opcion == "Lineas - Factor de Seguridad":
                ax.plot(registros, df["factor_seguridad"],
                        color="#0077cc", marker="o", linewidth=2.5,
                        markersize=8, markerfacecolor="white",
                        markeredgewidth=2, label="Factor de Seguridad")
                ax.fill_between(registros, df["factor_seguridad"], alpha=0.15, color="#0077cc")
                ax.axhline(y=2.0, color="#2ecc71", linestyle="--", linewidth=2, label="Seguro (>=2.0)")
                ax.axhline(y=1.5, color="#f39c12", linestyle="--", linewidth=2, label="Precaucion (1.5-2.0)")
                ax.axhline(y=1.0, color="#e74c3c", linestyle="--", linewidth=2, label="Peligroso (<1.5)")
                ax.set_title("Factor de Seguridad por Registro", color="black", fontsize=14, fontweight="bold")
                ax.set_xlabel("Registro #", color="black", fontsize=12)
                ax.set_ylabel("Factor de Seguridad", color="black", fontsize=12)
                legend = ax.legend(loc="upper right", facecolor="white", edgecolor="#cccccc")
                for text in legend.get_texts():
                    text.set_color("black")

            elif opcion == "Pastel - Estados de Carga":
                conteo = df["estado_carga"].value_counts()
                mapa_colores = {
                    "SEGURO":     "#2ecc71",
                    "PRECAUCION": "#f39c12",
                    "PELIGROSO":  "#e74c3c"
                }
                colores_extra = ["#3498db", "#9b59b6", "#1abc9c"]
                colores = []
                for i, k in enumerate(conteo.index):
                    colores.append(mapa_colores.get(k, colores_extra[i % len(colores_extra)]))
                wedges, texts, autotexts = ax.pie(
                    conteo.values,
                    labels=conteo.index,
                    colors=colores,
                    autopct="%1.1f%%",
                    startangle=140,
                    pctdistance=0.75,
                    wedgeprops={"edgecolor": "white", "linewidth": 2}
                )
                for text in texts:
                    text.set_color("black")
                    text.set_fontsize(12)
                    text.set_fontweight("bold")
                for autotext in autotexts:
                    autotext.set_color("white")
                    autotext.set_fontsize(11)
                    autotext.set_fontweight("bold")
                ax.set_title("Estados de Carga", color="black", fontsize=14, fontweight="bold")

            elif opcion == "Barras dobles - Potencia W vs HP":
                import numpy as np
                x = np.arange(len(registros))
                bars1 = ax.bar(x - 0.2, df["potencia_W"],  width=0.35,
                               color="#0077cc", edgecolor="white", linewidth=1.2, label="Potencia (W)")
                bars2 = ax.bar(x + 0.2, df["potencia_HP"], width=0.35,
                               color="#f8a500", edgecolor="white", linewidth=1.2, label="Potencia (HP)")
                ax.set_xticks(x)
                ax.set_xticklabels([f"Reg. {r}" for r in registros], color="black")
                ax.set_title("Potencia: Watts vs Caballos de Fuerza", color="black", fontsize=14, fontweight="bold")
                ax.set_ylabel("Potencia", color="black", fontsize=12)
                for bar, val in zip(bars1, df["potencia_W"]):
                    ax.text(bar.get_x() + bar.get_width()/2,
                            bar.get_height() + 0.5,
                            f"{val:.1f}W", ha="center", va="bottom", color="black", fontsize=9)
                for bar, val in zip(bars2, df["potencia_HP"]):
                    ax.text(bar.get_x() + bar.get_width()/2,
                            bar.get_height() + 0.001,
                            f"{val:.3f}HP", ha="center", va="bottom", color="black", fontsize=9)
                legend = ax.legend(loc="upper right", facecolor="white", edgecolor="#cccccc")
                for text in legend.get_texts():
                    text.set_color("black")

            plt.tight_layout()
            st.pyplot(fig)

    # ============================================
    # PESTAÑA 4: EXPORTAR
    # ============================================
    with tab4:
        st.subheader("💾 Exportar Historial")
        if len(st.session_state.historial) == 0:
            st.info("No hay registros para exportar.")
        else:
            df = pd.DataFrame(st.session_state.historial)

            st.markdown("### 📊 Descargar CSV")
            csv = df.to_csv(index=False, encoding="utf-8").encode("utf-8")
            st.download_button(
                label="📊 Descargar CSV (Excel)",
                data=csv,
                file_name="historial_montacargas.csv",
                mime="text/csv"
            )

            st.divider()

            st.markdown("### 📝 Descargar TXT")
            lineas = [
                "=" * 50,
                "  REPORTE - SISTEMA MONTACARGAS",
                f"  Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                f"  Total registros: {len(df)}",
                "=" * 50 + "\n"
            ]
            for i, row in df.iterrows():
                lineas.append(f"--- Registro #{i+1} ---")
                for col in df.columns:
                    lineas.append(f"  {col}: {row[col]}")
                lineas.append("-" * 40 + "\n")
            st.download_button(
                label="📝 Descargar TXT",
                data="\n".join(lineas),
                file_name="historial_montacargas.txt",
                mime="text/plain"
            )