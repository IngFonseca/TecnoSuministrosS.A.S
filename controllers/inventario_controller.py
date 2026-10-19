from models.producto_model import ProductoModel, CategoriaModel
from utils import logger
from utils.api_client import ApiError
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
            return True, "Categoría creada."
        except ApiError as e:
            return False, e.detail

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

        try:
            codigo = ProductoModel.create(nombre, cantidad, precio, categoria_id, proveedor_id)
        except ApiError as e:
            return False, e.detail
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

        try:
            ProductoModel.update(producto_id, nombre, cantidad, precio, categoria_id, proveedor_id)
        except ApiError as e:
            return False, e.detail
        return True, "Producto actualizado."

    @staticmethod
    def eliminar(producto_id: int, nombre: str, usuario: dict) -> None:
        ProductoModel.delete(producto_id)

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

        try:
            ProductoModel.registrar_movimiento(producto_id, tipo, cantidad, motivo)
        except ApiError as e:
            return False, e.detail
        return True, "Movimiento registrado."

    # ── Reporte ───────────────────────────────────────────────────────────────

    @staticmethod
    def exportar_pdf(usuario: dict) -> str:
        rows = ProductoModel.get_para_reporte()
        ruta = reporte_inventario(rows)
        logger.log(usuario["id"], usuario["nombre_completo"],
                   "Exportó PDF de inventario", "Inventario")
        return ruta