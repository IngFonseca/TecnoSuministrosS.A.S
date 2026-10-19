from utils import api_client as api


class UsuarioModel:

    @staticmethod
    def login(usuario: str, password: str) -> dict:
        """Devuelve {"token": ..., "usuario": {...}}. Lanza ApiError si falla."""
        return api.post("/auth/login", {"usuario": usuario, "password": password})

    @staticmethod
    def registrar(nombre: str, correo: str, usuario: str, password: str) -> str:
        return api.post("/auth/registro", {
            "nombre": nombre, "correo": correo, "usuario": usuario, "password": password,
        })["mensaje"]

    @staticmethod
    def get_all() -> list:
        return api.get("/usuarios")

    @staticmethod
    def create(nombre: str, correo: str, usuario: str,
               password: str, rol: str | None) -> str:
        return api.post("/usuarios", {
            "nombre": nombre, "correo": correo, "usuario": usuario,
            "password": password, "rol": rol,
        })["mensaje"]

    @staticmethod
    def update_rol(usuario_id: int, nuevo_rol: str) -> str:
        return api.put(f"/usuarios/{usuario_id}/rol", {"rol": nuevo_rol})["mensaje"]

    @staticmethod
    def delete(usuario_id: int) -> str:
        return api.delete(f"/usuarios/{usuario_id}")["mensaje"]