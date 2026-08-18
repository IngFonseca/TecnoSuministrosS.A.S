"""
MODELO – Venta
Responsabilidad: acceso a datos de la tabla `ventas`.
"""
from utils.db import execute_query


class VentaModel:

    @staticmethod
    def create(producto_id: int, nombre_producto: str, cantidad: int,
               precio_unitario: float, descuento: float, iva: float,
               total: float, usuario_id: int) -> int:
        return execute_query(
            "INSERT INTO ventas "
            "(producto_id, nombre_producto, cantidad, precio_unitario, "
            "descuento, iva, total, usuario_id) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (producto_id, nombre_producto, cantidad, precio_unitario,
             descuento, iva, total, usuario_id)
        )

    @staticmethod
    def get_recientes(limite: int = 10) -> list:
        return execute_query(
            """
            SELECT
                fecha,
                COALESCE(NULLIF(nombre_producto, ''), 'Venta histórica') AS nombre_producto,
                cantidad,
                precio_unitario,
                descuento,
                total
            FROM ventas
            ORDER BY fecha DESC
            LIMIT %s
            """,
            (limite,),
            fetch=True
        )

    @staticmethod
    def get_todas() -> list:
        return execute_query(
            "SELECT fecha, nombre_producto, cantidad, precio_unitario, descuento, iva, total "
            "FROM ventas ORDER BY fecha DESC",
            fetch=True
        )

    @staticmethod
    def count_hoy() -> int:
        row = execute_query(
            "SELECT COUNT(*) as c FROM ventas WHERE DATE(fecha)=CURDATE()",
            fetch=True
        )
        return row[0]["c"]
