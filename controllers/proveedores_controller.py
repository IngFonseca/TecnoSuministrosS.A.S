from models.proveedor_model import ProveedorModel
from utils import logger
from utils.api_client import ApiError
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
        try:
            ProveedorModel.create(nombre, telefono.strip(), correo.strip(), tipo.strip())
        except ApiError as e:
            return False, e.detail
        return True, "Proveedor registrado."

    @staticmethod
    def editar(proveedor_id: int, nombre: str, telefono: str,
               correo: str, tipo: str, usuario: dict) -> tuple[bool, str]:
        nombre = nombre.strip()
        if not nombre:
            return False, "El nombre es obligatorio."
        try:
            ProveedorModel.update(proveedor_id, nombre, telefono.strip(), correo.strip(), tipo.strip())
        except ApiError as e:
            return False, e.detail
        return True, "Proveedor actualizado."

    @staticmethod
    def eliminar(proveedor_id: int, nombre: str, usuario: dict) -> None:
        ProveedorModel.delete(proveedor_id)

    @staticmethod
    def exportar_pdf(usuario: dict) -> str:
        rows = ProveedorModel.get_para_reporte()
        ruta = reporte_proveedores(rows)
        logger.log(usuario["id"], usuario["nombre_completo"],
                   "Exportó PDF de proveedores", "Proveedores")
        return ruta