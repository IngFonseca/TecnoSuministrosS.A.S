"""
MODELO – Proveedor
Responsabilidad: acceso a datos de la tabla `proveedores`.
"""
from utils.db import execute_query


class ProveedorModel:

    @staticmethod
    def get_all() -> list:
        return execute_query(
            """
            SELECT
                id,
                nombre,
                contacto AS correo,
                telefono,
                tipo AS tipo_producto
            FROM proveedores
            ORDER BY nombre
            """,
            fetch=True
        )

    @staticmethod
    def get_by_id(proveedor_id: int) -> dict | None:
        rows = execute_query(
            """
            SELECT
                id,
                nombre,
                contacto AS correo,
                telefono,
                tipo AS tipo_producto
            FROM proveedores
            WHERE id=%s
            """,
            (proveedor_id,),
            fetch=True
        )
        return rows[0] if rows else None

    @staticmethod
    def create(
        nombre: str,
        telefono: str,
        correo: str,
        tipo_producto: str
    ) -> int:
        return execute_query(
            """
            INSERT INTO proveedores
                (nombre, contacto, telefono, tipo)
            VALUES
                (%s, %s, %s, %s)
            """,
            (
                nombre,
                correo,
                telefono,
                tipo_producto
            )
        )

    @staticmethod
    def update(
        proveedor_id: int,
        nombre: str,
        telefono: str,
        correo: str,
        tipo_producto: str
    ) -> None:
        execute_query(
            """
            UPDATE proveedores
            SET
                nombre=%s,
                contacto=%s,
                telefono=%s,
                tipo=%s
            WHERE id=%s
            """,
            (
                nombre,
                correo,
                telefono,
                tipo_producto,
                proveedor_id
            )
        )

    @staticmethod
    def delete(proveedor_id: int) -> None:
        execute_query(
            "DELETE FROM proveedores WHERE id=%s",
            (proveedor_id,)
        )

    @staticmethod
    def count() -> int:
        row = execute_query(
            "SELECT COUNT(*) AS c FROM proveedores",
            fetch=True
        )
        return row[0]["c"]

    @staticmethod
    def get_para_reporte() -> list:
        return execute_query(
            """
            SELECT
                nombre,
                contacto AS correo,
                telefono,
                tipo AS tipo_producto
            FROM proveedores
            ORDER BY nombre
            """,
            fetch=True
        )