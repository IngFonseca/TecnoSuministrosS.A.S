"""Generador de reportes PDF para TecnoSuministros."""
import os
from datetime import datetime
from fpdf import FPDF

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

AZUL = (26, 58, 92)
AZUL_CLARO = (232, 240, 254)
GRIS = (240, 244, 248)
TEXTO = (51, 51, 51)
BLANCO = (255, 255, 255)


class ReportePDF(FPDF):
    def __init__(self, titulo: str):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.titulo_reporte = titulo
        self.add_page()
        self.set_auto_page_break(auto=True, margin=15)
        self._encabezado()

    def _encabezado(self):
        self.set_fill_color(*AZUL)
        self.rect(0, 0, 297, 30, "F")
        self.set_text_color(*BLANCO)
        self.set_font("Helvetica", "B", 16)
        self.set_xy(10, 8)
        self.cell(0, 8, "TecnoSuministros S.A.S.", ln=True)
        self.set_font("Helvetica", "", 10)
        self.set_xy(10, 17)
        self.cell(0, 6, self.titulo_reporte, ln=True)
        # fecha
        self.set_font("Helvetica", "", 9)
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.set_xy(220, 17)
        self.cell(0, 6, f"Generado: {fecha}", ln=False)
        self.ln(20)
        self.set_text_color(*TEXTO)

    def tabla_encabezado(self, columnas: list, anchos: list):
        self.set_fill_color(*AZUL)
        self.set_text_color(*BLANCO)
        self.set_font("Helvetica", "B", 9)
        for col, ancho in zip(columnas, anchos):
            self.cell(ancho, 8, col, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(*TEXTO)
        self._fila_par = True

    def tabla_fila(self, valores: list, anchos: list):
        self.set_font("Helvetica", "", 9)
        if self._fila_par:
            self.set_fill_color(*GRIS)
        else:
            self.set_fill_color(*BLANCO)
        self._fila_par = not self._fila_par
        for val, ancho in zip(valores, anchos):
            self.cell(ancho, 7, str(val), border=1, fill=True)
        self.ln()

    def guardar(self, nombre_archivo: str) -> str:
        ruta = os.path.join(OUTPUT_DIR, nombre_archivo)
        self.output(ruta)
        return ruta


def reporte_ventas(ventas: list) -> str:
    pdf = ReportePDF("Reporte de Ventas")
    cols = ["Fecha", "Producto", "Cantidad", "P. Unitario", "Descuento %", "IVA %", "Total"]
    anchos = [35, 80, 22, 28, 26, 20, 30]
    pdf.tabla_encabezado(cols, anchos)
    for v in ventas:
        fecha = v["fecha"].strftime("%d/%m/%Y %H:%M") if hasattr(v["fecha"], "strftime") else str(v["fecha"])
        pdf.tabla_fila([
            fecha,
            v.get("nombre_producto", ""),
            v.get("cantidad", ""),
            f"${v.get('precio_unitario', 0):,.0f}",
            f"{v.get('descuento', 0)}%",
            f"{v.get('iva', 19)}%",
            f"${v.get('total', 0):,.0f}",
        ], anchos)
    return pdf.guardar(f"ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")


def reporte_inventario(productos: list) -> str:
    pdf = ReportePDF("Reporte de Inventario")
    cols = ["Código", "Nombre", "Categoría", "Proveedor", "Cantidad", "Precio"]
    anchos = [25, 80, 40, 55, 24, 30]
    pdf.tabla_encabezado(cols, anchos)
    for p in productos:
        pdf.tabla_fila([
            p.get("codigo", ""),
            p.get("nombre", ""),
            p.get("categoria", ""),
            p.get("proveedor", ""),
            p.get("cantidad", 0),
            f"${p.get('precio', 0):,.0f}",
        ], anchos)
    return pdf.guardar(f"inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")


def reporte_proveedores(proveedores: list) -> str:
    pdf = ReportePDF("Reporte de Proveedores")
    cols = ["Nombre", "Teléfono", "Correo", "Tipo de producto"]
    anchos = [60, 35, 60, 100]
    pdf.tabla_encabezado(cols, anchos)
    for p in proveedores:
        pdf.tabla_fila([
            p.get("nombre", ""),
            p.get("telefono", ""),
            p.get("correo", ""),
            p.get("tipo_producto", ""),
        ], anchos)
    return pdf.guardar(f"proveedores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")


def reporte_movimientos(movimientos: list) -> str:
    pdf = ReportePDF("Reporte de Movimientos de Stock (Compras/Entradas)")
    cols = ["Fecha", "Producto", "Tipo", "Cantidad", "Motivo", "Usuario"]
    anchos = [35, 70, 20, 22, 70, 40]
    pdf.tabla_encabezado(cols, anchos)
    for m in movimientos:
        fecha = m["fecha"].strftime("%d/%m/%Y %H:%M") if hasattr(m["fecha"], "strftime") else str(m["fecha"])
        pdf.tabla_fila([
            fecha,
            m.get("nombre_producto", ""),
            m.get("tipo", "").upper(),
            m.get("cantidad", ""),
            m.get("motivo", ""),
            m.get("usuario_nombre", ""),
        ], anchos)
    return pdf.guardar(f"movimientos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
