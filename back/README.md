# ProyectoIntegrador - Backend (Django REST Framework)

Backend API construido con Django REST Framework y MySQL.

## Prerequisites

- Python 3.10+
- MySQL 5.7+
- pip

## Setup

Desde `back/`, en PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env_modelo .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Guardar la clave generada en `SECRET_KEY` de `.env` y completar `DB_USER` y
`DB_PASSWORD` con las credenciales propias. No subir ni compartir este archivo.
En desarrollo, `DEBUG=True` permite HTTP local; el código usa `DEBUG=False` si
la variable no está definida. `DB_USER` no tiene fallback a `root`.
Las variables del sistema tienen prioridad sobre el archivo `back/.env`.

Usar un usuario MySQL dedicado con permisos sobre la base de NutriApp. No crear
migraciones para instalar el proyecto: aplicar las que ya están versionadas.

```powershell
python manage.py migrate --plan
python manage.py migrate
python manage.py runserver
```

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

## Tokens de API: vencimiento de 25 minutos

`AUTH_TOKEN_TTL_MINUTES=25` define el plazo absoluto desde la emision del token.
La actividad y un nuevo login mientras el token sigue vigente no extienden ese plazo.
Al vencer, los recursos protegidos responden `401` y el usuario debe iniciar sesion otra vez.
El login reemplaza un token vencido; no necesita migraciones nuevas ni cambios en el
header Android `Authorization: Token <token>`. Login y registro devuelven ademas
`expires_at` en formato ISO 8601. La aplicacion detecta el vencimiento en su siguiente
peticion protegida; este cambio no agrega un temporizador de cierre visual al cliente.

Los tokens emitidos hace mas de 25 minutos tambien seran rechazados al desplegar este
cambio. No renovar su fecha ni desactivar la expiracion para conservar esas sesiones.
Los endpoints publicos de login y registro no autentican el token viejo que pudiera
enviar el cliente: validan las credenciales o datos de registro correspondientes.

DRF mantiene un token por cuenta. Una cuenta compartida comparte el vencimiento y un
logout revoca la sesion de todos los dispositivos. Para sesiones independientes se
necesitan cuentas distintas o un esquema de multiples tokens, no cambios de password
o rotacion del token en cada login. El plazo aplica a tokens de la API, no a cookies
del panel de administracion Django.

## Cuenta administradora de pruebas

Desde `back/`, en una terminal interactiva del entorno aprobado y con este codigo
desplegado:

```text
python manage.py crear_admin_pruebas --email CORREO_DEL_EQUIPO --nombre Equipo --apellido Pruebas
```

El responsable ingresa y confirma la contrasena de forma privada, sin eco. Debe tener
al menos 12 caracteres, mayuscula, minuscula, numero y simbolo, y superar los validadores
de Django. No pasar contrasenas como argumentos, variables publicas o texto del chat.

El comando crea solo una cuenta nueva con rol `administrador` de la aplicacion,
`is_staff=False` e `is_superuser=False`: no habilita el panel Django. No crea un token,
no cambia cuentas existentes y no instala administradores mediante migraciones.
Ejecutar el comando contra el entorno correcto; no crear esta cuenta como parte de las
pruebas automaticas ni ejecutar migraciones productivas para esta tarea.

La contrasena compartida debe distribuirse por un canal privado acordado por el equipo
y la cuenta debe deshabilitarse cuando termine su uso de pruebas. El administrador
de aplicacion tiene acceso amplio a la API: no utilizar datos personales reales.

## CORS Configuration

Configurar `CORS_ALLOWED_ORIGINS` con una lista separada por comas, por ejemplo
`https://frontend.example.com`. Incluir esquema y puerto cuando corresponda,
sin slash final. En desarrollo se admiten por defecto localhost:4200,
127.0.0.1:4200 y localhost:3000; en producción la lista por defecto está vacía.
`FRONTEND_URL` ya no se usa. Android no necesita CORS y CORS no sustituye la
autenticación ni los permisos.

Para peticiones con cookies de sesión desde otro origen confiable, configurar
también `CSRF_TRUSTED_ORIGINS`. No desactivar CSRF para habilitar el frontend.

## Perfil: persistencia y errores

`GET /api/perfil/` devuelve solo el perfil de la cuenta autenticada; si aún no
existe, responde 404. `PUT /api/perfil/` crea o actualiza ese perfil y su peso del
día, junto con las asignaciones recomendadas, dentro de una transacción.
Un fallo inesperado revierte los cambios de esa operación y responde 500 con
`{"detail": "No se pudo guardar el perfil. Intenta nuevamente."}`.
Los errores por campo conservan 400 y una petición sin token recibe 401.
El cuerpo no permite elegir otro usuario.

Los errores internos de guardado se registran con `logging` en stderr para que
Railway los recoja. No se escriben archivos en rutas Windows ni se registra el
payload de Perfil. El cliente no recibe trazas ni mensajes internos de excepción.

## Pruebas locales sin Railway

```powershell
python manage.py test api proyecto.test_settings --settings=proyecto.settings_test
python manage.py check --settings=proyecto.settings_test
```

Esta configuración usa SQLite en memoria y valores exclusivos de pruebas; no
conecta con MySQL. Ejecuta migraciones y los tests existentes, además de pruebas
de validación, aislamiento entre cuentas, persistencia, rollback y configuración
HTTPS. No usar `proyecto.settings_test` en un servidor. Estas pruebas no reemplazan
la regresión con MySQL en un entorno de pruebas antes de publicar.

## Producción y Railway

Antes de publicar, configurar en las variables del servicio (no en Git):

| Variable | Valor o criterio |
| --- | --- |
| `SECRET_KEY` | Clave aleatoria privada, estable entre despliegues |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `nutriapp-appmovil.up.railway.app`, sin esquema ni `*` |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Valores reales del servicio MySQL; no usar las credenciales de la plantilla |
| `CORS_ALLOWED_ORIGINS` | Orígenes HTTPS del frontend desplegado; vacío si solo se usa Android |
| `CSRF_TRUSTED_ORIGINS` | Orígenes confiables que envían peticiones con sesión/cookies |
| `TRUST_X_FORWARDED_PROTO` | `True` en Railway, donde el proxy controla `X-Forwarded-Proto` |

Con `DEBUG=False`, se activan redirección HTTPS, cookies seguras y HSTS durante
una hora. En Railway debe configurarse `TRUST_X_FORWARDED_PROTO=True` antes del
despliegue para evitar redirecciones en bucle. Fuera de un proxy confiable,
mantenerlo en `False`; no confiar en un header enviado libremente por el cliente.
HSTS no incluye subdominios ni preload: habilitarlos requiere revisar todos los
dominios afectados.

Con las variables de producción, ejecutar:

```powershell
python manage.py check --deploy
python manage.py migrate --plan
```

Revisar cada advertencia de `check --deploy`; W005 (HSTS en subdominios) y W021
(preload) se mantienen deliberadamente desactivados en esta primera etapa.
En particular, `develop` ya incluye la migración
`0007_remove_legacy_seed_admin`, que elimina `admin@nutriapp.com`: revisar su
impacto y contar con otra cuenta administrativa antes de ejecutar `migrate`.

Tras aprobar el plan de migraciones y desplegar, comprobar que HTTPS responde
sin bucles, que `/api/perfil/` sin token devuelve 401 y que un usuario de pruebas
puede guardar y recuperar su perfil. No ejecutar la suite contra la base productiva.
La integración de `develop` a `main` y el despliegue se realizan como paso separado.

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

Para producción, seguir la sección anterior. El servidor falla al iniciar si
faltan `SECRET_KEY`, `DB_USER` o `DB_PASSWORD`; con `DEBUG=False` exige también
`DB_NAME`, `DB_HOST` y hosts explícitos.
