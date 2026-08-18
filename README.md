# Sistema de Gestión de Inventario y Ventas - TecnoSuministros S.A.S.

Aplicación de escritorio para la gestión integral de inventario, ventas, proveedores y trabajadores de TecnoSuministros S.A.S. El sistema permite administrar productos y existencias, registrar ventas, controlar movimientos de stock, gestionar proveedores y usuarios, generar reportes en PDF y manejar diferentes roles de acceso.

El proyecto está construido siguiendo el patrón **MVC (Modelo - Vista - Controlador)**, separando la interfaz gráfica, la lógica de negocio y el acceso a los datos para facilitar su mantenimiento y futuras extensiones.

## Descripción

TecnoSuministros S.A.S. es un sistema de gestión empresarial desarrollado para centralizar y facilitar las operaciones relacionadas con el inventario y las ventas.

La aplicación permite administrar productos, categorías, proveedores, usuarios y ventas desde una interfaz gráfica desarrollada con **Tkinter**. También incorpora un sistema de autenticación y autorización basado en roles, control de movimientos de inventario, generación de reportes en formato PDF y registro de las actividades realizadas por los usuarios.

El sistema utiliza **MySQL** como sistema de gestión de base de datos y **bcrypt** para proteger las contraseñas almacenadas.

El proyecto sigue una arquitectura **MVC**, donde:

- **Modelo:** gestiona las entidades y el acceso a la base de datos.
- **Vista:** proporciona la interfaz gráfica desarrollada con Tkinter.
- **Controlador:** contiene la lógica de negocio y coordina la comunicación entre las vistas y los modelos.

Esta separación permite mantener el código organizado y facilita futuras modificaciones o ampliaciones del sistema.

## Características

- Sistema de autenticación y registro de usuarios
- Gestión de usuarios y trabajadores
- Sistema de roles y permisos
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
- Envío de correos electrónicos automáticos
- Contraseñas protegidas mediante `bcrypt`
- Arquitectura MVC para facilitar el mantenimiento y escalabilidad

## Arquitectura MVC

El sistema implementa el patrón **Modelo - Vista - Controlador (MVC)** para separar las responsabilidades de cada componente.

### Modelo

La capa de modelo se encarga de representar las entidades del sistema y realizar las operaciones directamente relacionadas con la base de datos.

Incluye:

- Gestión de usuarios
- Gestión de productos
- Gestión de categorías
- Gestión de ventas
- Gestión de proveedores
- Gestión de movimientos de inventario

Los modelos trabajan con MySQL y no contienen lógica relacionada con la interfaz gráfica.

### Vista

La capa de vista proporciona la interfaz gráfica de la aplicación utilizando **Tkinter**.

Incluye:

- Inicio de sesión y registro
- Dashboard
- Inventario
- Ventas
- Proveedores
- Trabajadores
- Reportes

Las vistas no acceden directamente a la base de datos. Se comunican con los controladores para ejecutar las operaciones necesarias.

### Controlador

La capa de controlador contiene la lógica de negocio del sistema y coordina la comunicación entre las vistas y los modelos.

Incluye controladores para:

- Autenticación
- Dashboard
- Inventario
- Ventas
- Proveedores
- Trabajadores
- Reportes

Los controladores validan la información, aplican las reglas de negocio y solicitan al modelo las operaciones necesarias.

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

## Reglas de Negocio

### Ventas

- Se valida la disponibilidad de stock antes de agregar productos al carrito.
- Se vuelve a validar el stock al finalizar una venta.
- Se aplica un descuento automático del **5%** cuando la venta supera las 10 unidades totales.
- Se aplica un **IVA del 19%** sobre el subtotal después del descuento.

### Inventario

- Las entradas y salidas de productos quedan registradas.
- Los movimientos de stock almacenan información sobre el producto, cantidad, motivo y usuario responsable.
- Cuando una venta deja el stock de un producto en **5 unidades o menos**, se genera una alerta al proveedor correspondiente.

### Usuarios

- Solo el gerente puede asignar o modificar roles.
- Un usuario no puede eliminar su propia cuenta.
- Las contraseñas se almacenan utilizando `bcrypt`.
- Las actividades realizadas por los usuarios quedan registradas en el sistema.

## Tecnologías

- **Lenguaje:** Python 3.10+
- **Interfaz gráfica:** Tkinter
- **Base de datos:** MySQL
- **Conector de base de datos:** `mysql-connector-python`
- **Seguridad de contraseñas:** `bcrypt`
- **Generación de PDF:** `fpdf2`
- **Variables de entorno:** `python-dotenv`
- **Procesamiento de imágenes:** `Pillow`
- **Arquitectura:** MVC (Modelo - Vista - Controlador)

## Requisitos

- Python >= 3.10
- MySQL Server
- pip
- Cuenta de correo Gmail para las funciones de envío de correos
- Gmail App Password para la autenticación del servicio de correo

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/TU_USUARIO/tecnosuministros-mvc.git
   cd tecnosuministros-mvc
   ```

2. Crea y activa un entorno virtual:

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

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

4. Crea el archivo `.env` a partir de `.env.example`:

   En Windows:

   ```bash
   copy .env.example .env
   ```

   En Linux / macOS:

   ```bash
   cp .env.example .env
   ```

5. Configura el archivo `.env` con las credenciales de tu base de datos MySQL y tu cuenta de correo:

   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=tecnosuministros
   DB_USER=root
   DB_PASSWORD=TU_PASSWORD

   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USER=TU_CORREO
   EMAIL_PASSWORD=TU_APP_PASSWORD
   EMAIL_FROM_NAME=TecnoSuministros S.A.S.
   ```

   **Importante:** el archivo `.env` contiene información sensible y no debe subirse a GitHub. El proyecto incluye `.env.example` como plantilla.

6. Inicializa la base de datos:

   ```bash
   python setup_db.py
   ```

   Este proceso configura la base de datos y crea el gerente inicial.

7. Ejecuta la aplicación:

   ```bash
   python main.py
   ```

## Uso

Ejecuta la aplicación desde la raíz del proyecto:

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

1. Consultar productos.
2. Registrar productos.
3. Actualizar productos.
4. Administrar categorías.
5. Controlar existencias.
6. Registrar entradas de stock.
7. Registrar salidas de stock.
8. Consultar movimientos de inventario.

### Gestión de Ventas

El módulo de ventas permite:

1. Consultar productos disponibles.
2. Agregar productos al carrito.
3. Modificar cantidades.
4. Validar disponibilidad.
5. Aplicar descuentos automáticamente.
6. Calcular el IVA.
7. Finalizar la venta.
8. Consultar el historial de ventas.

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

El sistema permite enviar notificaciones mediante correo electrónico para diferentes eventos:

| Evento | Destinatario |
|---|---|
| Nuevo usuario registrado | Gerente |
| Registro de nuevo usuario | Usuario |
| Asignación inicial de rol | Usuario |
| Venta con stock ≤ 5 unidades | Proveedor |

Para utilizar esta funcionalidad se deben configurar correctamente las variables de correo en el archivo `.env`.

## Estructura del Proyecto

```text
tecnosuministros_mvc/
│
├── main.py                              # Punto de entrada de la aplicación
├── main_window.py                       # Ventana principal y navegación
├── setup_db.py                          # Inicialización de la base de datos
├── requirements.txt                     # Dependencias del proyecto
├── .env.example                         # Plantilla de variables de entorno
├── .gitignore                            # Archivos excluidos de Git
│
├── models/                              # MODELO
│   ├── usuario_model.py                 # CRUD de usuarios y hashing
│   ├── producto_model.py                # Productos, categorías y movimientos
│   ├── venta_model.py                   # Gestión de ventas
│   └── proveedor_model.py               # Gestión de proveedores
│
├── controllers/                         # CONTROLADOR
│   ├── auth_controller.py               # Login, registro y validaciones
│   ├── dashboard_controller.py          # Métricas del sistema
│   ├── inventario_controller.py         # Lógica de inventario y stock
│   ├── ventas_controller.py             # Carrito, cálculos y ventas
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
│   ├── db.py                            # Conexión con MySQL
│   ├── email_service.py                 # Servicio de correo
│   ├── logger.py                        # Registro de actividades
│   ├── pdf_generator.py                 # Generación de PDF
│   └── theme.py                         # Tema y estilos de la aplicación
│
└── reports/                             # Reportes PDF generados
```

## Seguridad

El sistema incorpora diferentes mecanismos de seguridad:

- Contraseñas protegidas mediante **bcrypt**.
- Las contraseñas nunca se almacenan en texto plano.
- Las credenciales se manejan mediante variables de entorno.
- El archivo `.env` está incluido en `.gitignore`.
- Se registra la actividad realizada por los usuarios.
- Se implementa control de acceso basado en roles.
- Solo el gerente puede asignar o modificar roles.
- Un usuario no puede eliminar su propia cuenta.

**Importante:** nunca se deben subir credenciales reales, contraseñas, claves de correo o archivos `.env` al repositorio de GitHub.

## Datos y Archivos Generados

La carpeta `reports/` almacena los archivos PDF generados por la aplicación.

Los archivos generados automáticamente pueden excluirse del control de versiones mediante `.gitignore`.

De igual manera, los directorios `__pycache__/` y archivos `.pyc` son generados automáticamente por Python y no deben versionarse.

## Roadmap

- Mejorar el dashboard con estadísticas y gráficos adicionales.
- Incorporar nuevos tipos de reportes.
- Implementar filtros avanzados para inventario y ventas.
- Mejorar el sistema de notificaciones por correo.
- Incorporar exportación de información a Excel.
- Ampliar el sistema de auditoría y trazabilidad.
- Implementar nuevas funcionalidades administrativas.
- Posible desarrollo de una API REST para complementar la aplicación de escritorio.
- Posible migración futura a una interfaz web manteniendo la arquitectura MVC.

## Autor

Juan Fernando Fonseca Martínez

## Licencia

Este proyecto no especifica una licencia por el momento.

## Soporte

Para reportar problemas o sugerir mejoras:

- Abre un **Issue en GitHub**.
- Describe claramente el problema encontrado.
- Incluye los pasos necesarios para reproducirlo.
- Si es posible, proporciona mensajes de error o capturas de pantalla.
