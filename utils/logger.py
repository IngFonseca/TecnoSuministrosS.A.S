from utils import api_client as api


def log(usuario_id: int, usuario_nombre: str, accion: str, modulo: str = ""):
    """Registra acciones que solo existen en el cliente (cerrar sesión, exportar PDF)."""
    try:
        api.post("/log", {"accion": accion, "modulo": modulo})
    except Exception as e:
        print(f"[Logger] No se pudo registrar acción: {e}")