from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Categoria, Post, Comentario # Asegúrate de importar tu modelo Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
from django.urls import reverse_lazy

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


@login_required
def agregar_post(request):
    """
    Vista para agregar un nuevo post.
    Maneja la lógica de validación del formulario y guarda el post.
    """
    if request.method == 'POST':
        # Instancia el formulario con los datos POST y los archivos (para la imagen)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # No guardes el formulario directamente si necesitas asignar el autor
            post = form.save(commit=False)
            # Asigna el autor del post al usuario actualmente logueado
            # El decorador @login_required garantiza que request.user es un usuario autenticado.
            post.autor = request.user

            try:
                post.save() # Guarda el objeto Post en la base de datos
                # Guarda los datos Many-to-Many (como categorías)
                # Esto es necesario después de que el objeto principal (post) ha sido guardado.
                form.save_m2m()

                # Redirige a la página 'home' de la aplicación 'news'
                return redirect('news:home')
            except Exception as e:
                # Captura cualquier error durante el guardado y lo imprime para depuración
                print(f"Error al guardar el post: {e}")
                # Puedes añadir un mensaje de error al formulario o al contexto aquí
                # form.add_error(None, "Hubo un error al guardar el post. Inténtalo de nuevo.")
        else:
            # Si el formulario no es válido, imprime los errores en la consola para depuración
            print("Errores del formulario:")
            print(form.errors)
            # La plantilla se renderizará con los errores automáticamente si los manejas.

    else:
        # Si la solicitud es GET, crea un formulario vacío
        form = PostForm()

    # Renderiza la plantilla con el formulario (vacío o con errores)
    return render(request, 'news/agregar_post.html', {'form': form})

@login_required
def eliminar_post(request, pk):
    post = Post.objects.get(pk =pk)
    post = get_object_or_404(Post, pk=pk)
    contexto = {'posts': post}
    if request.method == 'POST':
        post.delete()
        return redirect('news:home')
    return render(request, 'news/detalle_post.html', contexto)

 

@login_required
def editar_post(request, pk):
    # obtengo la noticia y si no existe tira error
    post = get_object_or_404(Post, pk=pk)
    # si se aprieta el boton de guardar cambios manda la info a travez de POST 
    if request.method == 'POST':
        # inicializamos el formulario con el parametro instance, que es un parametro que se necesita para actualizar una instancia de la BD
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('news:post_detail', pk=post.pk) 

    else:
        form = PostForm(instance=post)
   
    return render(request, 'news/editar_post.html',{'form': form, 'post': post})

@login_required
def Comentar_Post(request):
    comentario = request.POST.get('comentario', None)
    user = request.user
    post_a_comentar = request.POST.get('id_post', None)
    post = Post.objects.get(pk=post_a_comentar)
    coment = Comentario.objects.create(
    usuario=user, post=post, texto=comentario)
    return redirect(reverse_lazy('news:post_detail', kwargs={"pk": noti}))

class EditarComentario(View):
    def get(self, request, pk):
        comment = Comentario.objects.get(pk=pk) # extraemos el objeto de comentarios con igual pk
        post = comment.post 
        return render(request, 'news/editar_comentario.html', {'comment': comment, 'post': post})

    def post(self, request, pk):
        comment = Comentario.objects.get(pk=pk)
        nuevo_contenido = request.POST.get('texto')
        comment.texto = nuevo_contenido
        comment.save()
        post = comment.post      # buscamos de que noticia es el comentario para sarlo para redireccionarme a la misma despues de editarla
        return redirect('news:post_detail', pk=post.pk)
