from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Post, Comentario, Categoria # Asegúrate de importar tu modelo Post

# Vista principal del sitio (usa index.html que extiende de base.html)
def index(request):
    posts=Post.objects.all().order_by('fecha_publicacion') # Aquí podrías obtener los posts desde la base de datos
    return render(request, 'news/index.html', {'posts': posts})  # Pasamos los posts al contexto de la plantilla

def post_detail(request, pk):
    contexto = {}
    try:
      # Obtenemos el id del post desde la URL    data = Post.objects.Get.get(pk=pk)
      data = Post.objects.get(pk=pk)  # Obtenemos el post por su id
      contexto['post'] = data
      comentarios = Comentario.objects.filter(post=data)# Obtenemos los comentarios del post
      contexto['comentarios'] = comentarios
    except Post.DoesNotExist:
      raise Http404('El Post seleccionado no existe')

    return render(request, 'news/detalle_post.html',contexto)