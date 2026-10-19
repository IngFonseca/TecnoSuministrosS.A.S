"""
VISTA – Inventario
Responsabilidad: UI para productos, categorías y movimientos de stock.
Toda la lógica va a InventarioController.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from controllers.inventario_controller import InventarioController
from utils.theme import *
import subprocess, sys, os


class InventarioView(tk.Frame):
    def __init__(self, parent, usuario):
        super().__init__(parent, bg=FONDO)
        self.usuario = usuario
        self._sel_id = None
        self._build()
        self.cargar()

    def _build(self):
        # Barra superior
        top = tk.Frame(self, bg=FONDO)
        top.pack(fill="x", padx=20, pady=(16, 8))
        tk.Label(top, text="📦 Inventario", font=FONT_TITULO, bg=FONDO, fg=TEXTO_DARK).pack(side="left")
        tk.Button(top, text="➕ Nuevo producto",  command=self._dlg_nuevo,      **BTN_PRIMARY).pack(side="right", padx=4)
        tk.Button(top, text="📄 Exportar PDF",    command=self._exportar_pdf,   **BTN_SECONDARY).pack(side="right", padx=4)
        tk.Button(top, text="📂 Nueva categoría", command=self._nueva_categoria,**BTN_WARNING).pack(side="right", padx=4)

        # Filtros
        f = tk.Frame(self, bg=FONDO)
        f.pack(fill="x", padx=20, pady=4)
        tk.Label(f, text="Buscar:", font=FONT_NORMAL, bg=FONDO).pack(side="left")
        self.var_buscar = tk.StringVar()
        self.var_buscar.trace_add("write", lambda *_: self.cargar())
        tk.Entry(f, textvariable=self.var_buscar, font=FONT_NORMAL,
                 relief="solid", bd=1, width=24).pack(side="left", padx=6, ipady=4)
        tk.Label(f, text="Categoría:", font=FONT_NORMAL, bg=FONDO).pack(side="left", padx=(12, 4))
        self.var_cat = tk.StringVar(value="Todas")
        self.cb_cat = ttk.Combobox(f, textvariable=self.var_cat, state="readonly", width=20)
        self.cb_cat.pack(side="left")
        self.cb_cat.bind("<<ComboboxSelected>>", lambda _: self.cargar())
        self._refrescar_categorias()

        # Tabla
        cols = ("ID", "Código", "Nombre", "Categoría", "Proveedor", "Cantidad", "Precio")
        self.tv = ttk.Treeview(self, columns=cols, show="headings", height=18)
        for c, w in zip(cols, [50, 80, 200, 120, 150, 80, 100]):
            self.tv.heading(c, text=c); self.tv.column(c, width=w, anchor="center")
        self.tv.column("Nombre", anchor="w")

        style = ttk.Style()
        style.configure("Treeview.Heading", background=TABLA_HEAD, foreground="white",
                        font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 9))

        sb = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        self.tv.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=8)
        sb.pack(side="left", fill="y", pady=8)
        self.tv.bind("<<TreeviewSelect>>", lambda _: self._on_select())

        # Panel acciones
        acc = tk.Frame(self, bg=FONDO)
        acc.pack(side="right", fill="y", padx=12, pady=8)
        tk.Label(acc, text="Acciones", font=FONT_SUBTITULO, bg=FONDO, fg=TEXTO_DARK).pack(pady=(0, 12))
        tk.Button(acc, text="✏️ Editar",        command=self._editar,                      **BTN_WARNING,   width=16).pack(pady=4)
        tk.Button(acc, text="🗑️ Eliminar",      command=self._eliminar,                    **BTN_DANGER,    width=16).pack(pady=4)
        tk.Button(acc, text="📥 Entrada stock", command=lambda: self._movimiento("entrada"),**BTN_SUCCESS,   width=16).pack(pady=4)
        tk.Button(acc, text="📤 Salida stock",  command=lambda: self._movimiento("salida"), **BTN_SECONDARY, width=16).pack(pady=4)
        tk.Button(acc, text="↻ Actualizar",    command=self.cargar,
                  bg=AZUL_CLARO, fg=AZUL_MEDIO, font=FONT_SMALL, relief="flat",
                  cursor="hand2", width=16).pack(pady=12)

    def _on_select(self):
        sel = self.tv.selection()
        self._sel_id = int(sel[0]) if sel else None

    def _refrescar_categorias(self):
        cats = InventarioController.get_categorias()
        self.cb_cat["values"] = ["Todas"] + [c["nombre"] for c in cats]

    def cargar(self):
        self.tv.delete(*self.tv.get_children())
        rows = InventarioController.listar(
            buscar=self.var_buscar.get().strip(),
            categoria=self.var_cat.get()
        )
        for i, r in enumerate(rows):
            tag = "par" if i % 2 == 0 else "impar"
            self.tv.insert("", "end", iid=str(r["id"]),
                           values=(r["id"], r["codigo"], r["nombre"],
                                   r["categoria"], r["proveedor"],
                                   r["cantidad"], f"${r['precio']:,.0f}"),
                           tags=(tag, "bajo" if r["cantidad"] <= 5 else ""))
        self.tv.tag_configure("par", background=TABLA_PAR)
        self.tv.tag_configure("impar", background=TABLA_IMPAR)
        self.tv.tag_configure("bajo", foreground=PELIGRO)

    def _dlg_nuevo(self):
        ProductoFormView(self, self.usuario, None, self.cargar)

    def _editar(self):
        if not self._sel_id:
            messagebox.showwarning("Selección", "Selecciona un producto.", parent=self); return
        prod = InventarioController.get_por_id(self._sel_id)
        if prod:
            ProductoFormView(self, self.usuario, prod, self.cargar)

    def _eliminar(self):
        if not self._sel_id:
            messagebox.showwarning("Selección", "Selecciona un producto.", parent=self); return
        prod = InventarioController.get_por_id(self._sel_id)
        if not prod: return
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{prod['nombre']}'?", parent=self):
            InventarioController.eliminar(self._sel_id, prod["nombre"], self.usuario)
            self.cargar()

    def _movimiento(self, tipo):
        if not self._sel_id:
            messagebox.showwarning("Selección", "Selecciona un producto.", parent=self); return
        MovimientoFormView(self, self.usuario, self._sel_id, tipo, self.cargar)

    def _nueva_categoria(self):
        nombre = simpledialog.askstring("Nueva categoría", "Nombre:", parent=self)
        if nombre:
            ok, msg = InventarioController.crear_categoria(nombre, self.usuario)
            if ok:
                self._refrescar_categorias()
                messagebox.showinfo("Éxito", msg, parent=self)
            else:
                messagebox.showerror("Error", msg, parent=self)

    def _exportar_pdf(self):
        ruta = InventarioController.exportar_pdf(self.usuario)
        messagebox.showinfo("PDF generado", f"Guardado en:\n{ruta}", parent=self)
        _abrir(ruta)


class ProductoFormView(tk.Toplevel):
    def __init__(self, parent, usuario, producto, on_save):
        super().__init__(parent)
        self.usuario  = usuario
        self.producto = producto
        self.on_save  = on_save
        self.title("Nuevo producto" if producto is None else "Editar producto")
        self.geometry("420x480")
        self.resizable(False, False)
        self.configure(bg=FONDO)
        self.grab_set()
        self._build()

    def _build(self):
        tk.Label(self, text="Producto", font=FONT_TITULO, bg=FONDO, fg=TEXTO_DARK).pack(pady=(20, 12))
        frame = tk.Frame(self, bg=FONDO)
        frame.pack(fill="x", padx=28)

        cats = InventarioController.get_categorias()
        from models.proveedor_model import ProveedorModel
        provs = ProveedorModel.get_all()
        self._cat_map  = {c["nombre"]: c["id"] for c in cats}
        self._prov_map = {p["nombre"]: p["id"] for p in provs}

        tk.Label(frame, text="Nombre", font=FONT_BOLD, bg=FONDO, anchor="w").pack(fill="x")
        self.e_nombre = tk.Entry(frame, font=FONT_NORMAL, relief="solid", bd=1)
        self.e_nombre.pack(fill="x", pady=(2, 8), ipady=5)

        tk.Label(frame, text="Cantidad", font=FONT_BOLD, bg=FONDO, anchor="w").pack(fill="x")
        self.e_cant = tk.Entry(frame, font=FONT_NORMAL, relief="solid", bd=1)
        self.e_cant.pack(fill="x", pady=(2, 8), ipady=5)

        tk.Label(frame, text="Precio ($)", font=FONT_BOLD, bg=FONDO, anchor="w").pack(fill="x")
        self.e_precio = tk.Entry(frame, font=FONT_NORMAL, relief="solid", bd=1)
        self.e_precio.pack(fill="x", pady=(2, 8), ipady=5)

        tk.Label(frame, text="Categoría", font=FONT_BOLD, bg=FONDO, anchor="w").pack(fill="x")
        self.cb_cat = ttk.Combobox(frame, values=list(self._cat_map.keys()), state="readonly")
        self.cb_cat.pack(fill="x", pady=(2, 8))

        tk.Label(frame, text="Proveedor", font=FONT_BOLD, bg=FONDO, anchor="w").pack(fill="x")
        self.cb_prov = ttk.Combobox(frame, values=["(ninguno)"] + list(self._prov_map.keys()), state="readonly")
        self.cb_prov.pack(fill="x", pady=(2, 8))

        if self.producto:
            self.e_nombre.insert(0, self.producto["nombre"])
            self.e_cant.insert(0,   self.producto["cantidad"])
            self.e_precio.insert(0, self.producto["precio"])
            # Nombres a partir de los mapas ya cargados desde la API
            cat_name  = next((n for n, i in self._cat_map.items()
                              if i == self.producto["categoria_id"]), None)
            prov_name = next((n for n, i in self._prov_map.items()
                              if i == self.producto["proveedor_id"]), None)
            if cat_name:
                self.cb_cat.set(cat_name)
            self.cb_prov.set(prov_name or "(ninguno)")

        self.lbl_err = tk.Label(self, text="", font=FONT_SMALL, bg=FONDO, fg=PELIGRO)
        self.lbl_err.pack()
        tk.Button(self, text="Guardar", command=self._guardar, **BTN_PRIMARY).pack(pady=8, padx=28, fill="x")

    def _guardar(self):
        cat_id  = self._cat_map.get(self.cb_cat.get())
        prov_n  = self.cb_prov.get()
        prov_id = self._prov_map.get(prov_n) if prov_n != "(ninguno)" else None

        if self.producto is None:
            ok, msg = InventarioController.crear(
                self.e_nombre.get(), self.e_cant.get(), self.e_precio.get(),
                cat_id, prov_id, self.usuario
            )
        else:
            ok, msg = InventarioController.editar(
                self.producto["id"], self.e_nombre.get(),
                self.e_cant.get(), self.e_precio.get(),
                cat_id, prov_id, self.usuario
            )
        if ok:
            self.on_save(); self.destroy()
        else:
            self.lbl_err.config(text=msg)


class MovimientoFormView(tk.Toplevel):
    def __init__(self, parent, usuario, producto_id, tipo, on_save):
        super().__init__(parent)
        self.usuario    = usuario
        self.producto_id = producto_id
        self.tipo       = tipo
        self.on_save    = on_save
        self.title(f"{'Entrada' if tipo == 'entrada' else 'Salida'} de stock")
        self.geometry("420x360")
        self.resizable(False, False)
        self.configure(bg=FONDO)
        self.grab_set()
        self._build()

    def _build(self):
        prod = InventarioController.get_por_id(self.producto_id)
        nombre = prod["nombre"] if prod else ""
        stock = prod["cantidad"] if prod else 0
    
        tk.Label(
            self,
            text=f"{'📥 Entrada' if self.tipo == 'entrada' else '📤 Salida'} de stock",
            font=FONT_TITULO,
            bg=FONDO,
            fg=TEXTO_DARK
        ).pack(pady=(20, 4))
    
        tk.Label(
            self,
            text=f"Producto: {nombre}  |  Stock actual: {stock}",
            font=FONT_SMALL,
            bg=FONDO,
            fg=TEXTO_MEDIUM
        ).pack()
    
        frame = tk.Frame(self, bg=FONDO)
        frame.pack(
            padx=28,
            pady=16,
            fill="x"
        )
    
        tk.Label(
            frame,
            text="Cantidad:",
            font=FONT_BOLD,
            bg=FONDO,
            anchor="w"
        ).pack(fill="x")
    
        self.e_cant = tk.Entry(
            frame,
            font=FONT_NORMAL,
            relief="solid",
            bd=1
        )
        self.e_cant.pack(
            fill="x",
            ipady=6,
            pady=(2, 12)
        )
    
        tk.Label(
            frame,
            text="Motivo:",
            font=FONT_BOLD,
            bg=FONDO,
            anchor="w"
        ).pack(fill="x")
    
        self.e_motivo = tk.Entry(
            frame,
            font=FONT_NORMAL,
            relief="solid",
            bd=1
        )
        self.e_motivo.pack(
            fill="x",
            ipady=6,
            pady=(2, 12)
        )
    
        self.lbl_err = tk.Label(
            self,
            text="",
            font=FONT_SMALL,
            bg=FONDO,
            fg=PELIGRO
        )
        self.lbl_err.pack(
            padx=28,
            pady=(0, 5)
        )
    
        # BOTÓN PARA GUARDAR/REGISTRAR
        tk.Button(
            self,
            text="✅ Registrar movimiento",
            command=self._registrar,
            **BTN_SUCCESS
        ).pack(
            pady=(5, 16),
            padx=28,
            fill="x"
        )

    def _registrar(self):
        ok, msg = InventarioController.registrar_movimiento(
            self.producto_id, self.tipo,
            self.e_cant.get(), self.e_motivo.get(), self.usuario
        )
        if ok:
            self.on_save(); self.destroy()
        else:
            self.lbl_err.config(text=msg)


    def _abrir(ruta):
        try:
            if sys.platform == "win32": os.startfile(ruta)
            elif sys.platform == "darwin": subprocess.call(["open", ruta])
            else: subprocess.call(["xdg-open", ruta])
        except Exception: pass
