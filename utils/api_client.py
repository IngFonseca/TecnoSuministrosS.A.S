import re
import threading
from datetime import datetime

import requests

from utils.config import get_api_url


class ApiError(Exception):
    """Error de la API o de conexión. `detail` es un texto listo para mostrar."""

    def __init__(self, detail: str, status: int = 0):
        super().__init__(detail)
        self.detail = detail
        self.status = status


_token: str | None = None
_session = requests.Session()
_TIMEOUT = (15, 90)   # Render gratis puede tardar en "despertar"

_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
_CAMPOS_FECHA = {"fecha", "fecha_creacion"}


def set_token(token: str | None) -> None:
    global _token
    _token = token


def clear_token() -> None:
    set_token(None)


def _convertir_fechas(obj):
    """La API manda las fechas como texto; las vistas esperan objetos datetime."""
    if isinstance(obj, list):
        return [_convertir_fechas(x) for x in obj]
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in _CAMPOS_FECHA and isinstance(v, str) and _ISO.match(v):
                try:
                    v = datetime.fromisoformat(v)
                except ValueError:
                    pass
            else:
                v = _convertir_fechas(v)
            out[k] = v
        return out
    return obj


def _mensaje_error(resp: requests.Response) -> str:
    try:
        detail = resp.json().get("detail")
    except Exception:
        detail = None
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list):  # errores de validación (422)
        partes = []
        for d in detail:
            campo = ".".join(str(x) for x in d.get("loc", [])[1:])
            partes.append(f"{campo}: {d.get('msg', 'inválido')}" if campo else d.get("msg", "inválido"))
        return "Datos inválidos – " + "; ".join(partes)
    return f"Error del servidor ({resp.status_code})."


def request(method: str, path: str, *, json=None, params=None):
    headers = {"Authorization": f"Bearer {_token}"} if _token else {}
    try:
        resp = _session.request(method, get_api_url() + path, json=json,
                                params=params, headers=headers, timeout=_TIMEOUT)
    except requests.exceptions.ConnectTimeout:
        raise ApiError("El servidor tardó demasiado en responder.\n"
                       "Si acaba de iniciarse puede tardar hasta un minuto: inténtalo de nuevo.")
    except requests.exceptions.ReadTimeout:
        raise ApiError("El servidor tardó demasiado en responder. Inténtalo de nuevo.")
    except requests.exceptions.ConnectionError:
        raise ApiError("No se pudo conectar con el servidor.\n"
                       "Revisa tu conexión a internet e inténtalo de nuevo.")
    except requests.exceptions.RequestException as exc:
        raise ApiError(f"Error de comunicación: {exc}")

    if resp.status_code >= 400:
        raise ApiError(_mensaje_error(resp), resp.status_code)
    if not resp.content:
        return None
    return _convertir_fechas(resp.json())


def get(path, params=None):          return request("GET", path, params=params)
def post(path, json=None):           return request("POST", path, json=json)
def put(path, json=None):            return request("PUT", path, json=json)
def delete(path):                    return request("DELETE", path)


def warmup() -> None:
    """Despierta el servidor en segundo plano mientras el usuario escribe su clave."""
    def _ping():
        try:
            _session.get(get_api_url() + "/health", timeout=(15, 90))
        except Exception:
            pass
    threading.Thread(target=_ping, daemon=True).start()