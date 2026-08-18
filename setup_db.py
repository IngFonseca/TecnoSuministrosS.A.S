"""
setup_db.py – Crea la base de datos, tablas y el usuario gerente inicial.
Ejecutar una sola vez antes de iniciar la aplicación por primera vez.
"""
import os, sys
import bcrypt
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def run_setup():
    host     = os.getenv("DB_HOST", "localhost")
    port     = int(os.getenv("DB_PORT", 3306))
    db_name  = os.getenv("DB_NAME", "tecnosuministros")
    db_user  = os.getenv("DB_USER", "root")
    db_pass  = os.getenv("DB_PASSWORD", "")

    print("=" * 55)
    print("  TecnoSuministros S.A.S. – Configuración inicial")
    print("=" * 55)

    # 1. Conectar sin seleccionar BD
    try:
        conn = mysql.connector.connect(host=host, port=port, user=db_user, password=db_pass)
        cursor = conn.cursor()
    except Error as e:
        print(f"\n❌ No se pudo conectar a MySQL: {e}")
        sys.exit(1)

    # 2. Crear base de datos
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute(f"USE `{db_name}`")
    print(f"✅ Base de datos '{db_name}' lista.")

    # 3. Crear tablas
    tablas = [
        """CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre_completo VARCHAR(150) NOT NULL,
            correo VARCHAR(150) UNIQUE NOT NULL,
            usuario VARCHAR(80) UNIQUE NOT NULL,
            contrasena VARCHAR(255) NOT NULL,
            rol ENUM('gerente','administrador','vendedor','bodega') DEFAULT NULL,
            activo TINYINT(1) DEFAULT 1,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB""",

        """CREATE TABLE IF NOT EXISTS categorias (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) UNIQUE NOT NULL,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB""",

        """CREATE TABLE IF NOT EXISTS proveedores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            telefono VARCHAR(30),
            correo VARCHAR(150),
            tipo_producto VARCHAR(150),
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB""",

        """CREATE TABLE IF NOT EXISTS productos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo VARCHAR(20) UNIQUE NOT NULL,
            nombre VARCHAR(200) NOT NULL,
            cantidad INT DEFAULT 0,
            precio DECIMAL(12,2) DEFAULT 0.00,
            categoria_id INT,
            proveedor_id INT,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE SET NULL,
            FOREIGN KEY (proveedor_id) REFERENCES proveedores(id) ON DELETE SET NULL
        ) ENGINE=InnoDB""",

        """CREATE TABLE IF NOT EXISTS ventas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            producto_id INT,
            nombre_producto VARCHAR(200),
            cantidad INT NOT NULL,
            precio_unitario DECIMAL(12,2) NOT NULL,
            descuento DECIMAL(5,2) DEFAULT 0,
            iva DECIMAL(5,2) DEFAULT 19,
            total DECIMAL(12,2) NOT NULL,
            usuario_id INT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE SET NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
        ) ENGINE=InnoDB""",

        """CREATE TABLE IF NOT EXISTS movimientos_stock (
            id INT AUTO_INCREMENT PRIMARY KEY,
            producto_id INT,
            nombre_producto VARCHAR(200),
            tipo ENUM('entrada','salida') NOT NULL,
            cantidad INT NOT NULL,
            motivo VARCHAR(255),
            usuario_id INT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE SET NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
        ) ENGINE=InnoDB""",

        """CREATE TABLE IF NOT EXISTS log_actividad (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT,
            usuario_nombre VARCHAR(150),
            accion VARCHAR(500) NOT NULL,
            modulo VARCHAR(100),
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
        ) ENGINE=InnoDB""",
    ]

    for sql in tablas:
        cursor.execute(sql)
    print("✅ Tablas creadas correctamente.")

    # 4. Insertar categorías iniciales
    categorias = ["Electrónica","Cables y Conectores","Herramientas","Redes","Computadores","Accesorios"]
    for cat in categorias:
        cursor.execute("INSERT IGNORE INTO categorias (nombre) VALUES (%s)", (cat,))
    conn.commit()
    print("✅ Categorías iniciales insertadas.")

    # 5. Crear gerente por defecto si no existe
    cursor.execute("SELECT id FROM usuarios WHERE rol='gerente' LIMIT 1")
    if cursor.fetchone():
        print("✅ Ya existe un gerente en el sistema.")
    else:
        print("\n── Crear cuenta de Gerente ──────────────────")
        nombre   = input("Nombre completo [Gerente General]: ").strip() or "Gerente General"
        correo   = input("Correo: ").strip()
        usuario  = input("Nombre de usuario [gerente]: ").strip() or "gerente"
        password = input("Contraseña [Admin123]: ").strip() or "Admin123"

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "INSERT INTO usuarios (nombre_completo, correo, usuario, contrasena, rol) VALUES (%s,%s,%s,%s,'gerente')",
            (nombre, correo, usuario, hashed)
        )
        conn.commit()
        print(f"\n✅ Gerente '{usuario}' creado exitosamente.")
        print(f"   Correo: {correo}")
        print(f"   Contraseña: {password}")

    cursor.close()
    conn.close()
    print("\n" + "=" * 55)
    print("  ✅ Configuración completa. Puedes ejecutar main.py")
    print("=" * 55)


if __name__ == "__main__":
    run_setup()
