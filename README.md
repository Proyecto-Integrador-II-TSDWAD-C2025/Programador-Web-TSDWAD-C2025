# NutriApp

**NutriApp** es una aplicación web diseñada para brindar planes personalizados de nutrición y entrenamiento físico, adaptados a las necesidades de cada usuario.

La plataforma tiene como objetivo principal ayudar a las personas a mejorar su salud y condición física, ya sea aumentando o disminuyendo su masa corporal, mediante recomendaciones específicas basadas en su perfil.

## 📋 Descripción

NutriApp es una solución full-stack moderna que integra **Angular** en el frontend con **Django REST Framework** en el backend, conectado a una base de datos **MySQL**.

- **Frontend**: Angular v21+ con Bootstrap (sin CDN)
- **Backend**: Django REST Framework con MySQL
- **API**: RESTful endpoints bien documentados
- **Autenticación**: Soporte para múltiples métodos
- **Escalable**: Arquitectura modular y reutilizable

## 🚀 Características

✅ Landing page responsive con Bootstrap  
✅ Planes personalizados de nutrición y entrenamiento  
✅ API RESTful completa  
✅ Base de datos MySQL  
✅ Variables de entorno (.env)  
✅ Soporte CORS  
✅ Autenticación básica  
✅ Admin Django  
✅ Documentación completa  

## 📁 Estructura del Proyecto

```
NutriApp/
├── front/                 # Frontend Angular
│   ├── src/
│   │   ├── app/          # Componente principal
│   │   └── styles.css    # Estilos globales con Bootstrap
│   ├── package.json
│   └── angular.json
├── back/                  # Backend Django
│   ├── api/              # App principal
│   ├── proyecto/         # Configuración Django
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env              # Variables de entorno (no subir a Git)
│   └── .env_modelo       # Plantilla de variables
└── README.md             # Este archivo
```

## 🛠️ Instalación

### Requisitos previos

- Python 3.x
- Node.js y npm
- Angular CLI (`npm install -g @angular/cli`)
- MySQL Server

### Frontend

```bash
cd front
npm install
ng serve
```

### Backend

```bash
cd back
python -m venv venv
source venv/Scripts/activate      # Windows (Bash)
# source venv/bin/activate         # Linux/Mac
pip install -r requirements.txt
cp .env_modelo .env               # Completar con tus datos
python manage.py migrate
python manage.py runserver
```

### Variables de entorno

Completar el archivo `.env` con los datos de tu entorno local:

```env
SECRET_KEY=tu-secret-key
DEBUG=True
DB_NAME=nutriapp
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
FRONTEND_URL=http://localhost:4200
```

> ⚠️ Nunca subir `.env` a Git.

## 🌐 Uso básico

Una vez levantados ambos servidores:

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:4200 |
| Backend | http://localhost:8000 |
| API | http://localhost:8000/api/ |
| Admin Django | http://localhost:8000/admin/ |

Para crear un superusuario y acceder al admin:

```bash
python manage.py createsuperuser
```

## 📡 API Endpoints

### Usuarios

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/usuarios/` | Listar usuarios |
| GET | `/api/usuarios/test/` | Prueba de conexión a BD |
| POST | `/api/usuarios/` | Crear usuario |
| GET | `/api/usuarios/{id}/` | Obtener usuario |
| PUT | `/api/usuarios/{id}/` | Actualizar usuario |
| DELETE | `/api/usuarios/{id}/` | Eliminar usuario |

## 📝 Requerimientos

### Requerimientos Funcionales (RF)

| N° | Descripción |
|----|-------------|
| RF1 | El sistema debe permitir el registro de nuevos usuarios. |
| RF2 | El sistema debe permitir el inicio de sesión de usuarios registrados. |
| RF3 | El sistema debe generar rutinas de ejercicio personalizadas según el perfil del usuario. |
| RF4 | El sistema debe brindar recomendaciones alimenticias basadas en los objetivos del usuario (incluyendo consumo de proteínas y calorías). |
| RF5 | El sistema debe permitir la gestión de planes de pago para acceder a funciones premium. |

### Requerimientos No Funcionales (RNF)

| N° | Descripción |
|----|-------------|
| RNF1 | El sistema debe contar con una interfaz amigable e intuitiva, accesible para usuarios sin conocimientos técnicos. |
| RNF2 | El sistema debe garantizar la seguridad y confidencialidad de los datos personales de los usuarios. |
| RNF3 | El sistema debe tener un buen rendimiento, respondiendo las solicitudes en tiempos aceptables bajo carga normal. |

## 🎯 Próximos Pasos

- [ ] Implementar autenticación JWT
- [ ] Agregar modelos de rutinas y planes alimenticios
- [ ] Crear interfaces de usuario avanzadas
- [ ] Implementar tests automatizados
- [ ] Configurar CI/CD
- [ ] Desplegar a producción

## 👥 Desarrollo

### Agregar Nuevos Endpoints

1. **Backend**: Crear modelo → Serializer → View → URL
2. **Frontend**: Crear servicio → Componente → Template

### Mejores Prácticas

- Seguir Django y Angular style guides
- Escribir tests para nuevas características
- Documentar cambios importantes
- Usar variables de entorno para configuración sensible

## 📧 Contacto

Para preguntas o sugerencias, contactar al equipo de desarrollo.

---

**Última actualización**: Abril 2026  
**Versión**: 1.0.0
