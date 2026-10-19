import re
from models.usuario_model import UsuarioModel
from utils.api_client import ApiError

ROLES = ["gerente", "administrador", "vendedor", "bodega"]


class TrabajadoresController:

    @staticmethod
    def listar() -> list:
        return UsuarioModel.get_all()

    @staticmethod
    def asignar_rol(target_id: int, nuevo_rol: str,
                    usuario_actual: dict) -> tuple[bool, str]:
        if usuario_actual["rol"] != "gerente":
            return False, "Solo el gerente puede asignar roles."
        if nuevo_rol not in ROLES:
            return False, "Rol inválido."
        try:
            return True, UsuarioModel.update_rol(target_id, nuevo_rol)
        except ApiError as e:
            return False, e.detail

    @staticmethod
    def eliminar(target_id: int, usuario_actual: dict) -> tuple[bool, str]:
        if target_id == usuario_actual["id"]:
            return False, "No puedes eliminar tu propia cuenta."
        try:
            return True, UsuarioModel.delete(target_id)
        except ApiError as e:
            return False, e.detail

    @staticmethod
    def crear_usuario(nombre: str, correo: str, usuario: str,
                      pwd: str, rol: str | None,
                      usuario_actual: dict) -> tuple[bool, str]:
        nombre  = nombre.strip()
        correo  = correo.strip()
        usuario = usuario.strip()

        if not all([nombre, correo, usuario, pwd]):
            return False, "Todos los campos son obligatorios."
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            return False, "Formato de correo inválido."
        if len(pwd) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."
        if rol and rol not in ROLES and usuario_actual["rol"] == "gerente":
            return False, "Rol inválido."

        rol_asignado = rol if usuario_actual["rol"] == "gerente" else None
        try:
            return True, UsuarioModel.create(nombre, correo, usuario, pwd, rol_asignado)
        except ApiError as e:
            return False, e.detail