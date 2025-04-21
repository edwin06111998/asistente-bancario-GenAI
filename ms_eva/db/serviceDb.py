import sqlite3
import os

# Ruta al archivo de base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "ms_eva.db")

def consultar_score(cedula: str) -> int | None:
    """
    Consulta el score Equifax de una cédula.
    
    :param cedula: Número de cédula a consultar.
    :return: El score (int) si existe, o None si no se encuentra.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT scoreEquifax FROM personas WHERE cedula = ?", (cedula,))
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"[Error] consultando la cédula {cedula}: {e}")
        return None

import sqlite3

def crear_base_de_datos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personas (
        cedula TEXT PRIMARY KEY,
        scoreEquifax INTEGER
    )
    """)

    # Datos de prueba opcionales
    clientes = [
        ("0102030405", 680),
        ("1102938475", 705),
        ("1709182736", 720),
        ("0901122233", 660),
    ]

    cursor.executemany("INSERT OR REPLACE INTO personas VALUES (?, ?)", clientes)
    conn.commit()
    conn.close()
    return "Base de datos creada exitosamente"
