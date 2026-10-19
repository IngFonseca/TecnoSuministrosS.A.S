from utils import api_client as api
from utils.api_client import ApiError


class ProductoModel:

    @staticmethod
    def get_all(buscar: str = "", categoria: str = "") -> list:
        return api.get("/productos", {"buscar": buscar, "categoria": categoria})

    @staticmethod
    def get_by_id(producto_id: int) -> dict | None:
        try:
            return api.get(f"/productos/{producto_id}")
        except ApiError as e:
            if e.status == 404:
                return None
            raise

    @staticmethod
    def get_disponibles(categoria: str = "") -> list:
        return api.get("/productos/disponibles", {"categoria": categoria})

    @staticmethod
    def create(nombre: str, cantidad: int, precio: float,
               categoria_id: int | None, proveedor_id: int | None) -> str:
        """Crea el producto (y su movimiento inicial). Devuelve el código."""
        return api.post("/productos", {
            "nombre": nombre, "cantidad": cantidad, "precio": precio,
            "categoria_id": categoria_id, "proveedor_id": proveedor_id,
        })["codigo"]

    @staticmethod
    def update(producto_id: int, nombre: str, cantidad: int, precio: float,
               categoria_id: int | None, proveedor_id: int | None) -> None:
        api.put(f"/productos/{producto_id}", {
            "nombre": nombre, "cantidad": cantidad, "precio": precio,
            "categoria_id": categoria_id, "proveedor_id": proveedor_id,
        })

    @staticmethod
    def delete(producto_id: int) -> None:
        api.delete(f"/productos/{producto_id}")

    @staticmethod
    def registrar_movimiento(producto_id: int, tipo: str,
                             cantidad: int, motivo: str) -> str:
        return api.post(f"/productos/{producto_id}/movimientos", {
            "tipo": tipo, "cantidad": cantidad, "motivo": motivo,
        })["mensaje"]

    @staticmethod
    def get_para_reporte() -> list:
        return api.get("/productos/reporte")


class CategoriaModel:

    @staticmethod
    def get_all() -> list:
        return api.get("/categorias")

    @staticmethod
    def create(nombre: str) -> int:
        return api.post("/categorias", {"nombre": nombre})["id"]


class MovimientoModel:

    @staticmethod
    def get_all() -> list:
        return api.get("/movimientos")