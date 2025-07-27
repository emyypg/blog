from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Categoria, Post, Comentario # Asegúrate de importar tu modelo Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# Vista principal del sitio (usa index.html que extiende de base.html)
def index(request):
    contexto = {}
    queryset_buscar = request.GET.get("buscar")
    id_categoria = request.GET.get("id_categoria")
    fecha_parametro = request.GET.get("fecha_publicacion")
    orden_parametro = request.GET.get("orden")

    # empezamos mostrando todos los posts

    base_posts_queryset = Post.objects.all()
    # Aplicamos el filtro de búsqueda si se proporciona
    if queryset_buscar:
        base_posts_queryset = base_posts_queryset.filter(
            Q(titulo__icontains=queryset_buscar) | 
            Q(contenido__icontains=queryset_buscar)|
            Q(categorias__nombre__icontains=queryset_buscar)
        ).distinct()
    # Filtramos por categoría si se proporciona
    if id_categoria:
        base_posts_queryset = base_posts_queryset.filter(categorias__id=id_categoria)
    # Aplicamos un orden predeterminado. Esta es la alternativa si no proporcionamos los parámetros de "fecha_publicacion" u "orden" 
    # en la URL, o si "filtrar_posts" no aplica un nuevo orden.
    base_posts_queryset = base_posts_queryset.order_by('-fecha_publicacion')
    # Pasamos el conjunto de consultas ya filtrado (por búsqueda/categoría) a 'filtrar_posts'
    # para ordenarlo según 'fecha_parametro' u 'orden_parametro'.
    final_posts_queryset = filtrar_posts(base_posts_queryset, fecha_parametro, orden_parametro)

    # Ahora pasamos el queryset filtrado y ordenado al contexto
    contexto['posts'] = final_posts_queryset
    contexto['categorias'] = Categoria.objects.all()  # Obtenemos todas las categorías

    return render(request, 'news/index.html', contexto)  # Pasamos los posts al contexto de la plantilla

def filtrar_posts(posts_queryset, fecha_parametro, orden_parametro):
    # Esta función SOLO debe modificar el 'posts_queryset' que se le pasa.
    # NO debe iniciar una nueva consulta con Posts.objects.all().

    # Prioriza el orden por título si se proporciona 'orden_param'.
    # Si tanto 'fecha_parametro' como 'orden_parametro' están presentes, 'orden_parametro' tendrá prioridad.
    if orden_parametro == 'asc':
        posts_queryset = posts_queryset.order_by('titulo')
    elif orden_parametro == 'des':
        posts_queryset = posts_queryset.order_by('-titulo')
    # If 'orden_param' was NOT provided, then check for 'fecha_param'.
    elif fecha_parametro == 'asc':
        posts_queryset = posts_queryset.order_by('fecha_publicacion')
    elif fecha_parametro == 'des':
        posts_queryset = posts_queryset.order_by('-fecha_publicacion')

    return posts_queryset # Return the modified (ordered) queryset

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

def agregar_post(request):
    if request.method == 'POST':
        form =PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news:home')
    else:
        form = PostForm()

    return render(request, 'news/agregar_post.html', {'form': form})

