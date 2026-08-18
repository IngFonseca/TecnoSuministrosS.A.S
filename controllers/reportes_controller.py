"""
CONTROLADOR – Reportes
Responsabilidad: orquestar la generación de PDFs usando los modelos y pdf_generator.
"""
from models.venta_model import VentaModel
from models.producto_model import ProductoModel, MovimientoModel
from models.proveedor_model import ProveedorModel
from utils.pdf_generator import (reporte_ventas, reporte_inventario,
                                  reporte_proveedores, reporte_movimientos)
from utils import logger


class ReportesController:

    @staticmethod
    def pdf_ventas(usuario: dict) -> tuple[bool, str]:
        rows = VentaModel.get_todas()
        if not rows:
            return False, "No hay ventas registradas."
        ruta = reporte_ventas(rows)
        logger.log(usuario["id"], usuario["nombre_completo"], "Generó PDF de ventas", "Reportes")
        return True, ruta

    @staticmethod
    def pdf_inventario(usuario: dict) -> tuple[bool, str]:
        rows = ProductoModel.get_para_reporte()
        if not rows:
            return False, "No hay productos registrados."
        ruta = reporte_inventario(rows)
        logger.log(usuario["id"], usuario["nombre_completo"], "Generó PDF de inventario", "Reportes")
        return True, ruta

    @staticmethod
    def pdf_movimientos(usuario: dict) -> tuple[bool, str]:
        rows = MovimientoModel.get_all()
        if not rows:
            return False, "No hay movimientos registrados."
        ruta = reporte_movimientos(rows)
        logger.log(usuario["id"], usuario["nombre_completo"], "Generó PDF de movimientos", "Reportes")
        return True, ruta

    @staticmethod
    def pdf_proveedores(usuario: dict) -> tuple[bool, str]:
        rows = ProveedorModel.get_para_reporte()
        if not rows:
            return False, "No hay proveedores registrados."
        ruta = reporte_proveedores(rows)
        logger.log(usuario["id"], usuario["nombre_completo"], "Generó PDF de proveedores", "Reportes")
        return True, ruta
