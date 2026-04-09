# Prode - API Backend - Desarrollo de Software - TP2

API para gestionar el fixture del Mundial de Fútbol 2026 y un sistema de pronósticos deportivos (ProDe).

Desarrollado con Flask y MySQL para la materia Introducción al Desarrollo de Software (TB022).

## Requisitos

- Python 3
- MySQL Server
- pip

## Instalación

1. Clonar el repositorio
2. Crear y activar el entorno virtual:
   python3 -m venv venv
   source venv/bin/activate
3. Instalar dependencias:
   pip install -r requirements.txt
4. Crear usuario con pass: alumno123 y user: alumno:
   sql
   CREATE USER 'alumno'@'localhost' IDENTIFIED BY 'alumno123';
   GRANT ALL PRIVILEGES ON *.* TO 'alumno'@'localhost';
   FLUSH PRIVILEGES;
   EXIT; 
  
  o cambiar las credenciales de los archivos (en init_db.py y db.py)

5. Crear la base de datos y cargar datos iniciales:
   cd app_backend
   python3 init_db.py
   cd ..
   Ejecutar:
     python3 -m app_backend.app

Y queda la API ejecutando en el puerto 5000
