from models.venta_model import VentaModel
from utils import api_client as api


class DashboardController:

    @staticmethod
    def get_metricas() -> dict:
        return api.get("/dashboard/metricas")

    @staticmethod
    def get_ultimas_ventas(limite: int = 10) -> list:
        return VentaModel.get_recientes(limite)