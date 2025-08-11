from django.contrib import admin
from .models import Categoria, Post, Comentario, Contacto
from apps.usuarios.models import Usuario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    fields = ('autor', 'contenido', 'fecha_creacion', 'comentario_padre')
    readonly_fields = ('fecha_creacion',)
    show_change_link = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'estado', 'fecha_publicacion', 'fecha_creacion')
    list_filter = ('estado', 'fecha_publicacion', 'categorias')
    search_fields = ('titulo', 'contenido', 'autor__username')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'
    ordering = ('-fecha_publicacion',)
    readonly_fields = ('fecha_creacion',)
    filter_horizontal = ('categorias',)

    inlines = [ComentarioInline]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('post', 'autor', 'contenido_corto', 'fecha_creacion', 'comentario_padre')
    list_filter = ('fecha_creacion',)
    search_fields = ('contenido', 'autor__username', 'post__titulo')
    readonly_fields = ('fecha_creacion',)

    def contenido_corto(self, obj):
        return obj.contenido[:40] + ('...' if len(obj.contenido) > 40 else '')
    contenido_corto.short_description = 'Contenido'

class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'asunto', 'fecha_recepcion') # Muestra estas columnas
    list_filter = ('fecha_recepcion',) # Permite filtrar por fecha
    search_fields = ('nombre', 'correo', 'asunto') # Permite buscar por estos campos
    readonly_fields = ('fecha_recepcion',) # Hace que el campo sea solo de lectura

# Asumiendo que has añadido un campo 'fecha_recepcion' en tu modelo Contacto:
# class Contacto(models.Model):
#     ...
#     fecha_recepcion = models.DateTimeField(auto_now_add=True)
#     ...

# Y registra el modelo con la clase de personalización
admin.site.register(Contacto, ContactoAdmin)
admin.site.register(Usuario)
