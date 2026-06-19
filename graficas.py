# ============================================
# MÓDULO 4: GRÁFICAS CON MATPLOTLIB
# ============================================

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---- COLORES ----
BG_PRINCIPAL  = "#1e1e2e"
COLOR_TEXTO   = "#ffffff"
BG_GRAFICA    = "#2a2a3e"
FUENTE_TITULO = ("Segoe UI", 13, "bold")
FUENTE_BTN    = ("Segoe UI", 10, "bold")
COLOR_BTN     = "#0077cc"


def crear_graficas(parent, historial_compartido):
    """Crea la pestaña de gráficas con 4 tipos de visualización."""

    # ---- FRAME PRINCIPAL ----
    frame = tk.Frame(parent, bg=BG_PRINCIPAL)
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    tk.Label(frame, text="📊 Gráficas del Montacargas",
             font=FUENTE_TITULO, bg=BG_PRINCIPAL,
             fg=COLOR_TEXTO).pack(pady=(0, 10))

    # ---- SELECTOR DE GRÁFICA ----
    frame_selector = tk.Frame(frame, bg=BG_PRINCIPAL)
    frame_selector.pack()

    tk.Label(frame_selector, text="Seleccionar gráfica:",
             font=("Segoe UI", 10), bg=BG_PRINCIPAL,
             fg=COLOR_TEXTO).pack(side="left", padx=5)

    opciones = [
        "Barras - Peso (N)",
        "Líneas - Factor de Seguridad",
        "Pastel - Estados de Carga",
        "Barras dobles - Potencia W vs HP"
    ]

    combo = ttk.Combobox(frame_selector, values=opciones,
                         state="readonly", width=35)
    combo.current(0)
    combo.pack(side="left", padx=5)

    # ---- ÁREA DE LA GRÁFICA ----
    frame_canvas = tk.Frame(frame, bg=BG_GRAFICA)
    frame_canvas.pack(fill="both", expand=True, pady=10)

    canvas_widget = [None]

    # ---- FUNCIÓN GRAFICAR ----
    def graficar():
        if len(historial_compartido) == 0:
            return

        seleccion = combo.get()

        # Limpiar canvas anterior
        if canvas_widget[0]:
            canvas_widget[0].get_tk_widget().destroy()

        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor(BG_GRAFICA)
        ax.set_facecolor(BG_GRAFICA)
        ax.tick_params(colors=COLOR_TEXTO)
        ax.xaxis.label.set_color(COLOR_TEXTO)
        ax.yaxis.label.set_color(COLOR_TEXTO)
        ax.title.set_color(COLOR_TEXTO)
        for spine in ax.spines.values():
            spine.set_edgecolor(COLOR_TEXTO)

        registros = list(range(1, len(historial_compartido) + 1))

        # ---- GRÁFICA 1: BARRAS DE PESO ----
        if seleccion == opciones[0]:
            pesos = [r["peso_N"] for r in historial_compartido]
            barras = ax.bar(registros, pesos, color="#f8a500", width=0.5)
            ax.set_title("Peso por Registro (N)")
            ax.set_xlabel("Registro")
            ax.set_ylabel("Peso (N)")
            for bar, val in zip(barras, pesos):
                ax.text(bar.get_x() + bar.get_width()/2,
                        bar.get_height() + 50,
                        str(val), ha="center",
                        color=COLOR_TEXTO, fontsize=9)

        # ---- GRÁFICA 2: LÍNEA FACTOR DE SEGURIDAD ----
        elif seleccion == opciones[1]:
            fs = [r["factor_seguridad"] for r in historial_compartido]
            ax.plot(registros, fs, color="#00aaff",
                    marker="o", linewidth=2, label="Factor Seguridad")
            ax.axhline(y=2.0, color="green", linestyle="--",
                       linewidth=1.5, label="Seguro (2.0)")
            ax.axhline(y=1.5, color="orange", linestyle="--",
                       linewidth=1.5, label="Precaución (1.5)")
            ax.set_title("Factor de Seguridad por Registro")
            ax.set_xlabel("Registro")
            ax.set_ylabel("Factor de Seguridad")
            legend = ax.legend()
            for text in legend.get_texts():
                text.set_color(COLOR_TEXTO)
            legend.get_frame().set_facecolor(BG_GRAFICA)

        # ---- GRÁFICA 3: PASTEL ESTADOS ----
        elif seleccion == opciones[2]:
            estados = [r["estado_carga"] for r in historial_compartido]
            conteo = {}
            for e in estados:
                clave = e.replace("✅ ", "").replace("⚠️ ", "").replace("🚨 ", "")
                conteo[clave] = conteo.get(clave, 0) + 1

            colores_mapa = {
                "SEGURO": "#2ecc71",
                "PRECAUCIÓN": "#f39c12",
                "PELIGROSO": "#e74c3c"
            }
            colores = [colores_mapa.get(k, "#aaaaaa") for k in conteo.keys()]
            ax.pie(conteo.values(), labels=conteo.keys(),
                   colors=colores, autopct="%1.1f%%",
                   textprops={"color": COLOR_TEXTO})
            ax.set_title("Distribución de Estados de Carga")

        # ---- GRÁFICA 4: BARRAS DOBLES POTENCIA ----
        elif seleccion == opciones[3]:
            import numpy as np
            pot_w  = [r["potencia_W"] for r in historial_compartido]
            pot_hp = [r["potencia_HP"] for r in historial_compartido]
            x = np.arange(len(registros))
            ax.bar(x - 0.2, pot_w,  width=0.35,
                   color="#0077cc", label="Potencia (W)")
            ax.bar(x + 0.2, pot_hp, width=0.35,
                   color="#f8a500", label="Potencia (HP)")
            ax.set_xticks(x)
            ax.set_xticklabels([f"R{r}" for r in registros])
            ax.set_title("Potencia W vs HP por Registro")
            ax.set_xlabel("Registro")
            ax.set_ylabel("Valor")
            legend = ax.legend()
            for text in legend.get_texts():
                text.set_color(COLOR_TEXTO)
            legend.get_frame().set_facecolor(BG_GRAFICA)

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas_widget[0] = canvas

    # ---- BOTÓN GRAFICAR ----
    btn_graficar = tk.Button(
        frame, text="📈  GENERAR GRÁFICA",
        font=FUENTE_BTN, bg=COLOR_BTN, fg=COLOR_TEXTO,
        relief="flat", padx=15, pady=7,
        command=graficar
    )
    btn_graficar.pack(pady=8)

    return frame