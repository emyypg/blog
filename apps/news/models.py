from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Post(models.Model):
    ESTADO_CHOICES = (
        ('borrador', 'Borrador'),
        ('publicado', 'Publicado'),
    )

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts_autor'
    )
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    contenido = models.TextField()
    categorias = models.ManyToManyField(Categoria, blank=True, related_name='posts')
    imagen_destacada = models.ImageField(upload_to='posts/', blank=True, null=True)

    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes', blank=True)  # <--- CORREGIDO

    class Meta:
        ordering = ['-fecha_publicacion', '-fecha_creacion']

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def publicar(self):
        self.estado = 'publicado'
        self.fecha_publicacion = timezone.now()
        self.save()


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios_usuario')
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    comentario_padre = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='respuestas'
    )

    # ✅ Campo agregado para me gusta en comentarios
    me_gusta = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='comentarios_me_gusta',
        blank=True
    )

    class Meta:
        ordering = ['fecha_creacion']

    def __str__(self):
        return f'Comentario de {self.autor} en "{self.post.titulo}"'

    def es_respuesta(self):
        return self.comentario_padre is not None

    # ✅ Método útil para contar me gusta
    def cantidad_likes(self):
        return self.me_gusta.count()
    
class Contacto(models.Model):
    nombre = models.CharField(max_length=60)
    correo = models.EmailField()
    asunto = models.CharField(max_length=40)
    texto = models.TextField()
    fecha_recepcion = models.DateTimeField(auto_now_add=True) # <-- Añade esta línea

    def __str__(self) -> str:
        return self.nombre