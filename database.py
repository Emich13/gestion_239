import sqlite3
import json

DB_NAME = "movimientos.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
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
    conn.close()

def agregar_usuario(nombre):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO usuarios (nombre) VALUES (?)', (nombre,))
    conn.commit()
    conn.close()

def obtener_usuarios():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, nombre FROM usuarios')
    usuarios = c.fetchall()
    conn.close()
    return usuarios

def agregar_movimiento(tipo, descripcion, monto, fecha, id_usuario, participantes):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    participantes_json = json.dumps(participantes)
    c.execute('''
        INSERT INTO movimientos (tipo, descripcion, monto, fecha, id_usuario, participantes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (tipo, descripcion, monto, fecha, id_usuario, participantes_json))
    conn.commit()
    conn.close()

def obtener_movimientos():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM movimientos ORDER BY fecha DESC')
    movimientos = c.fetchall()
    conn.close()
    return movimientos

def eliminar_movimiento(id_movimiento):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM movimientos WHERE id = ?', (id_movimiento,))
    conn.commit()
    conn.close()
