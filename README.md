# Proyecto IPCmarket - Arquitectura Cliente-Servidor
![mainIPC2](https://i.ibb.co/zGZX9fq/mainIPC2.png)

![admin-IPC2](https://i.ibb.co/8xp8KKs/admin-IPC2.png)

## Descripción del Proyecto

Este proyecto evoluciona la aplicación IPCmarket, originalmente desarrollada como una aplicación de escritorio, hacia un entorno web basado en una arquitectura cliente-servidor.

Frontend: Implementado con Django para proporcionar vistas dinámicas e interactividad con el usuario.Backend: Implementado con Flask para manejar la lógica de negocio, validaciones y transformación de datos.

El objetivo principal es ofrecer estadísticas visuales de productos, usuarios y compras mediante gráficos dinámicos y entendibles. Además, el sistema permite transformar archivos XML a JSON, almacenarlos y gestionarlos de manera eficiente.

## Instalación y Configuración
### Requisitos Previos
- Python 3.12 o superior
- pip (gestor de paquetes de Python)
### Instalación del Backend (Flask)
1. Navegar a la carpeta donde está el backend:
    ```bash
   cd backend
   ```
2. Instalar dependencias necesarias:
    ```bash
   pip install flask flask-cors requests
   ```
3. Ejecutar el servidor Flask:
    ```bash
   python main.py
   ```
4. El servidor estará disponible en:
    ```bash
   http://localhost:4000/
   ```
### Instalación del Frontend (Django)
1. Navegar a la carpeta donde está el frontend:
    ```bash
   cd frontend
   ```
2. Instalar dependencias necesarias:
    ```bash
   pip install django requests
   ```
3. Aplicar migraciones:
    ```bash
   python manage.py makemigrations
    python manage.py migrate
   ```
4. Levantar el servidor Django:
    ```bash
   python manage.py runserver
   ```
5. El servidor estará disponible en:
    ```bash
   http://localhost:8000/
   ```
## Funcionalidades Implementadas

### Frontend (Django)
1. El servidor estará disponible en:
    - Registro e inicio de Sesión
2. Visualización de Productos:
    - Ver catálogo, filtrar por categorías y buscar productos específicos.
3. Carrito de Compras:
    - Agregar productos al carrito y confirmar compras.
4. Estadísticas Dinámicas:
    - Gráficos para visualizar productos más vendidos y categorías con más productos.

### Backend (Flask)
1. Transformación de Datos:
    - Procesamiento de archivos XML a JSON.
2. Persistencia de Datos:
    - Almacenamiento de datos en formato XML.
3. Validaciones:
    - Integridad y formato de los datos entrantes.
4. API RESTful:
    - Endpoints para interactuar con el frontend, como carga de usuarios, productos y gestión del carrito.

## Rutas Disponibles
### Backend (Flask)
- Cargar Datos:
    - /cargausuarios - Carga datos de usuarios desde XML.
    - /cargaproductos - Carga datos de productos desde XML.
    - /cargaempleados - Carga datos de empleados desde XML.
    - /cargaactividades - Carga datos de actividades desde XML.
- Carrito de compras:
    - /añadircarrito - Añade productos al carrito.
    - /comprar - Procesa la compra del carrito.
- Consulta de datos:
    - /obtenerproductos - Devuelve lista de productos.
    - /obtenerusuarios - Devuelve lista de usuarios.
### Frontend (Django)
- Vistas del usuario:
    - Registro e inicio de sesión. 
    - Visualización y gestión del carrito.
    - Estadísticas visuales.

## Integración entre Frontend y Backend
La comunicación entre Django y Flask se realiza mediante API RESTful, donde Django consume los servicios proporcionados por Flask para mostrar la información procesada.
- Ejemplo de Petición al Backend desde el Frontend:
```bash
   import requests
    response = requests.get('http://localhost:4000/obtenerproductos')
    productos = response.json()
```


![userIPC2](https://i.ibb.co/bRWkV0x/userIPC2.png)

Admin ID: AdminIPC2
Password: IPC2VJ2024