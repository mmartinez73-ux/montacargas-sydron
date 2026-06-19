# ============================================
# MÓDULO 5: EXPORTAR HISTORIAL A CSV Y TXT
# ============================================

import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

# ---- COLORES Y FUENTES ----
BG_PRINCIPAL  = "#1e1e2e"
BG_FRAME      = "#2a2a3e"
COLOR_TEXTO   = "#ffffff"
COLOR_BTN     = "#0077cc"
FUENTE_TITULO = ("Segoe UI", 13, "bold")
FUENTE_LABEL  = ("Segoe UI", 11)
FUENTE_BTN    = ("Segoe UI", 10, "bold")


def exportar_csv(historial):
    """Exporta el historial a un archivo CSV compatible con Excel."""
    if len(historial) == 0:
        messagebox.showwarning("Sin datos", "No hay registros para exportar.")
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Archivo CSV", "*.csv")],
        title="Guardar historial como CSV",
        initialfile=f"historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    if not ruta:
        return  # Usuario canceló

    try:
        df = pd.DataFrame(historial)
        df.to_csv(ruta, index=False, encoding="utf-8-sig")
        messagebox.showinfo("Exportado", f"CSV guardado exitosamente en:\n{ruta}")
    except Exception as e:
        messagebox.showerror("Error al exportar", str(e))


def exportar_txt(historial):
    """Exporta el historial a un archivo TXT formateado con fecha y hora."""
    if len(historial) == 0:
        messagebox.showwarning("Sin datos", "No hay registros para exportar.")
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivo de texto", "*.txt")],
        title="Guardar historial como TXT",
        initialfile=f"historial_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    if not ruta:
        return  # Usuario canceló

    try:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("=" * 50 + "\n")
            f.write("  REPORTE DE HISTORIAL - SISTEMA MONTACARGAS\n")
            f.write(f"  Fecha de exportacion: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"  Total de registros: {len(historial)}\n")
            f.write("=" * 50 + "\n\n")

            for i, registro in enumerate(historial, 1):
                f.write(f"--- Registro #{i} ---\n")
                f.write(f"  Masa de la carga   : {registro.get('masa_kg', '-')} kg\n")
                f.write(f"  Peso               : {registro.get('peso_N', '-')} N\n")
                f.write(f"  Factor de Seguridad: {registro.get('factor_seguridad', '-')}\n")
                f.write(f"  Estado de carga    : {registro.get('estado_carga', '-')}\n")
                f.write(f"  Torque             : {registro.get('torque_Nm', '-')} Nm\n")
                f.write(f"  Potencia           : {registro.get('potencia_W', '-')} W\n")
                f.write(f"  Potencia           : {registro.get('potencia_HP', '-')} HP\n")
                f.write(f"  Estabilidad        : {registro.get('estabilidad', '-')}\n")
                f.write("-" * 40 + "\n\n")

        messagebox.showinfo("Exportado", f"TXT guardado exitosamente en:\n{ruta}")
    except Exception as e:
        messagebox.showerror("Error al exportar", str(e))


def crear_exportar(parent, historial_compartido):
    """Crea la pestaña de exportacion con botones CSV y TXT."""

    frame = tk.Frame(parent, bg=BG_PRINCIPAL)
    frame.pack(fill="both", expand=True, padx=15, pady=15)

    tk.Label(frame, text="💾 Exportar Historial",
             font=FUENTE_TITULO, bg=BG_PRINCIPAL,
             fg=COLOR_TEXTO).pack(pady=(0, 30))

    tk.Label(frame,
             text="Guarda todos los cálculos realizados en un archivo externo.",
             font=FUENTE_LABEL, bg=BG_PRINCIPAL,
             fg=COLOR_TEXTO).pack(pady=(0, 30))

    # ---- BOTÓN CSV ----
    btn_csv = tk.Button(
        frame, text="📄  EXPORTAR A CSV  (Excel)",
        font=FUENTE_BTN, bg=COLOR_BTN, fg=COLOR_TEXTO,
        relief="flat", padx=20, pady=12, width=30,
        command=lambda: exportar_csv(historial_compartido)
    )
    btn_csv.pack(pady=10)

    # ---- BOTÓN TXT ----
    btn_txt = tk.Button(
        frame, text="📝  EXPORTAR A TXT",
        font=FUENTE_BTN, bg="#555577", fg=COLOR_TEXTO,
        relief="flat", padx=20, pady=12, width=30,
        command=lambda: exportar_txt(historial_compartido)
    )
    btn_txt.pack(pady=10)

    # ---- INFO ----
    tk.Label(frame,
             text="Los archivos se guardan donde vos elijas.",
             font=("Segoe UI", 9), bg=BG_PRINCIPAL,
             fg="#aaaaaa").pack(pady=(20, 0))

    return frame