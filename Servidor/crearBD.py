import sqlite3

# Establecer conexión con la base de datos
conn = sqlite3.connect('registros.db')

# Crear un objeto cursor
cursor = conn.cursor()

# Ejecutar comandos SQL para crear tablas
cursor.execute('CREATE TABLE IF NOT EXISTS entrenador (id INTEGER PRIMARY KEY, nombre TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS capturas_pokemon (id INTEGER PRIMARY KEY, nombre TEXT, imagen TEXT)')

# Guardar los cambios en la base de datos
conn.commit()

# Cerrar la conexión
conn.close()
