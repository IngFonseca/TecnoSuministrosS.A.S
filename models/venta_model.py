from utils import api_client as api


class VentaModel:

    @staticmethod
    def registrar(items: list[dict]) -> dict:
        """
        Solo se envía (producto, cantidad): el precio, el descuento y el IVA
        los calcula el servidor. Devuelve {"mensaje", "subtotal", "descuento_pct", "total"}.
        """
        return api.post("/ventas", {
            "items": [{"producto_id": i["producto_id"], "cantidad": i["cantidad"]} for i in items]
        })

    @staticmethod
    def get_recientes(limite: int = 10) -> list:
        return api.get("/ventas/recientes", {"limite": limite})

    @staticmethod
    def get_todas() -> list:
        return api.get("/ventas/todas")