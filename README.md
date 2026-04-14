# ProyectoIntegrador

Proyecto full-stack moderno que integra **Angular** en el frontend con **Django REST Framework** en el backend, conectado a una base de datos **MySQL**.

## 📋 Descripción

ProyectoIntegrador es una solución completa que demuestra una arquitectura moderna de aplicación web con:

- **Frontend**: Angular v21+ con Bootstrap (sin CDN)
- **Backend**: Django REST Framework con MySQL
- **API**: RESTful endpoints bien documentados
- **Autenticación**: Soporte para múltiples métodos
- **Escalable**: Arquitectura modular y reutilizable

## 🚀 Características

✅ Landing page responsive con Bootstrap  
✅ API RESTful completa  
✅ Base de datos MySQL  
✅ Variables de entorno (.env)  
✅ Soporte CORS  
✅ Autenticación básica  
✅ Admin Django  
✅ Documentación completa  

## 📁 Estructura del Proyecto

```
proyectoIntegrador/
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
├── INSTALL.md            # Guía de instalación
└── README.md             # Este archivo
```

## 🛠️ Instalación Rápida

### Frontend
```bash
cd front
npm install
npm start
```

### Backend
```bash
cd back
pip install -r requirements.txt
# Copiar .env_modelo a .env y configurar
python manage.py migrate
python manage.py runserver
```

**Ver [INSTALL.md](./INSTALL.md) para instalación detallada**

## 🌐 URLs

- **Frontend**: http://localhost:4200
- **Backend**: http://localhost:8000
- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/

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

## 🔑 Variables de Entorno

### Backend (.env_modelo → .env)

```env
SECRET_KEY=tu-secret-key
DEBUG=True
DB_NAME=proyectointegrador
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
FRONTEND_URL=http://localhost:4200
```

**⚠️ Importante**: Nunca subir `.env` a Git

## 🧪 Testing

### Backend
```bash
cd back
python manage.py test
```

### Frontend
```bash
cd front
npm test
```

## 📚 Documentación

- [Frontend - Angular](./front/README.md)
- [Backend - Django](./back/README.md)
- [Guía de Instalación](./INSTALL.md)

## 🎯 Próximos Pasos

- [ ] Implementar autenticación JWT
- [ ] Agregar más modelos de datos
- [ ] Crear interfaces de usuario avanzadas
- [ ] Implementar tests automatizados
- [ ] Configurar CI/CD
- [ ] Desplegar a producción

## 👥 Desarrollo

El proyecto está estructurado para ser fácil de mantener y escalar.

### Agregar Nuevos Endpoints

1. **Backend**: Crear modelo → Serializer → View → URL
2. **Frontend**: Crear servicio → Componente → Template

### Mejores Prácticas

- Seguir Django y Angular style guides
- Escribir tests para nuevas características
- Documentar cambios importantes
- Usar variables de entorno para configuración sensible

## 📝 Licencia

Este proyecto es de código abierto. 

## 📧 Contacto

Para preguntas o sugerencias, contactar al equipo de desarrollo.

---

**Última actualización**: Abril 2026  
**Versión**: 1.0.0
