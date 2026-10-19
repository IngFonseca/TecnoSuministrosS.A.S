import os
import sys

# CAMBIA ESTA LÍNEA por la URL de tu API en Render antes de generar el .exe
DEFAULT_API_URL = "https://tecnosuministros-api.onrender.com"


def _carpeta_app() -> str:
    if getattr(sys, "frozen", False):          # ejecutando como .exe
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_api_url() -> str:
    url = os.getenv("TECNO_API_URL", "").strip()
    if not url:
        ruta = os.path.join(_carpeta_app(), "api_url.txt")
        if os.path.isfile(ruta):
            with open(ruta, encoding="utf-8") as f:
                url = f.read().strip()
    return (url or DEFAULT_API_URL).rstrip("/")


def get_reports_dir() -> str:
    """Carpeta de los PDF (en el .exe: Documentos/TecnoSuministros/reports)."""
    if getattr(sys, "frozen", False):
        base = os.path.join(os.path.expanduser("~"), "Documents", "TecnoSuministros", "reports")
    else:
        base = os.path.join(_carpeta_app(), "reports")
    os.makedirs(base, exist_ok=True)
    return base