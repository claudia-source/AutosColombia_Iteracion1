# Sistema de Información y Control Operativo — Parqueadero "Autos Colombia"

Este repositorio contiene la arquitectura, diagramas UML, modelos de datos y la API REST en Flask desarrollada para la gestión de operaciones del Parqueadero Autos Colombia.

## 🚀 Alcance por Iteraciones

### 🔹 Iteración 1 (Entregada)
- **HU-01 / RF-01, RF-02, RF-03:** Registro de Entrada de Vehículos y asignación de celdas.
- **HU-02 / RF-04:** Registro de Salida de Vehículos y liberación de espacios.
- **HU-03 / RF-05:** Tablero Visual de Disponibilidad de Celdas en Tiempo Real.

### 🔹 Iteración 2 (Entregable Actual)
- **HU-04 / RF-06:** Gestión y Administración de Usuarios (CRUD, asignación de roles Administrador/Operador).
- **HU-05 / RF-07 / RNF-04:** Autenticación de Usuarios con hashing seguro de contraseñas (`Werkzeug PBKDF2`).
- **HU-06 / RF-08:** Parametrización y Alta de Nuevas Celdas según tipo de vehículo y bloque.
- **HU-07 / RF-09:** Control del Estado Operativo de Celdas (`LIBRE`, `OCUPADA`, `MANTENIMIENTO`, `INHABILITADA`).

## 🛠️ Tecnologías e Infraestructura
- **Lenguaje / Framework:** Python 3.12 + Flask Framework
- **Seguridad:** Hashing seguro con Werkzeug Security
- **Modelado UML:** StarUML / PlantUML (Casos de Uso, Secuencia y Componentes)
- **Prototipado UI/UX:** Figma (Mockups interactivos de alta fidelidad)
- **Control de Versiones:** Git + GitHub

## 📡 Endpoints Disponibles en la API REST

| Módulo | Método | Endpoint | Descripción |
| :--- | :--- | :--- | :--- |
| **Portería** | `POST` | `/api/entrada` | Registrar entrada de vehículo y ocupar celda. |
| **Portería** | `POST` | `/api/salida` | Registrar salida de vehículo y liberar celda. |
| **Auth** | `POST` | `/api/login` | Validar credenciales de usuario e iniciar sesión. |
| **Usuarios** | `GET / POST` | `/api/usuarios` | Consultar lista o crear nuevo usuario en el sistema. |
| **Celdas** | `GET / POST` | `/api/celdas` | Listar celdas existentes o parametrizar una nueva. |
| **Celdas** | `PUT` | `/api/celdas/<codigo>/estado` | Modificar estado de celda (ej. pasar a MANTENIMIENTO). |

## 🧪 Instrucciones para Ejecución Local
```bash
# 1. Ejecutar la aplicación Flask
python app.py