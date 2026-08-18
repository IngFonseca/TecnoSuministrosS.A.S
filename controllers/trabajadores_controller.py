"""
CONTROLADOR – Trabajadores
Responsabilidad: lógica de negocio para gestión de usuarios y asignación de roles.
Solo el gerente puede asignar roles.
"""
import re
from models.usuario_model import UsuarioModel
from utils import logger
from utils.email_service import send_welcome_email, send_new_user_notification_to_manager

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

        rows = UsuarioModel.get_all()
        target = next((u for u in rows if u["id"] == target_id), None)
        if not target:
            return False, "Usuario no encontrado."

        rol_anterior = target["rol"]
        UsuarioModel.update_rol(target_id, nuevo_rol)
        logger.log(usuario_actual["id"], usuario_actual["nombre_completo"],
                   f"Asignó rol '{nuevo_rol}' a {target['nombre_completo']}", "Trabajadores")

        # Correo solo si es la primera asignación (venía sin rol)
        if rol_anterior is None:
            send_welcome_email(
                target["nombre_completo"], target["usuario"],
                target["correo"], nuevo_rol
            )
        return True, f"Rol '{nuevo_rol}' asignado a {target['nombre_completo']}."

    @staticmethod
    def eliminar(target_id: int, usuario_actual: dict) -> tuple[bool, str]:
        if target_id == usuario_actual["id"]:
            return False, "No puedes eliminar tu propia cuenta."
        rows = UsuarioModel.get_all()
        target = next((u for u in rows if u["id"] == target_id), None)
        nombre = target["nombre_completo"] if target else str(target_id)
        UsuarioModel.delete(target_id)
        logger.log(usuario_actual["id"], usuario_actual["nombre_completo"],
                   f"Eliminó usuario: {nombre}", "Trabajadores")
        return True, f"Usuario '{nombre}' eliminado."

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
        if UsuarioModel.exists(usuario, correo):
            return False, "El usuario o correo ya está registrado."

        # Solo el gerente puede asignar rol al crear; otros crean sin rol
        rol_asignado = rol if usuario_actual["rol"] == "gerente" else None
        uid = UsuarioModel.create(nombre, correo, usuario, pwd, rol_asignado)
        logger.log(usuario_actual["id"], usuario_actual["nombre_completo"],
                   f"Creó usuario: {nombre} ({usuario})", "Trabajadores")

        if rol_asignado:
            email_ok = send_welcome_email(
                nombre,
                usuario,
                correo,
                rol_asignado
            )

            if not email_ok:
                print(
                    "[Email] El usuario se creó correctamente, "
                    "pero no se pudo enviar el correo de bienvenida."
                )
        else:
            for g in UsuarioModel.get_gerentes():
                send_new_user_notification_to_manager(
                    g["correo"],
                    g["nombre_completo"],
                    nombre,
                    usuario,
                    correo
                )

            email_ok = send_welcome_email(
                nombre,
                usuario,
                correo,
                "pendiente de asignación"
            )

            if not email_ok:
                print(
                    "[Email] El usuario se creó correctamente, "
                    "pero no se pudo enviar el correo de bienvenida."
                )

        return True, f"Usuario '{usuario}' creado correctamente."
