"""Registro de actividad en base de datos."""
from utils.db import execute_query


def log(usuario_id: int, usuario_nombre: str, accion: str, modulo: str = ""):
    """Guarda una acción en el log de actividad."""
    try:
        execute_query(
            "INSERT INTO log_actividad (usuario_id, usuario_nombre, accion, modulo) VALUES (%s, %s, %s, %s)",
            (usuario_id, usuario_nombre, accion, modulo)
        )
    except Exception as e:
        print(f"[Logger] No se pudo registrar acción: {e}")
