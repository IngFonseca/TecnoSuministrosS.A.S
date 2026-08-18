"""
VISTA – Ventas
Responsabilidad: UI del carrito, selección de productos e historial.
Toda la lógica va a VentasController / CarritoController.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.ventas_controller import CarritoController, VentasController
from utils.theme import *
import subprocess, sys, os


class VentasView(tk.Frame):
    def __init__(self, parent, usuario):
        super().__init__(parent, bg=FONDO)
        self.usuario   = usuario
        self.carrito   = CarritoController()
        self._prods    = []
        self._build()
        self._cargar_historial()

    # ── Layout principal ──────────────────────────────────────────────────────

    def _build(self):
        tk.Label(self, text="🛒 Ventas", font=FONT_TITULO,
                 bg=FONDO, fg=TEXTO_DARK).pack(anchor="w", padx=20, pady=(16, 4))

        body = tk.Frame(self, bg=FONDO)
        body.pack(fill="both", expand=True, padx=20, pady=8)

        # Panel izquierdo
        left = tk.Frame(body, bg=FONDO)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self._build_selector(left)
        self._build_carrito(left)
        self._build_totales(left)

        # Panel derecho: historial
        right = tk.Frame(body, bg=FONDO, width=380)
        right.pack(side="right", fill="both")
        right.pack_propagate(False)
        self._build_historial(right)

    def _build_selector(self, parent):
        sel = tk.LabelFrame(parent, text="Agregar producto al carrito",
                            font=FONT_BOLD, bg=FONDO, fg=TEXTO_DARK, padx=8, pady=8)
        sel.pack(fill="x")

        r1 = tk.Frame(sel, bg=FONDO); r1.pack(fill="x", pady=2)
        tk.Label(r1, text="Categoría:", font=FONT_NORMAL, bg=FONDO).pack(side="left")
        self.var_cat = tk.StringVar(value="Todas")
        from controllers.inventario_controller import InventarioController
        cats = ["Todas"] + [c["nombre"] for c in InventarioController.get_categorias()]
        cb = ttk.Combobox(r1, textvariable=self.var_cat, values=cats, state="readonly", width=20)
        cb.pack(side="left", padx=6)
        cb.bind("<<ComboboxSelected>>", lambda _: self._refrescar_productos())

        r2 = tk.Frame(sel, bg=FONDO); r2.pack(fill="x", pady=4)
        tk.Label(r2, text="Producto:", font=FONT_NORMAL, bg=FONDO).pack(side="left")
        self.var_prod = tk.StringVar()
        self.cb_prod  = ttk.Combobox(r2, textvariable=self.var_prod, state="readonly", width=34)
        self.cb_prod.pack(side="left", padx=6)
        self._refrescar_productos()

        r3 = tk.Frame(sel, bg=FONDO); r3.pack(fill="x", pady=4)
        tk.Label(r3, text="Cantidad:", font=FONT_NORMAL, bg=FONDO).pack(side="left")
        self.e_cant = tk.Entry(r3, font=FONT_NORMAL, relief="solid", bd=1, width=8)
        self.e_cant.insert(0, "1")
        self.e_cant.pack(side="left", padx=6, ipady=4)
        tk.Button(r3, text="➕ Agregar", command=self._agregar, **BTN_PRIMARY).pack(side="left", padx=8)

    def _build_carrito(self, parent):
        cf = tk.LabelFrame(parent, text="Carrito",
                           font=FONT_BOLD, bg=FONDO, fg=TEXTO_DARK, padx=8, pady=8)
        cf.pack(fill="both", expand=True, pady=8)

        cols = ("Producto", "Cant.", "P. Unit.", "Subtotal")
        self.tv_carrito = ttk.Treeview(cf, columns=cols, show="headings", height=7)
        for c, w in zip(cols, [230, 60, 100, 100]):
            self.tv_carrito.heading(c, text=c)
            self.tv_carrito.column(c, width=w, anchor="center")
        self.tv_carrito.column("Producto", anchor="w")
        self.tv_carrito.pack(fill="both", expand=True)

        br = tk.Frame(cf, bg=FONDO); br.pack(fill="x", pady=4)
        tk.Button(br, text="🗑 Quitar seleccionado", command=self._quitar, **BTN_DANGER).pack(side="left")
        tk.Button(br, text="🗑 Vaciar", command=self._vaciar, **BTN_SECONDARY).pack(side="left", padx=8)

    def _build_totales(self, parent):
        tf = tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=BORDE)
        tf.pack(fill="x", pady=4)
        etiquetas = [
            ("Subtotal:",          "lbl_sub",   AZUL_MEDIO),
            ("Descuento (vol.):",  "lbl_desc",  ADVERTENCIA),
            ("IVA 19%:",           "lbl_iva",   TEXTO_MEDIUM),
            ("TOTAL:",             "lbl_total", EXITO),
        ]
        for label, attr, color in etiquetas:
            r = tk.Frame(tf, bg=PANEL); r.pack(fill="x", padx=12, pady=2)
            tk.Label(r, text=label, font=FONT_BOLD, bg=PANEL, fg=TEXTO_DARK).pack(side="left")
            lbl = tk.Label(r, text="$0", font=FONT_BOLD, bg=PANEL, fg=color)
            lbl.pack(side="right")
            setattr(self, attr, lbl)

        tk.Button(parent, text="✅ Finalizar venta", command=self._finalizar, **BTN_SUCCESS).pack(fill="x", pady=8)

    def _build_historial(self, parent):
        hdr = tk.Frame(parent, bg=FONDO); hdr.pack(fill="x")
        tk.Label(hdr, text="Historial de ventas", font=FONT_SUBTITULO,
                 bg=FONDO, fg=TEXTO_DARK).pack(side="left")
        tk.Button(hdr, text="📄 PDF", command=self._exportar_pdf, **BTN_SECONDARY).pack(side="right")

        cols = ("Fecha", "Producto", "Cant.", "Total")
        self.tv_hist = ttk.Treeview(parent, columns=cols, show="headings", height=22)
        for c, w in zip(cols, [120, 160, 50, 90]):
            self.tv_hist.heading(c, text=c)
            self.tv_hist.column(c, width=w, anchor="center")
        sb = ttk.Scrollbar(parent, orient="vertical", command=self.tv_hist.yview)
        self.tv_hist.configure(yscrollcommand=sb.set)
        self.tv_hist.pack(side="left", fill="both", expand=True, pady=4)
        sb.pack(side="right", fill="y", pady=4)

    # ── Acciones ──────────────────────────────────────────────────────────────

    def _refrescar_productos(self):
        self._prods = VentasController.get_productos_disponibles(self.var_cat.get())
        self.cb_prod["values"] = [f"{p['nombre']}  (${p['precio']:,.0f})" for p in self._prods]

    def _agregar(self):
        idx = self.cb_prod.current()
        if idx < 0:
            messagebox.showwarning("Selección", "Selecciona un producto.", parent=self); return
        try:
            cant = int(self.e_cant.get())
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.", parent=self); return

        ok, msg = self.carrito.agregar(self._prods[idx], cant)
        if not ok:
            messagebox.showerror("Stock", msg, parent=self); return
        self._render_carrito()

    def _render_carrito(self):
        self.tv_carrito.delete(*self.tv_carrito.get_children())
        for item in self.carrito.items:
            sub = item["precio"] * item["cantidad"]
            self.tv_carrito.insert("", "end",
                values=(item["nombre"], item["cantidad"],
                        f"${item['precio']:,.0f}", f"${sub:,.0f}"))
        t = self.carrito.calcular_totales()
        self.lbl_sub.config(text=f"${t['subtotal']:,.0f}")
        self.lbl_desc.config(text=f"-${t['desc_monto']:,.0f} ({int(t['desc_pct'])}%)")
        self.lbl_iva.config(text=f"${t['iva_monto']:,.0f}")
        self.lbl_total.config(text=f"${t['total']:,.0f}")

    def _quitar(self):
        sel = self.tv_carrito.selection()
        if not sel: return
        self.carrito.quitar(self.tv_carrito.index(sel[0]))
        self._render_carrito()

    def _vaciar(self):
        self.carrito.vaciar()
        self._render_carrito()

    def _finalizar(self):
        if self.carrito.esta_vacio():
            messagebox.showwarning("Carrito", "El carrito está vacío.", parent=self); return
        t = self.carrito.calcular_totales()
        msg = (f"Subtotal:   ${t['subtotal']:,.0f}\n"
               f"Descuento:  {int(t['desc_pct'])}%\n"
               f"IVA 19%:    ${t['iva_monto']:,.0f}\n\n"
               f"TOTAL:      ${t['total']:,.0f}\n\n¿Confirmar venta?")
        if not messagebox.askyesno("Confirmar venta", msg, parent=self): return

        ok, msg_res, total = self.carrito.finalizar(self.usuario)
        if ok:
            self._render_carrito()
            self._cargar_historial()
            self._refrescar_productos()
            messagebox.showinfo("Venta registrada", f"✅ {msg_res}\nTotal: ${total:,.0f}", parent=self)
        else:
            messagebox.showerror("Error", msg_res, parent=self)

    def _cargar_historial(self):
        self.tv_hist.delete(*self.tv_hist.get_children())
        rows = VentasController.get_historial(limite=100)
        for i, r in enumerate(rows):
            fecha = r["fecha"].strftime("%d/%m %H:%M") if hasattr(r["fecha"], "strftime") else str(r["fecha"])
            tag = "par" if i % 2 == 0 else "impar"
            self.tv_hist.insert("", "end",
                values=(fecha, r["nombre_producto"], r["cantidad"], f"${r['total']:,.0f}"),
                tags=(tag,))
        self.tv_hist.tag_configure("par",  background=TABLA_PAR)
        self.tv_hist.tag_configure("impar", background=TABLA_IMPAR)

    def _exportar_pdf(self):
        ruta = VentasController.exportar_pdf(self.usuario)
        messagebox.showinfo("PDF generado", f"Guardado en:\n{ruta}", parent=self)
        _abrir(ruta)


def _abrir(ruta):
    try:
        if sys.platform == "win32": os.startfile(ruta)
        elif sys.platform == "darwin": subprocess.call(["open", ruta])
        else: subprocess.call(["xdg-open", ruta])
    except Exception: pass
