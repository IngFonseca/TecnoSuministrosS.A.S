"""
CONTROLADOR – Inventario
Responsabilidad: lógica de negocio para productos, categorías y movimientos de stock.
"""
from models.producto_model import ProductoModel, CategoriaModel, MovimientoModel
from utils import logger
from utils.pdf_generator import reporte_inventario


class InventarioController:

    # ── Categorías ────────────────────────────────────────────────────────────

    @staticmethod
    def get_categorias() -> list:
        return CategoriaModel.get_all()

    @staticmethod
    def crear_categoria(nombre: str, usuario: dict) -> tuple[bool, str]:
        nombre = nombre.strip()
        if not nombre:
            return False, "El nombre de la categoría es obligatorio."
        try:
            CategoriaModel.create(nombre)
            logger.log(usuario["id"], usuario["nombre_completo"],
                       f"Creó categoría: {nombre}", "Inventario")
            return True, "Categoría creada."
        except Exception as e:
            return False, f"Error al crear categoría: {e}"

    # ── Productos ─────────────────────────────────────────────────────────────

    @staticmethod
    def listar(buscar: str = "", categoria: str = "") -> list:
        return ProductoModel.get_all(buscar, categoria)

    @staticmethod
    def get_por_id(producto_id: int) -> dict | None:
        return ProductoModel.get_by_id(producto_id)

    @staticmethod
    def crear(nombre: str, cantidad_str: str, precio_str: str,
              categoria_id, proveedor_id, usuario: dict) -> tuple[bool, str]:
        nombre = nombre.strip()
        if not nombre:
            return False, "El nombre es obligatorio."
        try:
            cantidad = int(cantidad_str)
            precio   = float(precio_str)
            if cantidad < 0 or precio < 0:
                raise ValueError
        except ValueError:
            return False, "Cantidad y precio deben ser números positivos."

        codigo = ProductoModel.create(nombre, cantidad, precio, categoria_id, proveedor_id)
        # Registrar movimiento de entrada inicial
        prod = ProductoModel.get_all(buscar=nombre)
        prod_id = next((p["id"] for p in prod if p["codigo"] == codigo), None)
        if prod_id and cantidad > 0:
            MovimientoModel.create(prod_id, nombre, "entrada", cantidad, "Stock inicial", usuario["id"])
        logger.log(usuario["id"], usuario["nombre_completo"],
                   f"Registró producto: {codigo} – {nombre}", "Inventario")
        return True, f"Producto {codigo} registrado."

    @staticmethod
    def editar(producto_id: int, nombre: str, cantidad_str: str, precio_str: str,
               categoria_id, proveedor_id, usuario: dict) -> tuple[bool, str]:
        nombre = nombre.strip()
        if not nombre:
            return False, "El nombre es obligatorio."
        try:
            cantidad = int(cantidad_str)
            precio   = float(precio_str)
        except ValueError:
            return False, "Cantidad y precio deben ser números válidos."

        ProductoModel.update(producto_id, nombre, cantidad, precio, categoria_id, proveedor_id)
        logger.log(usuario["id"], usuario["nombre_completo"],
                   f"Editó producto: {nombre}", "Inventario")
        return True, "Producto actualizado."

    @staticmethod
    def eliminar(producto_id: int, nombre: str, usuario: dict) -> None:
        ProductoModel.delete(producto_id)
        logger.log(usuario["id"], usuario["nombre_completo"],
                   f"Eliminó producto: {nombre}", "Inventario")

    # ── Movimientos de stock ──────────────────────────────────────────────────

    @staticmethod
    def registrar_movimiento(producto_id: int, tipo: str,
                             cantidad_str: str, motivo: str,
                             usuario: dict) -> tuple[bool, str]:
        try:
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            return False, "Ingresa una cantidad válida (entero positivo)."

        stock_actual = ProductoModel.get_stock(producto_id)
        prod = ProductoModel.get_by_id(producto_id)
        nombre = prod["nombre"] if prod else ""

        if tipo == "salida" and cantidad > stock_actual:
            return False, f"Stock insuficiente. Disponible: {stock_actual}"

        delta = cantidad if tipo == "entrada" else -cantidad
        ProductoModel.update_stock(producto_id, delta)
        MovimientoModel.create(producto_id, nombre, tipo,
                               cantidad, motivo or tipo.capitalize(), usuario["id"])
        logger.log(usuario["id"], usuario["nombre_completo"],
                   f"{tipo.capitalize()} de {cantidad} uds – {nombre}", "Inventario")
        return True, "Movimiento registrado."

    # ── Reporte ───────────────────────────────────────────────────────────────

    @staticmethod
    def exportar_pdf(usuario: dict) -> str:
        rows = ProductoModel.get_para_reporte()
        ruta = reporte_inventario(rows)
        logger.log(usuario["id"], usuario["nombre_completo"],
                   "Exportó PDF de inventario", "Inventario")
        return ruta
