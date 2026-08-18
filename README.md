# TecnoSuministros S.A.S. — Arquitectura MVC 🏗️
**Sistema de Gestión de Inventario y Ventas**  
Python · Tkinter · MySQL · FPDF · bcrypt · Patrón MVC · 2025

---

## 🏗️ Arquitectura Modelo–Vista–Controlador

```
┌─────────────────────────────────────────────────────────────┐
│                        USUARIO                              │
│                     (interacción)                           │
└───────────────────────────┬─────────────────────────────────┘
                            │ eventos UI
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    VISTA  (views/)                          │
│  auth_view · dashboard_view · inventario_view · ventas_view │
│  proveedores_view · trabajadores_view · reportes_view       │
│                                                             │
│  Solo Tkinter. No accede a la BD directamente.              │
│  Llama al Controlador y muestra lo que este retorna.        │
└───────────────────────────┬─────────────────────────────────┘
                            │ llama a métodos del controlador
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                CONTROLADOR  (controllers/)                  │
│  auth · dashboard · inventario · ventas · proveedores       │
│  trabajadores · reportes                                    │
│                                                             │
│  Lógica de negocio pura. Sin importar Tkinter.              │
│  Valida, orquesta, llama al Modelo, retorna resultados.     │
└───────────────────────────┬─────────────────────────────────┘
                            │ consulta / persiste datos
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   MODELO  (models/)                         │
│  usuario_model · producto_model · venta_model               │
│  proveedor_model                                            │
│                                                             │
│  Solo SQL. No tiene lógica de negocio ni UI.                │
│  Representa y persiste entidades del dominio.               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Estructura del proyecto

```
tecnosuministros_mvc/
│
├── main.py                          ← Punto de entrada
├── main_window.py                   ← Shell: sidebar + navegación por rol
├── setup_db.py                      ← Inicialización de BD y gerente
├── requirements.txt
├── .env.example
├── .gitignore
│
├── models/                          ── MODELO ──
│   ├── usuario_model.py             CRUD usuarios, hashing
│   ├── producto_model.py            CRUD productos, categorías, movimientos
│   ├── venta_model.py               CRUD ventas
│   └── proveedor_model.py           CRUD proveedores
│
├── controllers/                     ── CONTROLADOR ──
│   ├── auth_controller.py           Login, registro, validaciones
│   ├── dashboard_controller.py      Métricas del sistema
│   ├── inventario_controller.py     Lógica de inventario y stock
│   ├── ventas_controller.py         Carrito, cálculos, finalización
│   ├── proveedores_controller.py    Lógica CRUD proveedores
│   ├── trabajadores_controller.py   Gestión usuarios y roles
│   └── reportes_controller.py       Orquestación de PDFs
│
├── views/                           ── VISTA ──
│   ├── auth_view.py                 Login + formulario de registro
│   ├── dashboard_view.py            Tarjetas de métricas + tabla ventas
│   ├── inventario_view.py           Tabla productos + formularios
│   ├── ventas_view.py               Carrito + historial
│   ├── proveedores_view.py          Tabla proveedores + formularios
│   ├── trabajadores_view.py         Tabla usuarios + asignación de roles
│   └── reportes_view.py             Tarjetas de generación de PDF
│
├── utils/                           ── UTILIDADES ──
│   ├── db.py                        Conexión MySQL
│   ├── email_service.py             Bienvenida, alertas, notif. gerente
│   ├── logger.py                    Log de actividad en BD
│   ├── pdf_generator.py             Reportes PDF con encabezado
│   └── theme.py                     Colores, fuentes y estilos UI
│
└── reports/                         PDFs generados (auto-creado)
```

---

## 🚀 Instalación y uso

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Copiar y configurar variables de entorno
cp .env.example .env
# Editar .env con tus datos MySQL y Gmail App Password

# 3. Inicializar base de datos y crear gerente inicial
python setup_db.py

# 4. Ejecutar la aplicación
python main.py
```

---

## 🔐 Roles y permisos

| Módulo            | Gerente | Admin | Vendedor | Bodega |
|-------------------|:-------:|:-----:|:--------:|:------:|
| Dashboard         | ✅      | ✅    | ✅       | ✅     |
| Inventario        | ✅      | ✅    | ❌       | ✅     |
| Ventas            | ✅      | ✅    | ✅       | ❌     |
| Proveedores       | ✅      | ✅    | ❌       | ❌     |
| Reportes PDF      | ✅      | ✅    | ❌       | ❌     |
| Trabajadores      | ✅      | ✅    | ❌       | ❌     |
| **Asignar roles** | **✅ Solo Gerente** | ❌ | ❌ | ❌ |

### Tarea por rol (mostrada en Dashboard)
- **Gerente:** Gestionar trabajadores, asignar roles y supervisar el sistema.
- **Administrador:** Administrar inventario, proveedores y generar reportes PDF.
- **Vendedor:** Registrar ventas, gestionar el carrito y consultar el dashboard.
- **Bodega:** Controlar entradas/salidas de stock y movimientos de inventario.

---

## 📧 Correos automáticos

| Evento | Destinatario |
|--------|-------------|
| Nuevo usuario registrado | Gerente (alerta de acción requerida) |
| Nuevo usuario registrado | Usuario (bienvenida con credenciales) |
| Gerente asigna rol por primera vez | Usuario (notificación con rol) |
| Venta con stock resultante ≤ 5 uds | Proveedor del producto (alerta) |

---

## 🛒 Reglas de negocio (en Controladores)

- **Descuento por volumen:** 5% automático si la venta supera 10 unidades totales.
- **IVA:** 19% aplicado sobre el subtotal con descuento.
- **Stock:** validado antes de agregar al carrito y al finalizar la venta.
- **Roles:** solo el **gerente** puede asignar o cambiar roles (validación en `TrabajadoresController`).
- **Contraseñas:** cifradas con **bcrypt** — nunca texto plano en BD.

---

## 📋 Reportes PDF disponibles

Todos con **encabezado institucional**, fecha y filas alternadas:

| Reporte | Campos |
|---------|--------|
| Ventas | fecha, producto, cantidad, precio unitario, descuento, IVA, total |
| Inventario | código, nombre, categoría, proveedor, cantidad, precio |
| Movimientos de stock | fecha, producto, tipo, cantidad, motivo, usuario |
| Proveedores | nombre, teléfono, correo, tipo de producto |

---

## 🔒 Seguridad

- Contraseñas con **bcrypt** (sin texto plano en BD)
- Credenciales en **`.env`** excluido de Git con `.gitignore`
- **Log de actividad** completo: todas las acciones quedan en `log_actividad`
- Protección: un usuario no puede eliminar su propia cuenta
