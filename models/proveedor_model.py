from utils import api_client as api
from utils.api_client import ApiError


class ProveedorModel:

    @staticmethod
    def get_all() -> list:
        return api.get("/proveedores")

    @staticmethod
    def get_by_id(proveedor_id: int) -> dict | None:
        try:
            return api.get(f"/proveedores/{proveedor_id}")
        except ApiError as e:
            if e.status == 404:
                return None
            raise

    @staticmethod
    def create(nombre: str, telefono: str, correo: str, tipo_producto: str) -> int:
        return api.post("/proveedores", {
            "nombre": nombre, "telefono": telefono,
            "correo": correo, "tipo_producto": tipo_producto,
        })["id"]

    @staticmethod
    def update(proveedor_id: int, nombre: str, telefono: str,
               correo: str, tipo_producto: str) -> None:
        api.put(f"/proveedores/{proveedor_id}", {
            "nombre": nombre, "telefono": telefono,
            "correo": correo, "tipo_producto": tipo_producto,
        })

    @staticmethod
    def delete(proveedor_id: int) -> None:
        api.delete(f"/proveedores/{proveedor_id}")

    @staticmethod
    def get_para_reporte() -> list:
        return api.get("/proveedores/reporte")