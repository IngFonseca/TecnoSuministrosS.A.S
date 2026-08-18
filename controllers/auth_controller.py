"""
CONTROLADOR – Autenticación
Responsabilidad: lógica de negocio de login, registro y validaciones.
No importa nada de Tkinter.
"""
import re
from models.usuario_model import UsuarioModel
from utils.email_service import send_welcome_email, send_new_user_notification_to_manager
from utils import logger


class AuthController:

    @staticmethod
    def login(usuario: str, contrasena: str) -> tuple[dict | None, str]:
        """
        Retorna (usuario_dict, error_msg).
        Si login es exitoso, error_msg es "".
        """
        if not usuario or not contrasena:
            return None, "Completa todos los campos."

        user = UsuarioModel.get_by_usuario(usuario)
        if user is None or not UsuarioModel.verify_password(contrasena, user["contrasena"]):
            return None, "Credenciales incorrectas. Intenta de nuevo."

        if user["rol"] is None:
            return None, "Tu cuenta no tiene rol asignado.\nEspera a que el gerente te asigne uno."

        logger.log(user["id"], user["nombre_completo"], "Inicio de sesión", "Auth")
        return user, ""

    @staticmethod
    def registrar(nombre: str, correo: str, usuario: str,
                  pwd: str, pwd2: str) -> tuple[bool, str]:
        """
        Retorna (exito, mensaje).
        """
        if not all([nombre, correo, usuario, pwd, pwd2]):
            return False, "Todos los campos son obligatorios."
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            return False, "Formato de correo inválido."
        if len(pwd) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."
        if pwd != pwd2:
            return False, "Las contraseñas no coinciden."
        if UsuarioModel.exists(usuario, correo):
            return False, "El usuario o correo ya está registrado."

        uid = UsuarioModel.create(nombre, correo, usuario, pwd, rol=None)
        logger.log(uid, nombre, "Registro de nuevo usuario (sin rol)", "Auth")

        # Notificar a todos los gerentes
        for g in UsuarioModel.get_gerentes():
            send_new_user_notification_to_manager(
                g["correo"], g["nombre_completo"], nombre, usuario, correo
            )

        email_ok = send_welcome_email(
            nombre,
            usuario,
            correo,
            "pendiente de asignación"
        )

        if email_ok:
            mensaje_email = (
                f"Se envió el correo de bienvenida a {correo}."
            )
        else:
            mensaje_email = (
                "La cuenta fue creada, pero no se pudo enviar "
                "el correo de bienvenida. Revisa la configuración SMTP."
            )

        return True, (
            f"¡Cuenta creada!\n"
            f"Hola {nombre}.\n"
            f"{mensaje_email}\n"
            "Espera a que el gerente te asigne un rol."
        )
