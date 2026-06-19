# ============================================
# MÓDULO 3: HISTORIAL CON PANDAS Y TREEVIEW
# ============================================

import pandas as pd
import tkinter as tk
from tkinter import ttk

# Columnas que se mostrarán en la tabla
COLUMNAS = [
    "masa_kg", "peso_N", "factor_seguridad",
    "estado_carga", "torque_Nm", "potencia_W",
    "potencia_HP", "estabilidad"
]

ENCABEZADOS = [
    "Masa (kg)", "Peso (N)", "F. Seguridad",
    "Estado", "Torque (Nm)", "Potencia (W)",
    "Potencia (HP)", "Estabilidad"
]

# ---- COLORES ----
BG_PRINCIPAL  = "#1e1e2e"
BG_FRAME      = "#2a2a3e"
COLOR_TEXTO   = "#ffffff"
COLOR_BTN     = "#0077cc"
FUENTE_LABEL  = ("Segoe UI", 11)
FUENTE_TITULO = ("Segoe UI", 13, "bold")
FUENTE_BTN    = ("Segoe UI", 10, "bold")
FUENTE_STATS  = ("Segoe UI", 10)


def crear_historial(parent, historial_compartido):
    """Crea la pestaña de historial con tabla y estadísticas."""

    # ---- FRAME PRINCIPAL ----
    frame = tk.Frame(parent, bg=BG_PRINCIPAL)
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    # ---- TÍTULO ----
    tk.Label(frame, text="📋 Historial de Cálculos",
             font=FUENTE_TITULO, bg=BG_PRINCIPAL,
             fg=COLOR_TEXTO).pack(pady=(0, 10))

    # ---- FRAME TABLA ----
    frame_tabla = tk.Frame(frame, bg=BG_PRINCIPAL)
    frame_tabla.pack(fill="both", expand=True)

    # ---- SCROLLBARS ----
    scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")
    scroll_y.pack(side="right", fill="y")

    scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    # ---- TREEVIEW (TABLA) ----
    tabla = ttk.Treeview(
        frame_tabla,
        columns=COLUMNAS,
        show="headings",
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
        height=10
    )

    # Encabezados y ancho de columnas
    for col, enc in zip(COLUMNAS, ENCABEZADOS):
        tabla.heading(col, text=enc)
        tabla.column(col, width=110, anchor="center")

    tabla.pack(fill="both", expand=True)
    scroll_y.config(command=tabla.yview)
    scroll_x.config(command=tabla.xview)

    # ---- ESTADÍSTICAS ----
    lbl_stats = tk.Label(frame, text="Las estadísticas aparecerán aquí...",
                         font=FUENTE_STATS, bg=BG_FRAME, fg=COLOR_TEXTO,
                         justify="left", padx=15, pady=10, wraplength=700)
    lbl_stats.pack(fill="x", pady=10)

    # ---- FUNCIÓN ACTUALIZAR TABLA ----
    def actualizar_tabla():
        """Limpia y recarga la tabla con los datos del historial."""

        # Limpiar tabla
        for item in tabla.get_children():
            tabla.delete(item)

        if len(historial_compartido) == 0:
            lbl_stats.config(text="No hay registros aún. Realizá un cálculo primero.")
            return

        # Llenar tabla con datos
        for registro in historial_compartido:
            fila = [registro.get(col, "-") for col in COLUMNAS]
            tabla.insert("", "end", values=fila)

        # Calcular estadísticas con Pandas
        df = pd.DataFrame(historial_compartido)

        total     = len(df)
        masa_prom = round(df["masa_kg"].mean(), 2)
        peso_max  = round(df["peso_N"].max(), 2)
        peso_min  = round(df["peso_N"].min(), 2)
        fs_prom   = round(df["factor_seguridad"].mean(), 2)
        fs_min    = round(df["factor_seguridad"].min(), 2)
        pot_prom  = round(df["potencia_W"].mean(), 2)

        stats = (
            f"📊 Total de registros: {total}   |   "
            f"Masa promedio: {masa_prom} kg   |   "
            f"Peso máx: {peso_max} N   |   "
            f"Peso mín: {peso_min} N   |   "
            f"F. Seguridad promedio: {fs_prom}   |   "
            f"F. Seguridad mín: {fs_min}   |   "
            f"Potencia promedio: {pot_prom} W"
        )
        lbl_stats.config(text=stats)

    # ---- BOTÓN ACTUALIZAR ----
    btn_actualizar = tk.Button(
        frame, text="🔄  ACTUALIZAR HISTORIAL",
        font=FUENTE_BTN, bg=COLOR_BTN, fg=COLOR_TEXTO,
        relief="flat", padx=15, pady=7,
        command=actualizar_tabla
    )
    btn_actualizar.pack(pady=8)

    # ---- BOTÓN LIMPIAR HISTORIAL ----
    def limpiar_historial():
        historial_compartido.clear()
        actualizar_tabla()

    btn_limpiar = tk.Button(
        frame, text="🗑️  LIMPIAR HISTORIAL",
        font=FUENTE_BTN, bg="#555577", fg=COLOR_TEXTO,
        relief="flat", padx=15, pady=7,
        command=limpiar_historial
    )
    btn_limpiar.pack(pady=4)

    return frame, actualizar_tabla