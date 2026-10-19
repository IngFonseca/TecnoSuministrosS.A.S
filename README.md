# Sistema de Gestión de Inventario y Ventas - TecnoSuministros S.A.S.

Aplicación de escritorio para la gestión integral de inventario, ventas, proveedores y trabajadores de TecnoSuministros S.A.S. El sistema permite administrar productos y existencias, registrar ventas, controlar movimientos de stock, gestionar proveedores y usuarios, generar reportes en PDF y manejar diferentes roles de acceso.

El proyecto está construido siguiendo el patrón MVC (Modelo - Vista - Controlador) y se conecta a una API REST propia ([tecnosuministros-api](https://github.com/IngFonseca/tecnosuministros-api)), que es el único componente con acceso a la base de datos.

## Descripción

TecnoSuministros S.A.S. es un sistema de gestión empresarial desarrollado para centralizar y facilitar las operaciones relacionadas con el inventario y las ventas.

La aplicación permite administrar productos, categorías, proveedores, usuarios y ventas desde una interfaz gráfica desarrollada con Tkinter. También incorpora un sistema de autenticación y autorización basado en roles, control de movimientos de inventario, generación de reportes en formato PDF y registro de las actividades realizadas por los usuarios.

La aplicación **no se conecta directamente a la base de datos**: se comunica con la API mediante HTTPS usando un token de sesión. Las credenciales de la base de datos y del correo viven únicamente en el servidor, por lo que el ejecutable puede compartirse sin exponerlas. Las contraseñas se cifran con bcrypt en el servidor.

```text
App de escritorio ──HTTPS + token──► API (FastAPI) ──► MySQL
   (este proyecto)                  (tecnosuministros-api)
```

El proyecto sigue una arquitectura MVC, donde:

- **Modelo:** gestiona las entidades y se comunica con la API para obtener y guardar datos.
- **Vista:** proporciona la interfaz gráfica desarrollada con Tkinter.
- **Controlador:** contiene las validaciones y coordina la comunicación entre las vistas y los modelos.

Esta separación permite mantener el código organizado y facilita futuras modificaciones o ampliaciones del sistema.

## Características

- Sistema de autenticación y registro de usuarios
- Gestión de usuarios y trabajadores
- Sistema de roles y permisos (verificados en el servidor)
- Gestión completa de productos
- Gestión de categorías
- Control de inventario y existencias
- Registro de entradas y salidas de stock
- Gestión de proveedores
- Registro y gestión de ventas
- Carrito de compras
- Cálculo automático de descuentos
- Aplicación automática del IVA del 19%
- Validación de stock antes y durante la venta
- Dashboard con métricas generales del sistema
- Registro de actividad de los usuarios
- Generación de reportes en formato PDF
- Envío de correos electrónicos automáticos (desde la API)
- Sesiones con token y contraseñas protegidas mediante bcrypt
- Ejecutable para Windows sin credenciales incluidas
- Arquitectura MVC para facilitar el mantenimiento y escalabilidad

## Arquitectura MVC

El sistema implementa el patrón Modelo - Vista - Controlador (MVC) para separar las responsabilidades de cada componente.

### Modelo

La capa de modelo se encarga de representar las entidades del sistema y de comunicarse con la API para consultar y guardar la información.

Incluye:

- Gestión de usuarios
- Gestión de productos
- Gestión de categorías
- Gestión de ventas
- Gestión de proveedores
- Gestión de movimientos de inventario

Los modelos realizan peticiones HTTP a la API mediante `utils/api_client.py`. No acceden a la base de datos ni contienen lógica relacionada con la interfaz gráfica.

### Vista

La capa de vista proporciona la interfaz gráfica de la aplicación utilizando Tkinter.

Incluye:

- Inicio de sesión y registro
- Dashboard
- Inventario
- Ventas
- Proveedores
- Trabajadores
- Reportes

Las vistas no se comunican con la API directamente. Se comunican con los controladores para ejecutar las operaciones necesarias.

### Controlador

La capa de controlador contiene las validaciones de formulario y coordina la comunicación entre las vistas y los modelos.

Incluye controladores para:

- Autenticación
- Dashboard
- Inventario
- Ventas
- Proveedores
- Trabajadores
- Reportes

Los controladores validan la información, manejan los errores devueltos por la API y solicitan al modelo las operaciones necesarias. Las reglas de negocio críticas (precios, descuentos, stock y permisos) se aplican en el servidor.

## Roles y Permisos

El sistema cuenta con cuatro roles principales:

### Gerente

El gerente tiene acceso completo al sistema y es el único rol autorizado para asignar o modificar roles de otros usuarios.

- Acceso al dashboard
- Gestión de inventario
- Gestión de ventas
- Gestión de proveedores
- Gestión de trabajadores
- Generación de reportes PDF
- Asignación y modificación de roles
- Supervisión general del sistema

### Administrador

El administrador puede gestionar las principales operaciones administrativas.

- Acceso al dashboard
- Gestión de inventario
- Gestión de proveedores
- Generación de reportes PDF
- Gestión de productos y stock

### Vendedor

El vendedor está orientado principalmente al proceso de ventas.

- Acceso al dashboard
- Registro de ventas
- Gestión del carrito
- Consulta del historial de ventas

### Bodega

El usuario de bodega está orientado al control físico del inventario.

- Acceso al dashboard
- Control de entradas de productos
- Control de salidas de productos
- Gestión de movimientos de stock
- Consulta del inventario

### Matriz de permisos

| Módulo | Gerente | Administrador | Vendedor | Bodega |
|---|:---:|:---:|:---:|:---:|
| Dashboard | ✅ | ✅ | ✅ | ✅ |
| Inventario | ✅ | ✅ | ❌ | ✅ |
| Ventas | ✅ | ✅ | ✅ | ❌ |
| Proveedores | ✅ | ✅ | ❌ | ❌ |
| Reportes PDF | ✅ | ✅ | ❌ | ❌ |
| Trabajadores | ✅ | ✅ | ❌ | ❌ |
| Asignar roles | ✅ | ❌ | ❌ | ❌ |

Estos permisos los verifica la API en cada petición. Ocultar un botón en la interfaz no es la única barrera de seguridad.

## Reglas de Negocio

### Ventas

- Se valida la disponibilidad de stock antes de agregar productos al carrito.
- El stock se valida nuevamente en el servidor al finalizar la venta.
- Se aplica un descuento automático del 5% cuando la venta supera las 10 unidades totales.
- Se aplica un IVA del 19% sobre el subtotal después del descuento.
- La aplicación solo envía qué producto y cuántas unidades se venden. Los precios, el descuento y el IVA los calcula el servidor con los datos de la base.
- Cada venta se registra en una única transacción: o se guarda completa (venta, stock y movimientos) o no se guarda nada.

### Inventario

- Las entradas y salidas de productos quedan registradas.
- Los movimientos de stock almacenan información sobre el producto, cantidad, motivo y usuario responsable.
- Cuando una venta deja el stock de un producto en 5 unidades o menos, la API genera una alerta al proveedor correspondiente.

### Usuarios

- Solo el gerente puede asignar o modificar roles.
- Las cuentas nuevas quedan sin rol y no pueden ingresar hasta que el gerente les asigne uno.
- Un usuario no puede eliminar su propia cuenta.
- Las contraseñas se almacenan utilizando bcrypt.
- Las actividades realizadas por los usuarios quedan registradas en el sistema.

## Tecnologías

- Lenguaje: Python 3.10+
- Interfaz gráfica: Tkinter
- Comunicación con la API: requests
- Generación de PDF: fpdf2
- Procesamiento de imágenes: Pillow
- Empaquetado: PyInstaller
- Servidor: API REST con FastAPI (repositorio [tecnosuministros-api](https://github.com/IngFonseca/tecnosuministros-api))
- Base de datos: MySQL (accedida únicamente desde la API)
- Arquitectura: MVC (Modelo - Vista - Controlador)

## Requisitos

### Usuario final

- Windows
- Conexión a internet

### Desarrollador

- Python >= 3.10
- pip
- Una API de TecnoSuministros en funcionamiento (local o desplegada). Consulta el repositorio [tecnosuministros-api](https://github.com/IngFonseca/tecnosuministros-api).

## Instalación

### Uso rápido (usuarios finales)

La base de datos y la API ya están desplegadas en la nube, por lo que no es necesario instalar Python ni MySQL.

1. Descarga `TecnoSuministros.exe` desde la sección [Releases](https://github.com/IngFonseca/TecnoSuministrosS.A.S/releases) del repositorio.
2. Haz doble clic en el archivo.
3. Inicia sesión con las credenciales de prueba proporcionadas por el autor.

Notas:

- La primera vez puede tardar hasta un minuto en conectar, porque el servidor gratuito se "duerme" cuando no se usa.
- Windows puede mostrar el aviso "Windows protegió su PC", porque el ejecutable no tiene firma digital. Pulsa **Más información → Ejecutar de todos modos**.
- Todos los usuarios comparten la misma base de datos. Los datos son de demostración.
- Los reportes PDF se guardan en `Documentos\TecnoSuministros\reports`.

### Instalación para desarrolladores

Clona el repositorio:

```bash
git clone https://github.com/IngFonseca/TecnoSuministrosS.A.S.git
cd TecnoSuministrosS.A.S
```

Crea y activa un entorno virtual:

En Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

En Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Indica la dirección de la API. La aplicación la busca en este orden:

1. Variable de entorno `TECNO_API_URL`
2. Archivo `api_url.txt` junto al programa
3. Valor `DEFAULT_API_URL` en `utils/config.py`

En Windows:

```bash
set TECNO_API_URL=http://127.0.0.1:8000
```

En Linux / macOS:

```bash
export TECNO_API_URL=http://127.0.0.1:8000
```

Ejecuta la aplicación:

```bash
python main.py
```

La dirección de la API no es un secreto. La aplicación no contiene contraseñas de base de datos ni de correo.

### Generar el ejecutable

1. Edita `utils/config.py` y escribe la URL de tu API en `DEFAULT_API_URL`.
2. Instala PyInstaller y genera el ejecutable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name TecnoSuministros main.py
```

El resultado queda en `dist/TecnoSuministros.exe`. Los archivos `dist/` y `build/` no se suben al repositorio. El ejecutable se publica en la sección Releases.

## Uso

Ejecuta la aplicación con el ejecutable, o desde la raíz del proyecto:

```bash
python main.py
```

Al iniciar la aplicación se presenta el sistema de autenticación. El usuario debe ingresar sus credenciales para acceder al sistema.

Después del inicio de sesión, el sistema identifica el rol del usuario y habilita únicamente los módulos correspondientes a sus permisos.

### Dashboard

El dashboard muestra información general del sistema y métricas relacionadas con las operaciones realizadas.

Dependiendo del rol, el usuario puede acceder a diferentes módulos desde el menú principal.

### Gestión de Inventario

Permite:

- Consultar productos.
- Registrar productos.
- Actualizar productos.
- Administrar categorías.
- Controlar existencias.
- Registrar entradas de stock.
- Registrar salidas de stock.
- Consultar movimientos de inventario.

### Gestión de Ventas

El módulo de ventas permite:

- Consultar productos disponibles.
- Agregar productos al carrito.
- Modificar cantidades.
- Validar disponibilidad.
- Aplicar descuentos automáticamente.
- Calcular el IVA.
- Finalizar la venta.
- Consultar el historial de ventas.

### Gestión de Proveedores

Permite administrar la información de los proveedores:

- Nombre
- Teléfono
- Correo electrónico
- Tipo de producto

### Gestión de Trabajadores

Permite consultar y administrar los usuarios registrados en el sistema.

El gerente puede asignar y modificar los roles de los trabajadores.

### Reportes

El sistema permite generar reportes en formato PDF con información organizada y encabezados institucionales.

## Reportes PDF

El sistema incluye diferentes tipos de reportes:

### Reporte de Ventas

Incluye:

- Fecha
- Producto
- Cantidad
- Precio unitario
- Descuento
- IVA
- Total

### Reporte de Inventario

Incluye:

- Código
- Nombre
- Categoría
- Proveedor
- Cantidad
- Precio

### Reporte de Movimientos de Stock

Incluye:

- Fecha
- Producto
- Tipo de movimiento
- Cantidad
- Motivo
- Usuario responsable

### Reporte de Proveedores

Incluye:

- Nombre
- Teléfono
- Correo
- Tipo de producto

Todos los reportes cuentan con encabezado institucional y fecha de generación.

## Correos Automáticos

El envío de correos lo realiza la API, no la aplicación de escritorio. Se envían notificaciones para los siguientes eventos:

| Evento | Destinatario |
|---|---|
| Nuevo usuario registrado | Gerente |
| Registro de nuevo usuario | Usuario |
| Asignación inicial de rol | Usuario |
| Venta con stock ≤ 5 unidades | Proveedor |

Para utilizar esta funcionalidad se deben configurar las variables de correo en el servidor. Consulta el repositorio [tecnosuministros-api](https://github.com/IngFonseca/tecnosuministros-api).

## Estructura del Proyecto

```text
TecnoSuministrosS.A.S/
│
├── main.py                              # Punto de entrada de la aplicación
├── main_window.py                       # Ventana principal y navegación
├── requirements.txt                     # Dependencias del proyecto
├── .gitignore                           # Archivos excluidos de Git
│
├── models/                              # MODELO
│   ├── usuario_model.py                 # Usuarios (login, registro y gestión) vía API
│   ├── producto_model.py                # Productos, categorías y movimientos vía API
│   ├── venta_model.py                   # Ventas vía API
│   └── proveedor_model.py               # Proveedores vía API
│
├── controllers/                         # CONTROLADOR
│   ├── auth_controller.py               # Login, registro y validaciones
│   ├── dashboard_controller.py          # Métricas del sistema
│   ├── inventario_controller.py         # Lógica de inventario y stock
│   ├── ventas_controller.py             # Carrito, vista previa de totales y ventas
│   ├── proveedores_controller.py        # Gestión de proveedores
│   ├── trabajadores_controller.py       # Usuarios y roles
│   └── reportes_controller.py           # Generación de reportes
│
├── views/                               # VISTA
│   ├── auth_view.py                     # Login y registro
│   ├── dashboard_view.py                # Dashboard
│   ├── inventario_view.py               # Gestión de inventario
│   ├── ventas_view.py                   # Carrito e historial
│   ├── proveedores_view.py              # Gestión de proveedores
│   ├── trabajadores_view.py             # Gestión de trabajadores
│   └── reportes_view.py                 # Generación de reportes
│
├── utils/                               # UTILIDADES
│   ├── api_client.py                    # Cliente HTTP de la API y token de sesión
│   ├── config.py                        # Dirección de la API y carpeta de reportes
│   ├── logger.py                        # Registro de eventos del cliente
│   ├── pdf_generator.py                 # Generación de PDF
│   └── theme.py                         # Tema y estilos de la aplicación
│
└── reports/                             # Reportes PDF generados (modo desarrollo)
```

## Seguridad

El sistema incorpora diferentes mecanismos de seguridad:

- La aplicación no contiene credenciales de base de datos ni de correo.
- Contraseñas protegidas mediante bcrypt (en el servidor).
- Las contraseñas nunca se almacenan en texto plano.
- Sesiones con token que expira automáticamente.
- El token de sesión se guarda solo en memoria y se elimina al cerrar sesión.
- Bloqueo temporal tras varios intentos fallidos de inicio de sesión.
- Se registra la actividad realizada por los usuarios.
- Control de acceso basado en roles, verificado por el servidor en cada petición.
- Solo el gerente puede asignar o modificar roles.
- Un usuario no puede eliminar su propia cuenta.

**Importante:** nunca se deben subir credenciales reales, contraseñas, claves de correo o archivos `.env` a GitHub.

## Datos y Archivos Generados

En modo desarrollo, la carpeta `reports/` almacena los archivos PDF generados por la aplicación. En el ejecutable, los reportes se guardan en `Documentos\TecnoSuministros\reports`.

Los archivos generados automáticamente pueden excluirse del control de versiones mediante `.gitignore`. De igual manera, los directorios `__pycache__/`, `build/`, `dist/` y los archivos `.pyc` o `.spec` son generados automáticamente y no deben versionarse.

## Roadmap

- Mejorar el dashboard con estadísticas y gráficos adicionales.
- Incorporar nuevos tipos de reportes.
- Implementar filtros avanzados para inventario y ventas.
- Mejorar el sistema de notificaciones por correo.
- Incorporar exportación de información a Excel.
- Ampliar el sistema de auditoría y trazabilidad.
- Firmar digitalmente el ejecutable.
- Posible migración futura a una interfaz web reutilizando la misma API.

## Autor

Juan Fernando Fonseca Martínez

## Licencia

Este proyecto no especifica una licencia por el momento.

## Soporte

Para reportar problemas o sugerir mejoras:

- Abre un Issue en GitHub.
- Describe claramente el problema encontrado.
- Incluye los pasos necesarios para reproducirlo.
- Si es posible, proporciona mensajes de error o capturas de pantalla.
