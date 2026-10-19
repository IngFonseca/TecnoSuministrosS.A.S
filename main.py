import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _instalar_manejador_de_errores():
    """Todo error de la API que no atrape una pantalla se muestra como mensaje claro."""
    import tkinter as tk
    from tkinter import messagebox
    from utils.api_client import ApiError

    def manejador(self, exc, val, tb):
        if isinstance(val, ApiError):
            messagebox.showerror("Error", val.detail)
        else:
            import traceback
            traceback.print_exception(exc, val, tb)
            messagebox.showerror("Error inesperado", f"{type(val).__name__}: {val}")

    tk.Tk.report_callback_exception = manejador


def main():
    try:
        from utils import api_client
        from views.auth_view import LoginView
        from main_window import MainApp

        _instalar_manejador_de_errores()
        api_client.warmup()   # despierta el servidor mientras el usuario escribe
        LoginView(lambda usuario: MainApp(usuario))
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk(); root.withdraw()
        messagebox.showerror(
            "Error de inicio",
            f"No se pudo iniciar la aplicación:\n\n{e}\n\n"
            "Verifica:\n"
            "• Que tengas conexión a internet\n"
            "• Que la dirección de la API (utils/config.py o api_url.txt) sea correcta"
        )
        raise


if __name__ == "__main__":
    main()