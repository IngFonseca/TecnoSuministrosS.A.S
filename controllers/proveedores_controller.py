"""
CONTROLADOR – Proveedores
Responsabilidad: lógica de negocio CRUD de proveedores.
"""
from models.proveedor_model import ProveedorModel
from utils import logger
from utils.pdf_generator import reporte_proveedores


class ProveedoresController:

    @staticmethod
    def listar() -> list:
        return ProveedorModel.get_all()

    @staticmethod
    def get_por_id(proveedor_id: int) -> dict | None:
        return ProveedorModel.get_by_id(proveedor_id)

    @staticmethod
    def crear(nombre: str, telefono: str, correo: str,
              tipo: str, usuario: dict) -> tuple[bool, str]:
        nombre = nombre.strip()
        if not nombre:
            return False, "El nombre es obligatorio."
        ProveedorModel.create(nombre, telefono.strip(), correo.strip(), tipo.strip())
        logger.log(usuario["id"], usuario["nombre_completo"],
                   f"Registró proveedor: {nombre}", "Proveedores")
        return True, "Proveedor registrado."

    @staticmethod
    def editar(proveedor_id: int, nombre: str, telefono: str,
               correo: str, tipo: str, usuario: dict) -> tuple[bool, str]:
        nombre = nombre.strip()
        if not nombre:
            return False, "El nombre es obligatorio."
        ProveedorModel.update(proveedor_id, nombre, telefono.strip(), correo.strip(), tipo.strip())
        logger.log(usuario["id"], usuario["nombre_completo"],
                   f"Editó proveedor: {nombre}", "Proveedores")
        return True, "Proveedor actualizado."

    @staticmethod
    def eliminar(proveedor_id: int, nombre: str, usuario: dict) -> None:
        ProveedorModel.delete(proveedor_id)
        logger.log(usuario["id"], usuario["nombre_completo"],
                   f"Eliminó proveedor: {nombre}", "Proveedores")

    @staticmethod
    def exportar_pdf(usuario: dict) -> str:
        rows = ProveedorModel.get_para_reporte()
        ruta = reporte_proveedores(rows)
        logger.log(usuario["id"], usuario["nombre_completo"],
                   "Exportó PDF de proveedores", "Proveedores")
        return ruta
