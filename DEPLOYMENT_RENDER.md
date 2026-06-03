# 🚀 Deployment a Render - Guía Completa

## Paso 1: Preparar el repositorio

### 1.1 Inicializar Git (si no lo has hecho)
```bash
git init
git add .
git commit -m "Initial commit - Ready for Render deployment"
```

### 1.2 Crear `.env` basado en `.env.example`
```bash
cp .env.example .env
```

Edita `.env` con tus valores reales:
```env
GEMINI_API_KEY=tu_clave_aqui
SECRET_KEY=tu_secret_key_segura_aqui
ALLOWED_HOSTS=localhost,127.0.0.1,tu-app.onrender.com
DEBUG=False
```

## Paso 2: Subir a GitHub

```bash
git remote add origin https://github.com/tu-usuario/DuolingoChat.git
git branch -M main
git push -u origin main
```

## Paso 3: Crear la app en Render

1. Ve a https://dashboard.render.com
2. Haz clic en **"New +"** → **"Web Service"**
3. Conecta tu repositorio de GitHub
4. Configura los siguientes valores:
   - **Name:** duolingo-chat (o tu nombre preferido)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
   - **Start Command:** `gunicorn DuolingoChat.wsgi:application`

## Paso 4: Variables de Entorno en Render

En el dashboard de Render, ve a **Environment** y agrega:

```
GEMINI_API_KEY=tu_clave_api_gemini
SECRET_KEY=tu_secret_key_segura
ALLOWED_HOSTS=localhost,127.0.0.1,tu-app.onrender.com
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
```

## Paso 5: Deploy

Haz clic en **"Create Web Service"** y Render comenzará el deployment automáticamente.

---

## Archivos de Configuración Incluidos

| Archivo | Propósito |
|---------|-----------|
| `Procfile` | Especifica cómo ejecutar la app |
| `runtime.txt` | Define versión de Python |
| `requirements.txt` | Todas las dependencias de pip |
| `build.sh` | Script para build (migraciones, statics) |
| `.env.example` | Template de variables de entorno |

## Troubleshooting

### Error: "ModuleNotFoundError"
→ Verifica que `requirements.txt` está actualizado: `pip freeze > requirements.txt`

### Error: "Static files not found"
→ Render ejecuta `collectstatic` automáticamente. Si falla, agrega:
```
STATIC_ROOT=staticfiles
STATICFILES_STORAGE=whitenoise.storage.CompressedManifestStaticFilesStorage
```

### Error: "Database locked"
→ Usa SQLite solo para desarrollo. Para producción, considera PostgreSQL (disponible en Render).

---

## ✅ Checklist Final

- [ ] Todos los cambios en Git
- [ ] `.env` no está en Git (debe estar en `.gitignore`)
- [ ] `requirements.txt` está actualizado
- [ ] `SECRET_KEY` es diferente en Render y desarrollo
- [ ] `DEBUG=False` en producción
- [ ] `ALLOWED_HOSTS` incluye tu dominio de Render
- [ ] Variables de entorno configuradas en Render dashboard

¡Listo! Render desplegará tu app automáticamente. 🎉
