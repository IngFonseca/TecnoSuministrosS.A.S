import re
from models.usuario_model import UsuarioModel
from utils import api_client
from utils.api_client import ApiError


class AuthController:

    @staticmethod
    def login(usuario: str, contrasena: str) -> tuple[dict | None, str]:
        """Retorna (usuario_dict, error_msg). Si es exitoso, error_msg es ''."""
        if not usuario or not contrasena:
            return None, "Completa todos los campos."
        try:
            data = UsuarioModel.login(usuario, contrasena)
        except ApiError as e:
            return None, e.detail

        api_client.set_token(data["token"])   # la pulsera vive solo en memoria
        return data["usuario"], ""

    @staticmethod
    def logout() -> None:
        api_client.clear_token()

    @staticmethod
    def registrar(nombre: str, correo: str, usuario: str,
                  pwd: str, pwd2: str) -> tuple[bool, str]:
        if not all([nombre, correo, usuario, pwd, pwd2]):
            return False, "Todos los campos son obligatorios."
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            return False, "Formato de correo inválido."
        if len(pwd) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."
        if pwd != pwd2:
            return False, "Las contraseñas no coinciden."

        try:
            return True, UsuarioModel.registrar(nombre, correo, usuario, pwd)
        except ApiError as e:
            return False, e.detail