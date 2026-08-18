"""
CONTROLADOR – Ventas
Responsabilidad: lógica de carrito, cálculo de totales, registro de venta y alertas.
"""
from models.producto_model import ProductoModel, MovimientoModel
from models.venta_model import VentaModel
from utils import logger
from utils.email_service import send_low_stock_alert
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
        Registra la venta, descuenta stock y envía alertas.
        Retorna (exito, mensaje, total).
        """
        if self.esta_vacio():
            return False, "El carrito está vacío.", 0.0

        totales  = self.calcular_totales()
        desc_pct = totales["desc_pct"]
        total    = totales["total"]

        productos_bajo_stock = []

        for item in self.items:
            item_total = item["precio"] * item["cantidad"] * (1 - desc_pct / 100) * (1 + IVA_PCT / 100)
            VentaModel.create(
                item["producto_id"], item["nombre"], item["cantidad"],
                item["precio"], desc_pct, IVA_PCT, item_total, usuario["id"]
            )
            ProductoModel.update_stock(item["producto_id"], -item["cantidad"])
            MovimientoModel.create(
                item["producto_id"], item["nombre"], "salida",
                item["cantidad"], "Venta", usuario["id"]
            )
            # Revisar stock bajo
            nuevo_stock = ProductoModel.get_stock(item["producto_id"])
            if nuevo_stock <= 5:
                prod_info = ProductoModel.get_by_id(item["producto_id"])
                if prod_info and prod_info.get("proveedor_id"):
                    from models.proveedor_model import ProveedorModel
                    prov = ProveedorModel.get_by_id(prod_info["proveedor_id"])
                    if prov and prov.get("correo"):
                        productos_bajo_stock.append({
                            "proveedor_correo": prov["correo"],
                            "proveedor_nombre": prov["nombre"],
                            "codigo": prod_info["codigo"],
                            "nombre": item["nombre"],
                            "cantidad": nuevo_stock,
                        })

        logger.log(usuario["id"], usuario["nombre_completo"],
                   f"Venta por ${total:,.0f} – {len(self.items)} ítem(s)", "Ventas")

        # Alertas de stock bajo agrupadas por proveedor
        if productos_bajo_stock:
            from collections import defaultdict
            por_prov = defaultdict(list)
            for p in productos_bajo_stock:
                por_prov[(p["proveedor_correo"], p["proveedor_nombre"])].append(p)
            for (correo, nombre), prods in por_prov.items():
                send_low_stock_alert(correo, nombre, prods)

        self.vaciar()
        return True, "Venta registrada exitosamente.", total


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
