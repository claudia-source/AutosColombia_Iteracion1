# Sistema de Parqueadero Autos Colombia - Iteración 1

Este repositorio contiene la implementación del prototipo backend de la **Iteración 1** para el parqueadero "Autos Colombia", enfocado en el control de entrada y salida de vehículos.

## Estructura del Proyecto
- `app.py`: Servidor API REST con desarrollo en Python Flask y SQLite.
- `requirements.txt`: Lista de dependencias del proyecto.

## Pasos para Ejecutar
1. Clonar el repositorio:
   `git clone https://github.com/claudia-source/AutosColombia_Iteracion1.git`
2. Instalar dependencias:
   `pip install -r requirements.txt`
3. Iniciar el servidor:
   `python app.py`
4. Probar endpoints en `http://localhost:5000`:
   - `POST /api/entrada` -> Registrar ingreso.
   - `POST /api/salida` -> Registrar salida.
   - `GET /api/celdas` -> Consultar disponibilidad.