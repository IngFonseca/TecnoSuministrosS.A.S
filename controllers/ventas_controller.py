"""
CONTROLADOR – Ventas
Responsabilidad: lógica de carrito, cálculo de totales, registro de venta y alertas.
"""
from models.producto_model import ProductoModel
from models.venta_model import VentaModel
from utils import logger
from utils.api_client import ApiError
from utils.pdf_generator import reporte_ventas


DESCUENTO_UMBRAL = 10     # unidades totales para aplicar descuento
DESCUENTO_PCT    = 5.0    # porcentaje de descuento por volumen
IVA_PCT          = 19.0


class CarritoController:
    """Estado del carrito y operaciones sobre él."""

    def __init__(self):
        self.items: list[dict] = []

    # ── Items ─────────────────────────────────────────────────────────────────

    def agregar(self, producto: dict, cantidad: int) -> tuple[bool, str]:
        if cantidad <= 0:
            return False, "La cantidad debe ser mayor a cero."
        # Si ya existe en carrito, sumar
        for item in self.items:
            if item["producto_id"] == producto["id"]:
                nueva = item["cantidad"] + cantidad
                if nueva > producto["cantidad"]:
                    return False, f"Stock insuficiente. Disponible: {producto['cantidad']}"
                item["cantidad"] = nueva
                return True, ""
        if cantidad > producto["cantidad"]:
            return False, f"Stock insuficiente. Disponible: {producto['cantidad']}"
        self.items.append({
            "producto_id": producto["id"],
            "nombre":      producto["nombre"],
            "precio":      float(producto["precio"]),
            "cantidad":    cantidad,
        })
        return True, ""

    def quitar(self, index: int) -> None:
        if 0 <= index < len(self.items):
            self.items.pop(index)

    def vaciar(self) -> None:
        self.items.clear()

    def esta_vacio(self) -> bool:
        return len(self.items) == 0

    # ── Cálculos ──────────────────────────────────────────────────────────────

    def calcular_totales(self) -> dict:
        subtotal   = sum(i["precio"] * i["cantidad"] for i in self.items)
        total_uds  = sum(i["cantidad"] for i in self.items)
        desc_pct   = DESCUENTO_PCT if total_uds > DESCUENTO_UMBRAL else 0.0
        desc_monto = subtotal * (desc_pct / 100)
        sub_desc   = subtotal - desc_monto
        iva_monto  = sub_desc * (IVA_PCT / 100)
        total      = sub_desc + iva_monto
        return {
            "subtotal":   subtotal,
            "desc_pct":   desc_pct,
            "desc_monto": desc_monto,
            "iva_pct":    IVA_PCT,
            "iva_monto":  iva_monto,
            "total":      total,
        }

    # ── Finalizar venta ───────────────────────────────────────────────────────

    def finalizar(self, usuario: dict) -> tuple[bool, str, float]:
        """
        Envía la venta a la API. El SERVIDOR valida el stock, calcula precios,
        descuento e IVA, descuenta el stock y registra los movimientos,
        todo en una sola transacción. Retorna (exito, mensaje, total).
        """
        if self.esta_vacio():
            return False, "El carrito está vacío.", 0.0

        try:
            res = VentaModel.registrar(self.items)
        except ApiError as e:
            return False, e.detail, 0.0

        self.vaciar()
        return True, res["mensaje"], float(res["total"])

class VentasController:

    @staticmethod
    def get_productos_disponibles(categoria: str = "") -> list:
        return ProductoModel.get_disponibles(categoria)

    @staticmethod
    def get_historial(limite: int = 100) -> list:
        return VentaModel.get_recientes(limite)

    @staticmethod
    def exportar_pdf(usuario: dict) -> str:
        rows = VentaModel.get_todas()
        ruta = reporte_ventas(rows)
        logger.log(usuario["id"], usuario["nombre_completo"],
                   "Exportó PDF de ventas", "Ventas")
        return ruta
