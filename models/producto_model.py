"""
MODELO – Producto
Responsabilidad: acceso a datos de `productos`, `categorias`, `movimientos_stock`.
"""
from utils.db import execute_query


class ProductoModel:

    @staticmethod
    def _next_codigo() -> str:
        row = execute_query(
            "SELECT MAX(CAST(SUBSTRING(codigo,4) AS UNSIGNED)) as mx FROM productos",
            fetch=True
        )
        n = (row[0]["mx"] or 0) + 1
        return f"PRD{n:04d}"

    @staticmethod
    def get_all(buscar: str = "", categoria: str = "") -> list:
        q = """SELECT p.id, p.codigo, p.nombre,
                      IFNULL(c.nombre,'–') as categoria,
                      IFNULL(pr.nombre,'–') as proveedor,
                      p.cantidad, p.precio, p.proveedor_id
               FROM productos p
               LEFT JOIN categorias c ON p.categoria_id=c.id
               LEFT JOIN proveedores pr ON p.proveedor_id=pr.id
               WHERE 1=1"""
        params = []
        if buscar:
            q += " AND p.nombre LIKE %s"; params.append(f"%{buscar}%")
        if categoria and categoria != "Todas":
            q += " AND c.nombre=%s"; params.append(categoria)
        q += " ORDER BY p.codigo"
        return execute_query(q, tuple(params), fetch=True)

    @staticmethod
    def get_by_id(producto_id: int) -> dict | None:
        rows = execute_query("SELECT * FROM productos WHERE id=%s", (producto_id,), fetch=True)
        return rows[0] if rows else None

    @staticmethod
    def get_disponibles(categoria: str = "") -> list:
        q = """SELECT p.id, p.nombre, p.precio, p.cantidad,
                      IFNULL(c.nombre,'') as categoria
               FROM productos p
               LEFT JOIN categorias c ON p.categoria_id=c.id
               WHERE p.cantidad>0"""
        params = []
        if categoria and categoria != "Todas":
            q += " AND c.nombre=%s"; params.append(categoria)
        q += " ORDER BY p.nombre"
        return execute_query(q, tuple(params), fetch=True)

    @staticmethod
    def create(nombre: str, cantidad: int, precio: float,
               categoria_id: int | None, proveedor_id: int | None) -> str:
        codigo = ProductoModel._next_codigo()
        execute_query(
            "INSERT INTO productos (codigo, nombre, cantidad, precio, categoria_id, proveedor_id) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (codigo, nombre, cantidad, precio, categoria_id, proveedor_id)
        )
        return codigo

    @staticmethod
    def update(producto_id: int, nombre: str, cantidad: int, precio: float,
               categoria_id: int | None, proveedor_id: int | None) -> None:
        execute_query(
            "UPDATE productos SET nombre=%s, cantidad=%s, precio=%s, "
            "categoria_id=%s, proveedor_id=%s WHERE id=%s",
            (nombre, cantidad, precio, categoria_id, proveedor_id, producto_id)
        )

    @staticmethod
    def delete(producto_id: int) -> None:
        execute_query("DELETE FROM productos WHERE id=%s", (producto_id,))

    @staticmethod
    def update_stock(producto_id: int, delta: int) -> None:
        """delta positivo = entrada, negativo = salida."""
        execute_query(
            "UPDATE productos SET cantidad=cantidad+%s WHERE id=%s",
            (delta, producto_id)
        )

    @staticmethod
    def get_stock(producto_id: int) -> int:
        row = execute_query(
            "SELECT cantidad FROM productos WHERE id=%s", (producto_id,), fetch=True
        )
        return row[0]["cantidad"] if row else 0

    @staticmethod
    def get_bajo_stock(umbral: int = 5) -> list:
        return execute_query(
            "SELECT p.id, p.codigo, p.nombre, p.cantidad, p.proveedor_id, "
            "pr.contacto as proveedor_correo, pr.nombre as proveedor_nombre "
            "FROM productos p LEFT JOIN proveedores pr ON p.proveedor_id=pr.id "
            "WHERE p.cantidad<=%s",
            (umbral,), fetch=True
        )

    @staticmethod
    def get_para_reporte() -> list:
        return execute_query("""
            SELECT p.codigo, p.nombre,
                   IFNULL(c.nombre,'–') as categoria,
                   IFNULL(pr.nombre,'–') as proveedor,
                   p.cantidad, p.precio
            FROM productos p
            LEFT JOIN categorias c ON p.categoria_id=c.id
            LEFT JOIN proveedores pr ON p.proveedor_id=pr.id
            ORDER BY p.codigo
        """, fetch=True)


class CategoriaModel:

    @staticmethod
    def get_all() -> list:
        return execute_query("SELECT id, nombre FROM categorias ORDER BY nombre", fetch=True)

    @staticmethod
    def create(nombre: str) -> int:
        return execute_query(
            "INSERT INTO categorias (nombre) VALUES (%s)", (nombre,)
        )


class MovimientoModel:

    @staticmethod
    def create(producto_id: int, nombre_producto: str, tipo: str,
               cantidad: int, motivo: str, usuario_id: int) -> None:
        execute_query(
            "INSERT INTO movimientos_stock "
            "(producto_id, nombre_producto, tipo, cantidad, motivo, usuario_id) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (producto_id, nombre_producto, tipo, cantidad, motivo, usuario_id)
        )

    @staticmethod
    def get_all() -> list:
        return execute_query("""
            SELECT m.fecha, m.nombre_producto, m.tipo, m.cantidad, m.motivo,
                   IFNULL(u.nombre_completo,'–') as usuario_nombre
            FROM movimientos_stock m
            LEFT JOIN usuarios u ON m.usuario_id=u.id
            ORDER BY m.fecha DESC
        """, fetch=True)
