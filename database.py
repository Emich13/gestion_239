import sqlite3
import json

DB_NAME = "movimientos.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        # Crear tabla usuarios
        c.execute(''' 
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        ''')
        # Crear tabla movimientos
        c.execute(''' 
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT CHECK(tipo IN ('ingreso', 'gasto')) NOT NULL,
                descripcion TEXT,
                monto REAL NOT NULL,
                fecha DATE NOT NULL,
                id_usuario INTEGER NOT NULL,
                participantes TEXT,
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
            )
        ''')
        conn.commit()

def agregar_usuario(nombre):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO usuarios (nombre) VALUES (?)', (nombre,))
        conn.commit()

def obtener_usuarios():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT id, nombre FROM usuarios')
        usuarios = c.fetchall()
    return usuarios

def editar_usuario(id_usuario, nuevo_nombre):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("UPDATE usuarios SET nombre = ? WHERE id = ?", (nuevo_nombre, id_usuario))
        conn.commit()

def eliminar_usuario(id_usuario):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
        conn.commit()

def agregar_movimiento(tipo, descripcion, monto, fecha, id_usuario, participantes):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        participantes_json = json.dumps(participantes)
        c.execute(''' 
            INSERT INTO movimientos (tipo, descripcion, monto, fecha, id_usuario, participantes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (tipo, descripcion, monto, fecha, id_usuario, participantes_json))
        conn.commit()

def obtener_movimientos():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM movimientos ORDER BY fecha DESC')
        movimientos = c.fetchall()
    return movimientos


def editar_descripcion_movimiento(id_movimiento, nueva_descripcion):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("UPDATE movimientos SET descripcion = ? WHERE id = ?", (nueva_descripcion, id_movimiento))
        conn.commit()


def eliminar_movimiento(id_movimiento):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM movimientos WHERE id = ?', (id_movimiento,))
        conn.commit()
