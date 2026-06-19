# ============================================
# MÓDULO 2: INTERFAZ GRÁFICA CON TKINTER
# ============================================

import tkinter as tk
from tkinter import messagebox
from calculos import resumen_calculo

BG_PRINCIPAL    = "#1e1e2e"
BG_FRAME        = "#2a2a3e"
COLOR_TEXTO     = "#ffffff"
COLOR_ENTRY     = "#3a3a5c"
COLOR_BTN       = "#0077cc"
FUENTE_LABEL    = ("Segoe UI", 11)
FUENTE_TITULO   = ("Segoe UI", 14, "bold")
FUENTE_BTN      = ("Segoe UI", 11, "bold")

historial = []

def crear_formulario(parent, historial_compartido):
    """Construye el formulario principal de entrada de datos."""

    global historial
    historial = historial_compartido

    frame = tk.Frame(parent, bg=BG_PRINCIPAL)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(frame, text="Sistema de Calculo de Montacargas",
             font=FUENTE_TITULO, bg=BG_PRINCIPAL, fg=COLOR_TEXTO).grid(
             row=0, column=0, columnspan=2, pady=(0, 20))

    campos = [
        ("Masa de la carga (kg):", "masa_kg"),
        ("Carga maxima permitida (kg):", "carga_maxima"),
        ("Distancia al centro de carga (m):", "distancia_m"),
        ("Altura de elevacion (m):", "altura_m"),
        ("Tiempo de elevacion (s):", "tiempo_s"),
        ("Peso del contrapeso (kg):", "peso_contrapeso"),
        ("Distancia del contrapeso (m):", "dist_contrapeso"),
    ]

    entradas = {}

    for i, (etiqueta, clave) in enumerate(campos):
        tk.Label(frame, text=etiqueta, font=FUENTE_LABEL,
                 bg=BG_PRINCIPAL, fg=COLOR_TEXTO, anchor="w").grid(
                 row=i+1, column=0, sticky="w", pady=6, padx=(0, 15))

        entrada = tk.Entry(frame, font=FUENTE_LABEL, bg=COLOR_ENTRY,
                           fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                           relief="flat", width=20)
        entrada.grid(row=i+1, column=1, pady=6, ipady=5)
        entradas[clave] = entrada

    frame_btns = tk.Frame(frame, bg=BG_PRINCIPAL)
    frame_btns.grid(row=len(campos)+1, column=0, columnspan=2, pady=20)

    frame_resultado = tk.Frame(frame, bg=BG_FRAME)
    frame_resultado.grid(row=len(campos)+2, column=0, columnspan=2,
                         sticky="ew", padx=5, pady=5)

    lbl_resultado = tk.Label(frame_resultado,
                             text="Los resultados apareceran aqui...",
                             font=FUENTE_LABEL, bg=BG_FRAME, fg=COLOR_TEXTO,
                             justify="left", wraplength=500, padx=15, pady=15)
    lbl_resultado.pack()

    def on_calcular():
        try:
            valores = {k: float(v.get()) for k, v in entradas.items()}
            resultado = resumen_calculo(**valores)
            historial.append(resultado)
            texto = (
                f"Peso: {resultado['peso_N']} N\n"
                f"Factor de Seguridad: {resultado['factor_seguridad']}\n"
                f"Estado: {resultado['estado_carga']}\n"
                f"Torque: {resultado['torque_Nm']} Nm\n"
                f"Potencia: {resultado['potencia_W']} W  |  {resultado['potencia_HP']} HP\n"
                f"Estabilidad: {resultado['estabilidad']}"
            )
            lbl_resultado.config(text=texto)
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

    def on_limpiar():
        for entrada in entradas.values():
            entrada.delete(0, tk.END)
        lbl_resultado.config(text="Los resultados apareceran aqui...")

    tk.Button(frame_btns, text="CALCULAR",
              font=FUENTE_BTN, bg=COLOR_BTN, fg=COLOR_TEXTO,
              relief="flat", padx=20, pady=8,
              command=on_calcular).pack(side="left", padx=10)

    tk.Button(frame_btns, text="LIMPIAR",
              font=FUENTE_BTN, bg="#555577", fg=COLOR_TEXTO,
              relief="flat", padx=20, pady=8,
              command=on_limpiar).pack(side="left", padx=10)

    return frame