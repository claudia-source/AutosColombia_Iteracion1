from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

# ==========================================
# BASE DE DATOS EN MEMORIA (ITERACIONES 1 Y 2)
# ==========================================

usuarios_db = [
    {
        "id": 1,
        "nombre": "Claudia Cabrera",
        "correo": "admin@autoscolombia.com",
        "password_hash": generate_password_hash("Admin2026*"),
        "rol": "Administrador",
        "activo": True
    }
]

celdas_db = [
    {"id": 1, "codigo": "A-01", "tipo": "Automóvil", "estado": "LIBRE"},
    {"id": 2, "codigo": "A-02", "tipo": "Automóvil", "estado": "LIBRE"},
    {"id": 3, "codigo": "A-03", "tipo": "Automóvil", "estado": "OCUPADA"},
    {"id": 4, "codigo": "M-01", "tipo": "Motocicleta", "estado": "LIBRE"}
]

movimientos_db = []

# ==========================================
# RUTA RAÍZ (RESPUESTA EN NAVEGADOR)
# ==========================================

@app.route('/', methods=['GET'])
def inicio():
    return jsonify({
        "sistema": "Parqueadero Autos Colombia",
        "estado": "Servidor Backend Operativo",
        "iteracion": "2 (Gestión de Usuarios y Celdas)",
        "endpoints_disponibles": [
            "http://127.0.0.1:5000/api/usuarios",
            "http://127.0.0.1:5000/api/celdas"
        ]
    }), 200

# ==========================================
# ENDPOINTS ITERACIÓN 1: OPERACIÓN PORTERÍA
# ==========================================

@app.route('/api/entrada', methods=['POST'])
def registrar_entrada():
    data = request.get_json()
    placa = data.get('placa')
    codigo_celda = data.get('codigo_celda')

    celda = next((c for c in celdas_db if c['codigo'] == codigo_celda and c['estado'] == 'LIBRE'), None)
    if not celda:
        return jsonify({"error": "La celda seleccionada no está disponible o no existe"}), 400

    celda['estado'] = 'OCUPADA'
    movimiento = {
        "id": len(movimientos_db) + 1,
        "placa": placa,
        "codigo_celda": codigo_celda,
        "fecha_entrada": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_salida": None,
        "estado": "ACTIVO"
    }
    movimientos_db.append(movimiento)
    return jsonify({"mensaje": "Entrada registrada exitosamente", "ticket": movimiento}), 201

@app.route('/api/salida', methods=['POST'])
def registrar_salida():
    data = request.get_json()
    placa = data.get('placa')

    movimiento = next((m for m in movimientos_db if m['placa'] == placa and m['estado'] == 'ACTIVO'), None)
    if not movimiento:
        return jsonify({"error": "No se encontró un registro de entrada activo para esta placa"}), 404

    movimiento['fecha_salida'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    movimiento['estado'] = 'FINALIZADO'

    celda = next((c for c in celdas_db if c['codigo'] == movimiento['codigo_celda']), None)
    if celda:
        celda['estado'] = 'LIBRE'

    return jsonify({"mensaje": "Salida registrada y celda liberada", "movimiento": movimiento}), 200

# ==========================================
# ENDPOINTS ITERACIÓN 2: GESTIÓN DE USUARIOS
# ==========================================

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo')
    password = data.get('password')

    usuario = next((u for u in usuarios_db if u['correo'] == correo), None)
    if usuario and check_password_hash(usuario['password_hash'], password):
        return jsonify({
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {"id": usuario['id'], "nombre": usuario['nombre'], "rol": usuario['rol']}
        }), 200
    
    return jsonify({"error": "Credenciales inválidas"}), 401

@app.route('/api/usuarios', methods=['GET', 'POST'])
def gestionar_usuarios():
    if request.method == 'POST':
        data = request.get_json()
        if any(u['correo'] == data.get('correo') for u in usuarios_db):
            return jsonify({"error": "El correo ya se encuentra registrado"}), 400
        
        nuevo_usuario = {
            "id": len(usuarios_db) + 1,
            "nombre": data.get('nombre'),
            "correo": data.get('correo'),
            "password_hash": generate_password_hash(data.get('password')),
            "rol": data.get('rol', 'Operador'),
            "activo": True
        }
        usuarios_db.append(nuevo_usuario)
        return jsonify({"mensaje": "Usuario creado exitosamente", "id": nuevo_usuario['id']}), 201

    usuarios_list = [{"id": u['id'], "nombre": u['nombre'], "correo": u['correo'], "rol": u['rol'], "activo": u['activo']} for u in usuarios_db]
    return jsonify(usuarios_list), 200

# ==========================================
# ENDPOINTS ITERACIÓN 2: GESTIÓN DE CELDAS
# ==========================================

@app.route('/api/celdas', methods=['GET', 'POST'])
def gestionar_celdas():
    if request.method == 'POST':
        data = request.get_json()
        if any(c['codigo'] == data.get('codigo') for c in celdas_db):
            return jsonify({"error": "El código de celda ya existe"}), 400
        
        nueva_celda = {
            "id": len(celdas_db) + 1,
            "codigo": data.get('codigo'),
            "tipo": data.get('tipo', 'Automóvil'),
            "estado": "LIBRE"
        }
        celdas_db.append(nueva_celda)
        return jsonify({"mensaje": "Celda creada exitosamente", "celda": nueva_celda}), 201

    return jsonify(celdas_db), 200

@app.route('/api/celdas/<codigo>/estado', methods=['PUT'])
def actualizar_estado_celda(codigo):
    data = request.get_json()
    nuevo_estado = data.get('estado')
    
    estados_validos = ['LIBRE', 'OCUPADA', 'MANTENIMIENTO', 'INHABILITADA']
    if nuevo_estado not in estados_validos:
        return jsonify({"error": "Estado no válido"}), 400
        
    celda = next((c for c in celdas_db if c['codigo'] == codigo), None)
    if not celda:
        return jsonify({"error": "Celda no encontrada"}), 404
        
    celda['estado'] = nuevo_estado
    return jsonify({"mensaje": f"Estado de la celda {codigo} actualizado a {nuevo_estado}"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)