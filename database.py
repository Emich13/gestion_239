from dotenv import load_dotenv
load_dotenv()
import psycopg2
import os
import json

# Variables de entorno
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)  # Default a 5432 si no se proporciona

def conectar():
    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            sslmode="require"
        )
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise

def obtener_usuarios():
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nombre FROM usuarios ORDER BY id")
                return cur.fetchall()
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []

def agregar_usuario(nombre):
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
                conn.commit()
    except Exception as e:
        print(f"Error al agregar usuario: {e}")

def eliminar_usuario(id_usuario):
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
                conn.commit()
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")

def editar_usuario(id_usuario, nuevo_nombre):
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE usuarios SET nombre = %s WHERE id = %s", (nuevo_nombre, id_usuario))
                conn.commit()
    except Exception as e:
        print(f"Error al editar usuario: {e}")

def agregar_movimiento(tipo, descripcion, monto, fecha, id_usuario, participantes):
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO movimientos (tipo, descripcion, monto, fecha, id_usuario, participantes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (tipo, descripcion, monto, fecha, id_usuario, participantes))
                conn.commit()
    except Exception as e:
        print(f"Error al agregar movimiento: {e}")

def obtener_movimientos():
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, tipo, descripcion, monto, fecha, id_usuario, participantes
                    FROM movimientos
                    ORDER BY fecha
                """)
                movimientos = cur.fetchall()
                return [(id, tipo, descripcion, monto, fecha, id_usuario, json.dumps(participantes)) 
                        for id, tipo, descripcion, monto, fecha, id_usuario, participantes in movimientos]
    except Exception as e:
        print(f"Error al obtener movimientos: {e}")
        return []

def eliminar_movimiento(id_movimiento):
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM movimientos WHERE id = %s", (id_movimiento,))
                conn.commit()
    except Exception as e:
        print(f"Error al eliminar movimiento: {e}")

def editar_descripcion_movimiento(id_movimiento, nueva_descripcion):
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE movimientos SET descripcion = %s WHERE id = %s", (nueva_descripcion, id_movimiento))
                conn.commit()
    except Exception as e:
        print(f"Error al editar descripción del movimiento: {e}")
