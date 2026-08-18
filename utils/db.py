"""Módulo de conexión a la base de datos MySQL."""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Retorna una conexión activa a la base de datos."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            database=os.getenv("DB_NAME", "tecnosuministros"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            charset="utf8mb4",
            autocommit=False,
        )
        return conn
    except Error as e:
        raise ConnectionError(f"Error al conectar con la base de datos: {e}")


def execute_query(query: str, params: tuple = (), fetch: bool = False):
    """Ejecuta una consulta y opcionalmente retorna resultados."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            return result
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        conn.rollback()
        raise RuntimeError(f"Error en consulta SQL: {e}\nQuery: {query}")
    finally:
        cursor.close()
        conn.close()
