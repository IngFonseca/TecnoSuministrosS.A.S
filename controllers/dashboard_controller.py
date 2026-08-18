"""
CONTROLADOR – Dashboard
Responsabilidad: obtener métricas del sistema para mostrar en el dashboard.
"""
from models.producto_model import ProductoModel
from models.venta_model import VentaModel
from models.proveedor_model import ProveedorModel


class DashboardController:

    @staticmethod
    def get_metricas() -> dict:
        from utils.db import execute_query
        total_prod  = execute_query("SELECT COUNT(*) as c FROM productos", fetch=True)[0]["c"]
        ventas_hoy  = VentaModel.count_hoy()
        stock_bajo  = execute_query("SELECT COUNT(*) as c FROM productos WHERE cantidad<=5", fetch=True)[0]["c"]
        proveedores = ProveedorModel.count()
        return {
            "total_productos": total_prod,
            "ventas_hoy":      ventas_hoy,
            "stock_bajo":      stock_bajo,
            "total_proveedores": proveedores,
        }

    @staticmethod
    def get_ultimas_ventas(limite: int = 10) -> list:
        return VentaModel.get_recientes(limite)
