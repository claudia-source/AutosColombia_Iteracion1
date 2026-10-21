import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_NAME = 'parqueadero.db'

def init_db():
    """Inicializa la base de datos con tablas de prueba."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS celdas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            estado TEXT NOT NULL DEFAULT 'LIBRE'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            celda_codigo TEXT NOT NULL,
            fecha_entrada TEXT NOT NULL,
            fecha_salida TEXT,
            novedades TEXT
        )
    ''')
    
    # Celdas sembradas por defecto si la BD está vacía
    cursor.execute("SELECT COUNT(*) FROM celdas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO celdas (codigo, estado) VALUES (?, 'LIBRE')", 
                         [('A-01',), ('A-02',), ('A-03',), ('M-01',)])
    
    conn.commit()
    conn.close()

@app.route('/api/entrada', methods=['POST'])
def registrar_entrada():
    """Registra el ingreso de un vehículo y ocupa la celda asignada."""
    data = request.json
    placa = data.get('placa')
    celda_codigo = data.get('celda_codigo')
    novedades = data.get('novedades', '')

    if not placa or not celda_codigo:
        return jsonify({'error': 'Placa y celda son obligatorios'}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Verificar disponibilidad de la celda
    cursor.execute("SELECT estado FROM celdas WHERE codigo = ?", (celda_codigo,))
    celda = cursor.fetchone()

    if not celda:
        conn.close()
        return jsonify({'error': 'La celda especificada no existe'}), 404
    if celda[0] != 'LIBRE':
        conn.close()
        return jsonify({'error': f'La celda {celda_codigo} ya está ocupada'}), 400

    # Registrar movimiento y actualizar estado de la celda
    hora_entrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO movimientos (placa, celda_codigo, fecha_entrada, novedades) VALUES (?, ?, ?, ?)",
                   (placa.upper(), celda_codigo, hora_entrada, novedades))
    cursor.execute("UPDATE celdas SET estado = 'OCUPADA' WHERE codigo = ?", (celda_codigo,))

    conn.commit()
    conn.close()

    return jsonify({
        'mensaje': 'Ingreso registrado con éxito',
        'placa': placa.upper(),
        'celda': celda_codigo,
        'fecha_entrada': hora_entrada
    }), 201

@app.route('/api/salida', methods=['POST'])
def registrar_salida():
    """Registra la salida de un vehículo y libera la celda."""
    data = request.json
    placa = data.get('placa')

    if not placa:
        return jsonify({'error': 'La placa es obligatoria'}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, celda_codigo, fecha_entrada FROM movimientos WHERE placa = ? AND fecha_salida IS NULL", (placa.upper(),))
    movimiento = cursor.fetchone()

    if not movimiento:
        conn.close()
        return jsonify({'error': 'No se encontró un ingreso activo para esta placa'}), 404

    mov_id, celda_codigo, fecha_entrada = movimiento
    hora_salida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Actualizar movimiento y liberar celda
    cursor.execute("UPDATE movimientos SET fecha_salida = ? WHERE id = ?", (hora_salida, mov_id))
    cursor.execute("UPDATE celdas SET estado = 'LIBRE' WHERE codigo = ?", (celda_codigo,))

    conn.commit()
    conn.close()

    return jsonify({
        'mensaje': 'Salida registrada correctamente',
        'placa': placa.upper(),
        'celda_liberada': celda_codigo,
        'fecha_salida': hora_salida
    }), 200

@app.route('/api/celdas', methods=['GET'])
def consultar_celdas():
    """Devuelve el estado de todas las celdas en tiempo real."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, estado FROM celdas")
    celdas = [{'codigo': row[0], 'estado': row[1]} for row in cursor.fetchall()]
    conn.close()
    return jsonify(celdas), 200

if __name__ == '__main__':
    init_db()
    print("Servidor de Parqueadero Autos Colombia ejecutándose en puerto 5000...")
    app.run(debug=True, port=5000)