"""
VENTANA PRINCIPAL – TecnoSuministros S.A.S. (MVC)
Responsabilidad: shell de la aplicación (sidebar + área de contenido).
Instancia las Vistas e inyecta el usuario autenticado.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from utils.theme import *
from utils import logger


# Mapa de módulos: key → {label, roles, view_class}
MODULOS = {
    "dashboard":    {"label": "🏠 Dashboard",    "roles": ["gerente", "administrador", "vendedor", "bodega"]},
    "inventario":   {"label": "📦 Inventario",   "roles": ["gerente", "administrador", "bodega"]},
    "ventas":       {"label": "🛒 Ventas",       "roles": ["gerente", "administrador", "vendedor"]},
    "proveedores":  {"label": "🏭 Proveedores",  "roles": ["gerente", "administrador"]},
    "reportes":     {"label": "📋 Reportes",     "roles": ["gerente", "administrador"]},
    "trabajadores": {"label": "👥 Trabajadores", "roles": ["gerente", "administrador"]},
}


class MainApp:
    def __init__(self, usuario: dict):
        self.usuario = usuario
        self.frame_activo = None
        self.nav_buttons = {}

        self.root = tk.Tk()
        self.root.title("TecnoSuministros S.A.S.")
        self.root.geometry("1200x720")
        self.root.minsize(1000, 600)
        self.root.configure(bg=FONDO)

        # ============================================================
        # ESTILOS GLOBALES DE TABLAS
        # Se aplican a todos los ttk.Treeview de la aplicación.
        # ============================================================
        self._configurar_estilos_tablas()

        self._centrar()
        self._build_shell()
        self._navegar("dashboard")
        self.root.mainloop()

    # ── Estilos globales ─────────────────────────────────────────────

    def _configurar_estilos_tablas(self):
        style = ttk.Style(self.root)

        # Usamos clam porque permite controlar mejor los colores
        # de los encabezados y las filas.
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        # Texto y filas de las tablas
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#000000",
            fieldbackground="#FFFFFF",
            font=("Segoe UI", 10),
            rowheight=30
        )

        # Títulos / encabezados de las tablas
        style.configure(
            "Treeview.Heading",
            background="#FFFFFF",
            foreground="#000000",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(8, 8)
        )

        # Cuando el usuario selecciona una fila,
        # el texto continúa siendo visible.
        style.map(
            "Treeview",
            foreground=[
                ("selected", "#000000")
            ],
            background=[
                ("selected", "#DCE6F1")
            ]
        )

        # El encabezado permanece negro incluso al pasar el mouse.
        style.map(
            "Treeview.Heading",
            foreground=[
                ("active", "#000000")
            ],
            background=[
                ("active", "#FFFFFF")
            ]
        )

    def _centrar(self):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(
            f"1200x720+{(sw-1200)//2}+{(sh-720)//2}"
        )

    # ── Shell de la ventana ─────────────────────────────────────────

    def _build_shell(self):

        # Sidebar
        self.sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=220
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo
        logo = tk.Frame(
            self.sidebar,
            bg=AZUL_OSCURO,
            pady=16
        )
        logo.pack(fill="x")

        tk.Label(
            logo,
            text="⚙",
            font=("Segoe UI", 28),
            bg=AZUL_OSCURO,
            fg=ACENTO
        ).pack()

        tk.Label(
            logo,
            text="TecnoSuministros",
            font=("Segoe UI", 11, "bold"),
            bg=AZUL_OSCURO,
            fg="white"
        ).pack()

        tk.Label(
            logo,
            text="S.A.S.",
            font=("Segoe UI", 9),
            bg=AZUL_OSCURO,
            fg="#a8c4e0"
        ).pack()

        tk.Frame(
            self.sidebar,
            bg="#2a4a6c",
            height=1
        ).pack(fill="x", pady=4)

        # Botones de navegación
        nav = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )
        nav.pack(fill="x", pady=8)

        rol = self.usuario.get("rol", "")

        for key, info in MODULOS.items():

            if rol not in info["roles"]:
                continue

            btn = tk.Button(
                nav,
                text=info["label"],
                font=FONT_NAV,
                bg=SIDEBAR,
                fg=SIDEBAR_TEXT,
                relief="flat",
                anchor="w",
                padx=20,
                pady=10,
                cursor="hand2",
                bd=0,
                activebackground=SIDEBAR_HOVER,
                activeforeground="white",
                command=lambda k=key: self._navegar(k)
            )

            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        # Footer del sidebar
        foot = tk.Frame(
            self.sidebar,
            bg=SIDEBAR
        )
        foot.pack(
            side="bottom",
            fill="x",
            pady=8
        )

        tk.Frame(
            foot,
            bg="#2a4a6c",
            height=1
        ).pack(
            fill="x",
            pady=4
        )

        rol_color = ROLES_COLORES.get(
            rol,
            "#94a3b8"
        )

        tk.Label(
            foot,
            text=self.usuario["nombre_completo"],
            font=("Segoe UI", 9, "bold"),
            bg=SIDEBAR,
            fg="white",
            wraplength=190,
            justify="left"
        ).pack(
            padx=12,
            anchor="w"
        )

        tk.Label(
            foot,
            text=rol.upper() if rol else "SIN ROL",
            font=("Segoe UI", 8),
            bg=rol_color,
            fg="white",
            padx=6,
            pady=2
        ).pack(
            anchor="w",
            padx=12,
            pady=2
        )

        tk.Button(
            foot,
            text="⏻ Cerrar sesión",
            command=self._logout,
            bg="#c0392b",
            fg="white",
            font=("Segoe UI", 9),
            relief="flat",
            cursor="hand2",
            pady=6,
            bd=0,
            activebackground="#922b21"
        ).pack(
            fill="x",
            padx=12,
            pady=4
        )

        # Área principal de contenido
        self.content = tk.Frame(
            self.root,
            bg=FONDO
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

    # ── Navegación ───────────────────────────────────────────────────

    def _navegar(self, modulo: str):

        # Resaltar botón activo
        for key, btn in self.nav_buttons.items():

            btn.config(
                bg=SIDEBAR_HOVER if key == modulo else SIDEBAR,
                font=(
                    ("Segoe UI", 11, "bold")
                    if key == modulo
                    else FONT_NAV
                )
            )

        # Destruir vista anterior
        if self.frame_activo:
            self.frame_activo.destroy()
            self.frame_activo = None

        # Instanciar vista correspondiente
        vista = self._crear_vista(modulo)

        if vista:
            vista.pack(
                fill="both",
                expand=True
            )

            self.frame_activo = vista

    def _crear_vista(self, modulo: str):

        u = self.usuario

        if modulo == "dashboard":
            from views.dashboard_view import DashboardView
            return DashboardView(self.content, u)

        if modulo == "inventario":
            from views.inventario_view import InventarioView
            return InventarioView(self.content, u)

        if modulo == "ventas":
            from views.ventas_view import VentasView
            return VentasView(self.content, u)

        if modulo == "proveedores":
            from views.proveedores_view import ProveedoresView
            return ProveedoresView(self.content, u)

        if modulo == "reportes":
            from views.reportes_view import ReportesView
            return ReportesView(self.content, u)

        if modulo == "trabajadores":
            from views.trabajadores_view import TrabajadoresView
            return TrabajadoresView(self.content, u)

        return None

    # ── Logout ───────────────────────────────────────────────────────

    def _logout(self):

        if messagebox.askyesno(
            "Cerrar sesión",
            "¿Deseas cerrar sesión?",
            parent=self.root
        ):

            logger.log(
                self.usuario["id"],
                self.usuario["nombre_completo"],
                "Cierre de sesión",
                "Auth"
            )

            self.root.destroy()

            from views.auth_view import LoginView
            LoginView(
                lambda u: MainApp(u)
            )