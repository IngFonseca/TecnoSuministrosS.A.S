"""
MODELO – Usuario
Responsabilidad: acceso a datos de la tabla `usuarios`.
No contiene lógica de negocio ni UI.
"""
import bcrypt
from utils.db import execute_query


class UsuarioModel:

    @staticmethod
    def get_by_usuario(usuario: str) -> dict | None:
        rows = execute_query(
            "SELECT * FROM usuarios WHERE usuario=%s AND activo=1",
            (usuario,), fetch=True
        )
        return rows[0] if rows else None

    @staticmethod
    def get_all() -> list:
        return execute_query(
            "SELECT id, nombre_completo, usuario, correo, rol, activo "
            "FROM usuarios ORDER BY nombre_completo",
            fetch=True
        )

    @staticmethod
    def get_gerentes() -> list:
        return execute_query(
            "SELECT correo, nombre_completo FROM usuarios WHERE rol='gerente' AND activo=1",
            fetch=True
        )

    @staticmethod
    def create(nombre_completo: str, correo: str, usuario: str,
               contrasena_plana: str, rol: str | None) -> int:
        hashed = bcrypt.hashpw(contrasena_plana.encode(), bcrypt.gensalt()).decode()
        return execute_query(
            "INSERT INTO usuarios (nombre_completo, correo, usuario, contrasena, rol) "
            "VALUES (%s,%s,%s,%s,%s)",
            (nombre_completo, correo, usuario, hashed, rol)
        )

    @staticmethod
    def update_rol(usuario_id: int, nuevo_rol: str) -> None:
        execute_query(
            "UPDATE usuarios SET rol=%s WHERE id=%s",
            (nuevo_rol, usuario_id)
        )

    @staticmethod
    def delete(usuario_id: int) -> None:
        execute_query("DELETE FROM usuarios WHERE id=%s", (usuario_id,))

    @staticmethod
    def exists(usuario: str, correo: str) -> bool:
        rows = execute_query(
            "SELECT id FROM usuarios WHERE usuario=%s OR correo=%s",
            (usuario, correo), fetch=True
        )
        return bool(rows)

    @staticmethod
    def verify_password(contrasena_plana: str, hashed: str) -> bool:
        return bcrypt.checkpw(contrasena_plana.encode(), hashed.encode())
