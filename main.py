# ============================================
# MÓDULO 6: MAIN - INTEGRACIÓN PRINCIPAL
# ============================================

import tkinter as tk
from tkinter import ttk

from interfaz  import crear_formulario
from historial import crear_historial
from graficas  import crear_graficas
from exportar  import crear_exportar

# ---- COLORES ----
BG_PRINCIPAL = "#1e1e2e"
COLOR_TEXTO  = "#ffffff"

def main():
    """Función principal que lanza la aplicación."""

    historial = []

    # ---- VENTANA PRINCIPAL ----
    ventana = tk.Tk()
    ventana.title("Sistema de Montacargas")
    ventana.geometry("900x700")
    ventana.configure(bg=BG_PRINCIPAL)
    ventana.resizable(True, True)

    # ---- TÍTULO SUPERIOR ----
    tk.Label(ventana,
             text="SISTEMA DE CALCULO DE MONTACARGAS",
             font=("Segoe UI", 15, "bold"),
             bg=BG_PRINCIPAL, fg=COLOR_TEXTO).pack(pady=(15, 5))

    tk.Label(ventana,
             text="Ingenieria Industrial — Proyecto Final",
             font=("Segoe UI", 10),
             bg=BG_PRINCIPAL, fg="#aaaaaa").pack(pady=(0, 10))

    # ---- ESTILO DE PESTAÑAS ----
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TNotebook",
                    background=BG_PRINCIPAL,
                    borderwidth=0)
    style.configure("TNotebook.Tab",
                    background="#2a2a3e",
                    foreground=COLOR_TEXTO,
                    padding=[15, 8],
                    font=("Segoe UI", 10, "bold"))
    style.map("TNotebook.Tab",
              background=[("selected", "#0077cc")],
              foreground=[("selected", COLOR_TEXTO)])

    # ---- NOTEBOOK (PESTAÑAS) ----
    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True, padx=15, pady=10)

    tab1 = tk.Frame(notebook, bg=BG_PRINCIPAL)
    tab2 = tk.Frame(notebook, bg=BG_PRINCIPAL)
    tab3 = tk.Frame(notebook, bg=BG_PRINCIPAL)
    tab4 = tk.Frame(notebook, bg=BG_PRINCIPAL)

    notebook.add(tab1, text="  Calculos  ")
    notebook.add(tab2, text="  Historial  ")
    notebook.add(tab3, text="  Graficas  ")
    notebook.add(tab4, text="  Exportar  ")

    # ---- CONSTRUIR CADA PESTAÑA ----
    crear_formulario(tab1, historial)
    frame_hist, actualizar_hist = crear_historial(tab2, historial)
    crear_graficas(tab3, historial)
    crear_exportar(tab4, historial)

    # ---- ACTUALIZAR HISTORIAL AL CAMBIAR PESTAÑA ----
    def on_tab_change(event):
        if notebook.index("current") == 1:
            actualizar_hist()

    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

    ventana.mainloop()

if __name__ == "__main__":
    main()