# 📰 DevNews - Blog de Noticias de Programación

Bienvenido a **DevNews**, un blog moderno desarrollado en Django para compartir noticias, artículos, recursos y novedades del mundo de la programación. Proyecto final del Grupo 11 del Informatorio 2024.

## 🚀 Características principales

- Registro y autenticación de usuarios (con distintos perfiles: admin, staff, usuario registrado)
- Publicación, edición y eliminación de posts (solo para administradores y staff)
- Comentarios y sistema de "me gusta" en posts y comentarios
- Filtrado y búsqueda de publicaciones por categoría, fecha y texto
- Carrusel de imágenes destacadas en la portada
- Diseño responsive y moderno con Bootstrap 5
- Página de contacto y sección "Sobre nosotros"
- Panel de administración personalizado

## 🛠️ Instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/emyypg/blog.git
   cd blog
   ```

2. **Crea y activa un entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realiza las migraciones**
   ```bash
   python manage.py migrate
   ```

5. **Crea un superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecuta el servidor**
   ```bash
   python manage.py runserver
   ```

7. Accede a [http://localhost:8000](http://localhost:8000) en tu navegador.

## 📸 Capturas de pantalla

... ( imágenes del blog en funcionamiento para mostrar el diseño y las funcionalidades ) ...

## 📂 Estructura del proyecto

- `apps/news/` — Lógica de noticias, posts, comentarios y categorías
- `apps/usuarios/` — Gestión de usuarios y autenticación
- `core/` — Configuración principal del proyecto Django
- `media/` — Archivos subidos por los usuarios (imágenes de posts)
- `static/` — Archivos estáticos (CSS, imágenes, JS)
- `templates/` — Plantillas HTML

## 👨‍💻 Créditos

Desarrollado por el **Grupo 11** del Informatorio 2024:

- Puente Gonzalez, Emily - github: https://github.com/emyypg
- Carlos, Eduardo Gomez - github: https://github.com/gcarloseduardo
- Velazco, Carlos Ariel - github: https://github.com/carvelaz
- Cardozo, Ricardo - github: https://github.com/RickyRicardo19
- Bertran, Nelson - portfolio: https://portfolio-neelbit.netlify.app/ - github: https://github.com/NeelBit
  

## 📄 Licencia

Este proyecto es de uso educativo y sin fines de lucro.

---

¡Gracias por visitar DevNews! Si te gusta el proyecto, no dudes en dejar una estrella ⭐ en el [repositorio](https://github.com/emyypg/blog).
