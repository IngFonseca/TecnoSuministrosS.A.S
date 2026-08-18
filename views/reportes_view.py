"""
VISTA – Reportes
Responsabilidad: UI de tarjetas para generar PDFs.
Delega generación a ReportesController.
"""
import tkinter as tk
from tkinter import messagebox
from controllers.reportes_controller import ReportesController
from utils.theme import *
import subprocess, sys, os


class ReportesView(tk.Frame):
    def __init__(self, parent, usuario):
        super().__init__(parent, bg=FONDO)
        self.usuario = usuario
        self._build()

    def _build(self):
        tk.Label(self, text="📋 Reportes PDF", font=FONT_TITULO,
                 bg=FONDO, fg=TEXTO_DARK).pack(pady=(24, 4), anchor="w", padx=24)
        tk.Label(self,
                 text="Genera y descarga reportes con encabezado institucional y diseño profesional.",
                 font=FONT_NORMAL, bg=FONDO, fg=TEXTO_MEDIUM).pack(anchor="w", padx=24, pady=(0, 24))

        grid = tk.Frame(self, bg=FONDO)
        grid.pack(padx=24)

        tarjetas = [
            ("🛒", "Reporte de Ventas",
             "Fecha, producto, cantidad,\nprecio unitario y total.",
             self._pdf_ventas, EXITO),
            ("📦", "Reporte de Inventario",
             "Código, nombre, categoría,\nproveedor, cantidad y precio.",
             self._pdf_inventario, AZUL_MEDIO),
            ("📥", "Reporte de Movimientos",
             "Historial de entradas y salidas\nde mercancía en el inventario.",
             self._pdf_movimientos, ADVERTENCIA),
            ("🏭", "Reporte de Proveedores",
             "Listado completo con nombre,\nteléfono, correo y tipo.",
             self._pdf_proveedores, PELIGRO),
        ]
        for i, (icon, titulo, desc, cmd, color) in enumerate(tarjetas):
            row, col = divmod(i, 2)
            card = tk.Frame(grid, bg=PANEL, highlightthickness=1,
                            highlightbackground=BORDE, padx=24, pady=20)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
            grid.columnconfigure(col, weight=1)
            tk.Label(card, text=icon,   font=("Segoe UI", 36), bg=PANEL).pack()
            tk.Label(card, text=titulo, font=FONT_SUBTITULO,   bg=PANEL, fg=TEXTO_DARK).pack(pady=(4, 2))
            tk.Label(card, text=desc,   font=FONT_SMALL,       bg=PANEL, fg=TEXTO_MEDIUM, justify="center").pack(pady=(0, 12))
            tk.Button(card, text="📄 Generar PDF", command=cmd,
                      bg=color, fg="white", font=("Segoe UI", 10, "bold"),
                      relief="flat", cursor="hand2", padx=20, pady=8,
                      activebackground=color, activeforeground="white", bd=0).pack()

    def _generar(self, metodo):
        ok, resultado = metodo(self.usuario)
        if ok:
            messagebox.showinfo("PDF generado", f"Guardado en:\n{resultado}", parent=self)
            _abrir(resultado)
        else:
            messagebox.showinfo("Sin datos", resultado, parent=self)

    def _pdf_ventas(self):      self._generar(ReportesController.pdf_ventas)
    def _pdf_inventario(self):  self._generar(ReportesController.pdf_inventario)
    def _pdf_movimientos(self): self._generar(ReportesController.pdf_movimientos)
    def _pdf_proveedores(self): self._generar(ReportesController.pdf_proveedores)


def _abrir(ruta):
    try:
        if sys.platform == "win32": os.startfile(ruta)
        elif sys.platform == "darwin": subprocess.call(["open", ruta])
        else: subprocess.call(["xdg-open", ruta])
    except Exception: pass
