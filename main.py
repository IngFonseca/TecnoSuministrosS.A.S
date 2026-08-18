"""
main.py – Punto de entrada de TecnoSuministros S.A.S. (arquitectura MVC)

Pasos antes de ejecutar:
    1. cp .env.example .env  →  completar credenciales MySQL y Gmail
    2. pip install -r requirements.txt
    3. python setup_db.py    →  crea BD, tablas y usuario gerente inicial
    4. python main.py
"""
import sys
import os

# Asegurar que la raíz del proyecto esté en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    try:
        from views.auth_view import LoginView
        from main_window import MainApp
        LoginView(lambda usuario: MainApp(usuario))
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk(); root.withdraw()
        messagebox.showerror(
            "Error de inicio",
            f"No se pudo iniciar la aplicación:\n\n{e}\n\n"
            "Verifica:\n"
            "• MySQL esté corriendo\n"
            "• .env esté configurado correctamente\n"
            "• Hayas ejecutado: python setup_db.py\n"
            "• Dependencias instaladas: pip install -r requirements.txt"
        )
        raise


if __name__ == "__main__":
    main()
