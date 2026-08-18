"""
VISTA – Proveedores
Responsabilidad: UI para listar, crear, editar y eliminar proveedores.
Delega lógica a ProveedoresController.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.proveedores_controller import ProveedoresController
from utils.theme import *
import subprocess, sys, os


class ProveedoresView(tk.Frame):
    def __init__(self, parent, usuario):
        super().__init__(parent, bg=FONDO)
        self.usuario = usuario
        self._sel_id = None
        self._build()
        self.cargar()

    def _build(self):
        top = tk.Frame(self, bg=FONDO)
        top.pack(fill="x", padx=20, pady=(16, 8))
        tk.Label(top, text="🏭 Proveedores", font=FONT_TITULO, bg=FONDO, fg=TEXTO_DARK).pack(side="left")
        tk.Button(top, text="➕ Nuevo proveedor", command=self._nuevo,        **BTN_PRIMARY).pack(side="right", padx=4)
        tk.Button(top, text="📄 Exportar PDF",    command=self._exportar_pdf, **BTN_SECONDARY).pack(side="right", padx=4)

        cols = ("ID", "Nombre", "Teléfono", "Correo", "Tipo de producto")
        self.tv = ttk.Treeview(self, columns=cols, show="headings", height=20)
        for c, w in zip(cols, [50, 200, 120, 200, 200]):
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

        acc = tk.Frame(self, bg=FONDO)
        acc.pack(side="right", fill="y", padx=12, pady=8)
        tk.Label(acc, text="Acciones", font=FONT_SUBTITULO, bg=FONDO, fg=TEXTO_DARK).pack(pady=(0, 12))
        tk.Button(acc, text="✏️ Editar",    command=self._editar,   **BTN_WARNING,   width=16).pack(pady=4)
        tk.Button(acc, text="🗑️ Eliminar",  command=self._eliminar, **BTN_DANGER,    width=16).pack(pady=4)
        tk.Button(acc, text="↻ Actualizar", command=self.cargar,
                  bg=AZUL_CLARO, fg=AZUL_MEDIO, font=FONT_SMALL,
                  relief="flat", cursor="hand2", width=16).pack(pady=12)

    def _on_select(self):
        sel = self.tv.selection()
        self._sel_id = int(sel[0]) if sel else None

    def cargar(self):
        self.tv.delete(*self.tv.get_children())
        for i, r in enumerate(ProveedoresController.listar()):
            tag = "par" if i % 2 == 0 else "impar"
            self.tv.insert("", "end", iid=str(r["id"]),
                           values=(r["id"], r["nombre"], r["telefono"] or "–",
                                   r["correo"] or "–", r["tipo_producto"] or "–"),
                           tags=(tag,))
        self.tv.tag_configure("par",  background=TABLA_PAR)
        self.tv.tag_configure("impar", background=TABLA_IMPAR)

    def _nuevo(self):
        ProveedorFormView(self, self.usuario, None, self.cargar)

    def _editar(self):
        if not self._sel_id:
            messagebox.showwarning("Selección", "Selecciona un proveedor.", parent=self); return
        prov = ProveedoresController.get_por_id(self._sel_id)
        if prov:
            ProveedorFormView(self, self.usuario, prov, self.cargar)

    def _eliminar(self):
        if not self._sel_id:
            messagebox.showwarning("Selección", "Selecciona un proveedor.", parent=self); return
        prov = ProveedoresController.get_por_id(self._sel_id)
        if not prov: return
        if messagebox.askyesno("Confirmar", f"¿Eliminar a '{prov['nombre']}'?", parent=self):
            ProveedoresController.eliminar(self._sel_id, prov["nombre"], self.usuario)
            self.cargar()

    def _exportar_pdf(self):
        ruta = ProveedoresController.exportar_pdf(self.usuario)
        messagebox.showinfo("PDF generado", f"Guardado en:\n{ruta}", parent=self)
        _abrir(ruta)


class ProveedorFormView(tk.Toplevel):
    def __init__(self, parent, usuario, proveedor, on_save):
        super().__init__(parent)
        self.usuario   = usuario
        self.proveedor = proveedor
        self.on_save   = on_save
        self.title("Nuevo proveedor" if proveedor is None else "Editar proveedor")
        self.geometry("450x520")
        self.resizable(False, False)
        self.configure(bg=FONDO)
        self.grab_set()
        self._build()

    def _build(self):
        tk.Label(
            self,
            text="Proveedor",
            font=FONT_TITULO,
            bg=FONDO,
            fg=TEXTO_DARK
        ).pack(pady=(20, 12))

        frame = tk.Frame(
            self,
            bg=FONDO
        )
        frame.pack(
            fill="x",
            padx=28
        )

        campos = [
            ("Nombre completo", "e_nombre"),
            ("Teléfono", "e_tel"),
            ("Correo electrónico", "e_correo"),
            ("Tipo de producto que suministra", "e_tipo"),
        ]

        for label, attr in campos:

            tk.Label(
                frame,
                text=label,
                font=FONT_BOLD,
                bg=FONDO,
                fg=TEXTO_DARK,
                anchor="w"
            ).pack(fill="x")

            e = tk.Entry(
                frame,
                font=FONT_NORMAL,
                relief="solid",
                bd=1
            )

            e.pack(
                fill="x",
                pady=(2, 12),
                ipady=6
            )

            setattr(self, attr, e)

        if self.proveedor:
            self.e_nombre.insert(
                0,
                self.proveedor["nombre"] or ""
            )

            self.e_tel.insert(
                0,
                self.proveedor["telefono"] or ""
            )

            self.e_correo.insert(
                0,
                self.proveedor["correo"] or ""
            )

            self.e_tipo.insert(
                0,
                self.proveedor["tipo_producto"] or ""
            )

        self.lbl_err = tk.Label(
            self,
            text="",
            font=FONT_SMALL,
            bg=FONDO,
            fg=PELIGRO
        )

        self.lbl_err.pack(
            pady=(2, 8)
        )

        tk.Button(
            self,
            text="✅ Guardar proveedor",
            command=self._guardar,
            **BTN_PRIMARY
        ).pack(
            pady=(4, 18),
            padx=28,
            fill="x"
        )

    def _guardar(self):
        if self.proveedor is None:
            ok, msg = ProveedoresController.crear(
                self.e_nombre.get(), self.e_tel.get(),
                self.e_correo.get(), self.e_tipo.get(), self.usuario
            )
        else:
            ok, msg = ProveedoresController.editar(
                self.proveedor["id"], self.e_nombre.get(),
                self.e_tel.get(), self.e_correo.get(), self.e_tipo.get(), self.usuario
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
