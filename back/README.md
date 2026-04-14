# ProyectoIntegrador - Backend (Django REST Framework)

Backend API construido con Django REST Framework y MySQL.

## Prerequisites

- Python 3.10+
- MySQL 5.7+
- pip

## Setup

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copiar `.env_modelo` a `.env` y actualizar los valores:

```bash
cp .env_modelo .env
```

Editar `.env` con tus credenciales de MySQL:

```
DB_NAME=proyectointegrador
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
```

# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
source venv/Scripts/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar migraciones

    # ----1. Genera los archivos de migración desde los modelos:
    python manage.py makemigrations

    # ---- 2. Aplica esas migraciones a la base de datos:
    python manage.py migrate


# 5. Levantar el servidor
python manage.py runserver

El servidor estará disponible en `http://localhost:8000`

## API Endpoints

### Usuarios

- **GET** `/api/usuarios/` - Listar todos los usuarios
- **GET** `/api/usuarios/test/` - Endpoint de prueba para verificar conexión con la BD
- **POST** `/api/usuarios/` - Crear un nuevo usuario
- **GET** `/api/usuarios/{id}/` - Obtener un usuario específico
- **PUT** `/api/usuarios/{id}/` - Actualizar un usuario
- **DELETE** `/api/usuarios/{id}/` - Eliminar un usuario

## Admin Panel

Acceder a `http://localhost:8000/admin/` para gestionar datos (requiere antes crear un superusuario)

## CORS Configuration

El backend está configurado para aceptar requests desde:
- `http://localhost:4200` (Angular Dev Server)
- `http://127.0.0.1:4200`

Para agregar más origenes, editar `CORS_ALLOWED_ORIGINS` en `proyecto/settings.py`.

## Estructura del Proyecto

```
back/
├── api/                 # App principal de la API
│   ├── admin.py        # Configuración del admin
│   ├── apps.py         # Configuración de la app
│   ├── models.py       # Modelos de BD
│   ├── serializers.py  # Serializers DRF
│   ├── views.py        # Vistas de la API
│   └── urls.py         # URLs de la app
├── proyecto/           # Configuración del proyecto
│   ├── settings.py     # Configuración de Django
│   ├── urls.py         # URLs principales
│   ├── wsgi.py         # WSGI para producción
│   └── asgi.py         # ASGI para async
├── manage.py           # Comando CLI de Django
├── requirements.txt    # Dependencias
├── .env               # Variables de entorno (no subir a Git)
└── .env_modelo        # Plantilla de variables de entorno
```

## Notas Importantes

⚠️ **NUNCA** subir `.env` al repositorio. Usar `.env_modelo` como referencia.

Para producción:
- Cambiar `SECRET_KEY` a un valor seguro
- Establecer `DEBUG=False`
- Configurar `ALLOWED_HOSTS` con los dominios correctos
- Usar HTTPS
- Configurar credenciales de BD de forma segura
