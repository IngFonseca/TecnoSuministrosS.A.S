"""
VISTA – Dashboard
Responsabilidad: mostrar métricas y últimas ventas. Consulta datos al DashboardController.
"""
import tkinter as tk
from tkinter import ttk
from controllers.dashboard_controller import DashboardController
from utils.theme import *


class DashboardView(tk.Frame):
    def __init__(self, parent, usuario):
        super().__init__(parent, bg=FONDO)
        self.usuario = usuario
        self._build()

    def _build(self):
        # Encabezado
        hdr = tk.Frame(self, bg=FONDO)
        hdr.pack(fill="x", padx=20, pady=(20, 8))
        tk.Label(hdr, text=f"Bienvenido, {self.usuario['nombre_completo']}",
                 font=FONT_TITULO, bg=FONDO, fg=TEXTO_DARK).pack(side="left")
        rol_color = ROLES_COLORES.get(self.usuario.get("rol"), "#94a3b8")
        tk.Label(hdr, text=f"  {self.usuario['rol'].upper()}",
                 font=("Segoe UI", 9, "bold"), bg=rol_color, fg="white",
                 padx=8, pady=3).pack(side="left", padx=8)
        tk.Button(hdr, text="↻ Actualizar", command=self.refresh,
                  bg=AZUL_CLARO, fg=AZUL_MEDIO, font=FONT_SMALL,
                  relief="flat", cursor="hand2").pack(side="right")

        # Tarea del rol
        tarea = ROLES_TAREAS.get(self.usuario.get("rol"), "")
        if tarea:
            tf = tk.Frame(self, bg=AZUL_CLARO, pady=6)
            tf.pack(fill="x", padx=20, pady=(0, 12))
            tk.Label(tf, text=f"Tu tarea: {tarea}", font=FONT_SMALL,
                     bg=AZUL_CLARO, fg=AZUL_OSCURO, wraplength=900, justify="left").pack(padx=12)

        # Tarjetas de métricas
        self._cards_frame = tk.Frame(self, bg=FONDO)
        self._cards_frame.pack(fill="x", padx=20, pady=8)
        self._render_metricas()

        # Últimas ventas
        tk.Label(self, text="Últimas 10 ventas", font=FONT_SUBTITULO,
                 bg=FONDO, fg=TEXTO_DARK).pack(anchor="w", padx=20, pady=(16, 4))
        self._tabla_frame = tk.Frame(self, bg=FONDO)
        self._tabla_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        self._render_ventas()

    def _render_metricas(self):
        for w in self._cards_frame.winfo_children():
            w.destroy()
        data = DashboardController.get_metricas()
        items = [
            ("📦", "Total productos",   data["total_productos"],   AZUL_MEDIO),
            ("🛒", "Ventas hoy",        data["ventas_hoy"],        EXITO),
            ("⚠️", "Stock bajo (≤5)",   data["stock_bajo"],        PELIGRO),
            ("🏭", "Proveedores",       data["total_proveedores"], ADVERTENCIA),
        ]
        for i, (icon, label, valor, color) in enumerate(items):
            card = tk.Frame(self._cards_frame, bg=PANEL,
                            highlightthickness=1, highlightbackground=BORDE)
            card.grid(row=0, column=i, padx=8, pady=4, sticky="ew", ipadx=16, ipady=12)
            self._cards_frame.columnconfigure(i, weight=1)
            tk.Label(card, text=icon, font=("Segoe UI", 22), bg=PANEL).pack()
            tk.Label(card, text=str(valor), font=("Segoe UI", 28, "bold"), bg=PANEL, fg=color).pack()
            tk.Label(card, text=label, font=FONT_SMALL, bg=PANEL, fg=TEXTO_MEDIUM).pack()

    def _render_ventas(self):
        for w in self._tabla_frame.winfo_children():
            w.destroy()

        cols = ("Fecha", "Producto", "Cantidad", "P. Unitario", "Descuento", "Total")

        tv = ttk.Treeview(
            self._tabla_frame,
            columns=cols,
            show="headings",
            height=10
        )

        # Encabezados
        for c, w in zip(cols, [140, 220, 80, 100, 90, 100]):
            tv.heading(
                c,
                text=c,
                anchor="center"
            )
            tv.column(
                c,
                width=w,
                anchor="center"
            )

        style = ttk.Style()
        style.configure(
            "Treeview",
            rowheight=24,
            font=("Segoe UI", 9)
        )

        ventas = DashboardController.get_ultimas_ventas()

        for i, v in enumerate(ventas):

            # Fecha
            fecha = (
                v["fecha"].strftime("%d/%m/%Y %H:%M")
                if hasattr(v["fecha"], "strftime")
                else str(v["fecha"])
            )

            # Producto
            nombre_producto = v.get("nombre_producto")

            if not nombre_producto or str(nombre_producto).lower() == "none":
                nombre_producto = "Venta histórica"

            # Cantidad
            cantidad = v.get("cantidad", 0)

            # Precio unitario
            precio_unitario = v.get("precio_unitario")

            if precio_unitario is None or float(precio_unitario) == 0:
                precio_texto = "N/D"
            else:
                precio_texto = f"${float(precio_unitario):,.0f}"

            # Descuento
            descuento = v.get("descuento")

            if descuento is None:
                descuento_texto = "N/D"
            else:
                descuento_texto = f"{float(descuento):.2f}%"

            # Total
            total = v.get("total", 0)

            if total is None:
                total = 0

            total_texto = f"${float(total):,.0f}"

            tv.insert(
                "",
                "end",
                values=(
                    fecha,
                    nombre_producto,
                    cantidad,
                    precio_texto,
                    descuento_texto,
                    total_texto
                ),
                tags=("par" if i % 2 == 0 else "impar",)
            )

        # Colores alternos de filas
        tv.tag_configure(
            "par",
            background=TABLA_PAR,
            foreground="#000000"
        )
    
        tv.tag_configure(
            "impar",
            background=TABLA_IMPAR,
            foreground="#000000"
        )
    
        # Scroll
        sb = ttk.Scrollbar(
            self._tabla_frame,
            orient="vertical",
            command=tv.yview
        )
    
        tv.configure(
            yscrollcommand=sb.set
        )
    
        tv.pack(
            side="left",
            fill="both",
            expand=True
        )
    
        sb.pack(
            side="right",
            fill="y"
        )
    
    def refresh(self):
        self._render_metricas()
        self._render_ventas()
    