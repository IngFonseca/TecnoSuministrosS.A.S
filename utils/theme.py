"""Paleta de colores y estilos para la interfaz de TecnoSuministros."""

# Colores principales
AZUL_OSCURO   = "#1a3a5c"
AZUL_MEDIO    = "#2563a8"
AZUL_CLARO    = "#e8f0fe"
ACENTO        = "#f59e0b"
ACENTO_HOVER  = "#d97706"
PELIGRO       = "#dc2626"
EXITO         = "#16a34a"
ADVERTENCIA   = "#d97706"
FONDO         = "#f4f6f9"
PANEL         = "#ffffff"
SIDEBAR       = "#1a3a5c"
SIDEBAR_HOVER = "#2563a8"
SIDEBAR_TEXT  = "#ffffff"
TEXTO_DARK    = "#1e293b"
TEXTO_MEDIUM  = "#475569"
TEXTO_LIGHT   = "#94a3b8"
BORDE         = "#e2e8f0"
TABLA_PAR     = "#f8fafc"
TABLA_IMPAR   = "#ffffff"
TABLA_HEAD    = "#1a3a5c"
TABLA_HEAD_TXT= "#ffffff"

# Fuentes
FONT_TITULO   = ("Segoe UI", 18, "bold")
FONT_SUBTITULO= ("Segoe UI", 13, "bold")
FONT_NORMAL   = ("Segoe UI", 10)
FONT_SMALL    = ("Segoe UI", 9)
FONT_BOLD     = ("Segoe UI", 10, "bold")
FONT_NAV      = ("Segoe UI", 11)

# Estilos de botones
BTN_PRIMARY = {
    "bg": AZUL_MEDIO, "fg": "white", "font": ("Segoe UI", 10, "bold"),
    "relief": "flat", "cursor": "hand2", "padx": 16, "pady": 6,
    "activebackground": "#1d4ed8", "activeforeground": "white",
    "bd": 0,
}
BTN_DANGER = {
    "bg": PELIGRO, "fg": "white", "font": ("Segoe UI", 10, "bold"),
    "relief": "flat", "cursor": "hand2", "padx": 16, "pady": 6,
    "activebackground": "#b91c1c", "activeforeground": "white",
    "bd": 0,
}
BTN_SUCCESS = {
    "bg": EXITO, "fg": "white", "font": ("Segoe UI", 10, "bold"),
    "relief": "flat", "cursor": "hand2", "padx": 16, "pady": 6,
    "activebackground": "#15803d", "activeforeground": "white",
    "bd": 0,
}
BTN_WARNING = {
    "bg": ACENTO, "fg": "white", "font": ("Segoe UI", 10, "bold"),
    "relief": "flat", "cursor": "hand2", "padx": 16, "pady": 6,
    "activebackground": ACENTO_HOVER, "activeforeground": "white",
    "bd": 0,
}
BTN_SECONDARY = {
    "bg": "#64748b", "fg": "white", "font": ("Segoe UI", 10),
    "relief": "flat", "cursor": "hand2", "padx": 12, "pady": 5,
    "activebackground": "#475569", "activeforeground": "white",
    "bd": 0,
}

ROLES_COLORES = {
    "gerente":       "#7c3aed",
    "administrador": "#0284c7",
    "vendedor":      "#16a34a",
    "bodega":        "#d97706",
    None:            "#94a3b8",
}

ROLES_TAREAS = {
    "gerente":       "✦ Gestionar trabajadores, asignar roles y supervisar el sistema completo.",
    "administrador": "✦ Administrar inventario, proveedores y generar reportes PDF.",
    "vendedor":      "✦ Registrar ventas, gestionar el carrito y consultar el dashboard.",
    "bodega":        "✦ Controlar entradas/salidas de stock y movimientos de inventario.",
}
