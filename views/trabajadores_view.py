"""
VISTA – Trabajadores
Responsabilidad: UI para gestión de usuarios.
Solo el gerente puede asignar roles (controlado en TrabajadoresController).
"""
import tkinter as tk
from tkinter import ttk, messagebox
from controllers.trabajadores_controller import TrabajadoresController, ROLES
from utils.theme import *


class TrabajadoresView(tk.Frame):
    def __init__(self, parent, usuario):
        super().__init__(parent, bg=FONDO)
        self.usuario     = usuario
        self.es_gerente  = usuario["rol"] == "gerente"
        self._sel_id     = None
        self._build()
        self.cargar()

    def _build(self):
        top = tk.Frame(self, bg=FONDO)
        top.pack(fill="x", padx=20, pady=(16, 8))
        tk.Label(top, text="👥 Trabajadores", font=FONT_TITULO, bg=FONDO, fg=TEXTO_DARK).pack(side="left")
        if self.usuario["rol"] in ("gerente", "administrador"):
            tk.Button(top, text="➕ Nuevo usuario", command=self._nuevo, **BTN_PRIMARY).pack(side="right", padx=4)

        cols = ("ID", "Nombre completo", "Usuario", "Correo", "Rol", "Activo")
        self.tv = ttk.Treeview(self, columns=cols, show="headings", height=20)
        for c, w in zip(cols, [50, 200, 120, 200, 120, 60]):
            self.tv.heading(c, text=c); self.tv.column(c, width=w, anchor="center")
        self.tv.column("Nombre completo", anchor="w")

        style = ttk.Style()
        style.configure("Treeview.Heading", background=TABLA_HEAD, foreground="white",
                        font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 9))

        sb = ttk.Scrollbar(self, orient="vertical", command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        self.tv.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=8)
        sb.pack(side="left", fill="y", pady=8)
        self.tv.bind("<<TreeviewSelect>>", lambda _: self._on_select())

        # Panel derecho
        acc = tk.Frame(self, bg=FONDO, width=210)
        acc.pack(side="right", fill="y", padx=12, pady=8)
        acc.pack_propagate(False)
        tk.Label(acc, text="Acciones", font=FONT_SUBTITULO, bg=FONDO, fg=TEXTO_DARK).pack(pady=(0, 12))

        if self.es_gerente:
            tk.Label(acc, text="Cambiar rol:", font=FONT_BOLD, bg=FONDO, fg=TEXTO_DARK).pack(anchor="w")
            self.var_rol = tk.StringVar()
            self.cb_rol  = ttk.Combobox(acc, textvariable=self.var_rol,
                                         values=ROLES, state="readonly", width=18)
            self.cb_rol.pack(pady=4, fill="x")
            tk.Button(acc, text="💼 Asignar rol", command=self._asignar_rol,
                      **BTN_PRIMARY, width=18).pack(pady=4, fill="x")
            tk.Frame(acc, bg=BORDE, height=1).pack(fill="x", pady=8)

        tk.Button(acc, text="🗑️ Eliminar usuario", command=self._eliminar,
                  **BTN_DANGER, width=18).pack(pady=4, fill="x")
        tk.Button(acc, text="↻ Actualizar", command=self.cargar,
                  bg=AZUL_CLARO, fg=AZUL_MEDIO, font=FONT_SMALL,
                  relief="flat", cursor="hand2", width=18).pack(pady=12)

        if self.es_gerente:
            tk.Frame(acc, bg=BORDE, height=1).pack(fill="x", pady=4)
            tk.Label(acc, text="⚠️ Usuarios sin rol\nnecesitan asignación.",
                     font=FONT_SMALL, bg=FONDO, fg=ADVERTENCIA,
                     justify="center", wraplength=180).pack(pady=4)

    def _on_select(self):
        sel = self.tv.selection()
        self._sel_id = int(sel[0]) if sel else None

    def cargar(self):
        self.tv.delete(*self.tv.get_children())
        for i, r in enumerate(TrabajadoresController.listar()):
            tag = "par" if i % 2 == 0 else "impar"
            rol_label = r["rol"] or "⏳ Sin rol"
            self.tv.insert("", "end", iid=str(r["id"]),
                           values=(r["id"], r["nombre_completo"], r["usuario"],
                                   r["correo"], rol_label, "✅" if r["activo"] else "❌"),
                           tags=(tag, "sin_rol" if not r["rol"] else ""))
        self.tv.tag_configure("par",     background=TABLA_PAR)
        self.tv.tag_configure("impar",   background=TABLA_IMPAR)
        self.tv.tag_configure("sin_rol", foreground=ADVERTENCIA)

    def _asignar_rol(self):
        if not self._sel_id:
            messagebox.showwarning("Selección", "Selecciona un usuario.", parent=self); return
        nuevo_rol = self.var_rol.get()
        if not nuevo_rol:
            messagebox.showwarning("Rol", "Selecciona un rol primero.", parent=self); return

        # Obtener nombre para el confirm
        usuarios = TrabajadoresController.listar()
        target = next((u for u in usuarios if u["id"] == self._sel_id), None)
        nombre = target["nombre_completo"] if target else ""

        if not messagebox.askyesno("Confirmar",
                                   f"¿Asignar rol '{nuevo_rol}' a {nombre}?", parent=self):
            return

        ok, msg = TrabajadoresController.asignar_rol(self._sel_id, nuevo_rol, self.usuario)
        if ok:
            messagebox.showinfo("Rol asignado", msg, parent=self)
            self.cargar()
        else:
            messagebox.showerror("Error", msg, parent=self)

    def _eliminar(self):
        if not self._sel_id:
            messagebox.showwarning("Selección", "Selecciona un usuario.", parent=self); return
        ok, msg = TrabajadoresController.eliminar(self._sel_id, self.usuario)
        if ok:
            messagebox.showinfo("Eliminado", msg, parent=self)
            self.cargar()
        else:
            messagebox.showerror("Error", msg, parent=self)

    def _nuevo(self):
        NuevoUsuarioView(self, self.usuario, self.cargar)


class NuevoUsuarioView(tk.Toplevel):
    def __init__(self, parent, usuario_actual, on_save):
        super().__init__(parent)
        self.usuario_actual = usuario_actual
        self.on_save        = on_save
        self.title("Registrar nuevo usuario")
        self.geometry("420x480")
        self.resizable(False, False)
        self.configure(bg=FONDO)
        self.grab_set()
        self._build()

    def _build(self):
        tk.Label(self, text="Nuevo Usuario", font=FONT_TITULO, bg=FONDO, fg=TEXTO_DARK).pack(pady=(20, 4))
        frame = tk.Frame(self, bg=FONDO)
        frame.pack(fill="x", padx=28)

        campos = [
            ("Nombre completo",               "e_nombre",  False),
            ("Correo electrónico",            "e_correo",  False),
            ("Usuario",                        "e_usuario", False),
            ("Contraseña (mín. 6 caracteres)","e_pass",    True),
        ]
        for label, attr, es_pass in campos:
            tk.Label(frame, text=label, font=FONT_BOLD, bg=FONDO, fg=TEXTO_DARK, anchor="w").pack(fill="x")
            e = tk.Entry(frame, font=FONT_NORMAL, relief="solid", bd=1, show="•" if es_pass else "")
            e.pack(fill="x", pady=(2, 10), ipady=5)
            setattr(self, attr, e)

        tk.Label(frame, text="Rol", font=FONT_BOLD, bg=FONDO, fg=TEXTO_DARK, anchor="w").pack(fill="x")
        self.var_rol = tk.StringVar(value="vendedor")
        self.cb_rol  = ttk.Combobox(frame, textvariable=self.var_rol, values=ROLES, state="readonly")
        self.cb_rol.pack(fill="x", pady=(2, 10))
        # Solo el gerente puede asignar rol al crear
        if self.usuario_actual["rol"] != "gerente":
            self.cb_rol.config(state="disabled")
            tk.Label(frame, text="El gerente asignará el rol después del registro.",
                     font=FONT_SMALL, fg=ADVERTENCIA, bg=FONDO).pack(anchor="w")

        self.lbl_err = tk.Label(self, text="", font=FONT_SMALL, bg=FONDO, fg=PELIGRO, wraplength=360)
        self.lbl_err.pack()
        tk.Button(self, text="Crear usuario", command=self._crear, **BTN_PRIMARY).pack(pady=8, padx=28, fill="x")

    def _crear(self):
        rol = self.var_rol.get() if self.usuario_actual["rol"] == "gerente" else None
        ok, msg = TrabajadoresController.crear_usuario(
            self.e_nombre.get(), self.e_correo.get(),
            self.e_usuario.get(), self.e_pass.get(),
            rol, self.usuario_actual
        )
        if ok:
            messagebox.showinfo("Usuario creado", msg, parent=self)
            self.on_save()
            self.destroy()
        else:
            self.lbl_err.config(text=msg)
