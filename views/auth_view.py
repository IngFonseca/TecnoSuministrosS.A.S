"""
VISTA – Autenticación
Responsabilidad: UI de login y registro. Delega toda la lógica a AuthController.
"""
import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import AuthController
from utils.theme import *


class LoginView:
    def __init__(self, on_success):
        self.on_success = on_success
        self.root = tk.Tk()
        self.root.title("TecnoSuministros S.A.S. – Iniciar Sesión")
        self.root.geometry("460x560")
        self.root.resizable(False, False)
        self.root.configure(bg=FONDO)
        self._centrar()
        self._build()
        self.root.mainloop()

    def _centrar(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 460) // 2
        y = (self.root.winfo_screenheight() - 560) // 2
        self.root.geometry(f"460x560+{x}+{y}")

    def _build(self):
        # Header
        hdr = tk.Frame(self.root, bg=AZUL_OSCURO, height=120)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Label(hdr, text="⚙", font=("Segoe UI", 32), bg=AZUL_OSCURO, fg=ACENTO).pack(pady=(18, 2))
        tk.Label(hdr, text="TecnoSuministros S.A.S.", font=("Segoe UI", 14, "bold"),
                 bg=AZUL_OSCURO, fg="white").pack()

        # Card
        card = tk.Frame(self.root, bg=PANEL)
        card.pack(fill="both", expand=True, padx=32, pady=24)

        tk.Label(card, text="Iniciar Sesión", font=FONT_TITULO, bg=PANEL, fg=TEXTO_DARK).pack(pady=(8, 4))
        tk.Label(card, text="Ingresa tus credenciales para continuar",
                 font=FONT_SMALL, bg=PANEL, fg=TEXTO_MEDIUM).pack(pady=(0, 20))

        tk.Label(card, text="Usuario", font=FONT_BOLD, bg=PANEL, fg=TEXTO_DARK, anchor="w").pack(fill="x", padx=4)
        self.entry_user = tk.Entry(card, font=FONT_NORMAL, relief="solid", bd=1)
        self.entry_user.pack(fill="x", padx=4, pady=(2, 12), ipady=6)

        tk.Label(card, text="Contraseña", font=FONT_BOLD, bg=PANEL, fg=TEXTO_DARK, anchor="w").pack(fill="x", padx=4)
        self.entry_pass = tk.Entry(card, font=FONT_NORMAL, relief="solid", bd=1, show="•")
        self.entry_pass.pack(fill="x", padx=4, pady=(2, 20), ipady=6)
        self.entry_pass.bind("<Return>", lambda _: self._login())

        tk.Button(card, text="Ingresar al sistema", command=self._login, **BTN_PRIMARY).pack(fill="x", padx=4)
        tk.Frame(card, bg=BORDE, height=1).pack(fill="x", padx=4, pady=16)
        tk.Button(card, text="Registrar nuevo usuario", command=self._abrir_registro,
                  bg=FONDO, fg=AZUL_MEDIO, font=("Segoe UI", 10), relief="flat", cursor="hand2").pack(fill="x", padx=4)

        self.lbl_error = tk.Label(card, text="", font=FONT_SMALL, bg=PANEL, fg=PELIGRO, wraplength=360)
        self.lbl_error.pack(pady=4)

    def _login(self):
        usuario, resultado, error = (
            self.entry_user.get().strip(),
            None, ""
        )
        resultado, error = AuthController.login(
            self.entry_user.get().strip(),
            self.entry_pass.get()
        )
        if error:
            self.lbl_error.config(text=error)
            return
        self.root.destroy()
        self.on_success(resultado)

    def _abrir_registro(self):
        RegistroView(self.root)


class RegistroView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar nuevo usuario")
        self.geometry("440x520")
        self.resizable(False, False)
        self.configure(bg=FONDO)
        self.grab_set()
        self._build()

    def _build(self):
        tk.Label(self, text="Crear Cuenta", font=FONT_TITULO, bg=FONDO, fg=TEXTO_DARK).pack(pady=(20, 4))
        tk.Label(self,
                 text="El gerente asignará tu rol antes de que puedas ingresar.",
                 font=FONT_SMALL, bg=FONDO, fg=TEXTO_MEDIUM, wraplength=380).pack(pady=(0, 12))

        frame = tk.Frame(self, bg=FONDO)
        frame.pack(fill="x", padx=28)

        campos = [
            ("Nombre completo",               "e_nombre",  False),
            ("Correo electrónico",            "e_correo",  False),
            ("Usuario",                        "e_usuario", False),
            ("Contraseña (mín. 6 caracteres)","e_pass",    True),
            ("Confirmar contraseña",          "e_pass2",   True),
        ]
        for label, attr, es_pass in campos:
            tk.Label(frame, text=label, font=FONT_BOLD, bg=FONDO, fg=TEXTO_DARK, anchor="w").pack(fill="x")
            e = tk.Entry(frame, font=FONT_NORMAL, relief="solid", bd=1, show="•" if es_pass else "")
            e.pack(fill="x", pady=(2, 10), ipady=5)
            setattr(self, attr, e)

        self.lbl_err = tk.Label(self, text="", font=FONT_SMALL, bg=FONDO, fg=PELIGRO, wraplength=380)
        self.lbl_err.pack()
        tk.Button(self, text="Crear cuenta", command=self._registrar, **BTN_PRIMARY).pack(pady=10, padx=28, fill="x")

    def _registrar(self):
        ok, msg = AuthController.registrar(
            self.e_nombre.get().strip(),
            self.e_correo.get().strip(),
            self.e_usuario.get().strip(),
            self.e_pass.get(),
            self.e_pass2.get(),
        )
        if ok:
            messagebox.showinfo("Cuenta creada", msg, parent=self)
            self.destroy()
        else:
            self.lbl_err.config(text=msg)
