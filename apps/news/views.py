from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Categoria, Post, Comentario # Asegúrate de importar tu modelo Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm, CommentForm, ContactoForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages

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
    categorias = Categoria.objects.all()
    destacadas = Post.objects.all().order_by('-fecha_publicacion')[:3]
    return render(request, 'news/index.html', {
        'posts': final_posts_queryset,
        'categorias': categorias,
        'destacadas': destacadas,
    })

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
    post = get_object_or_404(Post, pk=pk)
    # Verifica si el usuario tiene permiso para eliminar el post
    if not (request.user.is_superuser or request.user.is_staff or request.user == post.autor):
        # Si el usuario no tiene permiso, redirige a la página de inicio o a una página de acceso denegado
        return redirect(reverse_lazy('news:home')) 
    # Si el usuario tiene permiso, procede con la eliminación
    # Si la solicitud es POST, significa que el usuario ha confirmado la eliminación
    if request.method == 'POST':
        # Elimina el post de la base de datos
        post.delete()
        # Redirige a la página de inicio después de eliminar el post
        return redirect(reverse_lazy('news:home'))
    else:
        # Si la solicitud es GET, muestra una página de confirmación de eliminación
    # Renderiza una plantilla de confirmación de eliminación
        return render(request, 'news/confirmar_eliminar_post.html', {'post': post})

@login_required
def editar_post(request, pk):
    # obtengo la noticia y si no existe tira error
    post = get_object_or_404(Post, pk=pk)
    # si se aprieta el boton de guardar cambios manda la info a travez de POST 
    if request.method == 'POST':
        # inicializamos el formulario con el parametro instance, que es un parametro que se necesita para actualizar una instancia de la BD
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('news:post_detail', pk=post.pk) 

    else:
        form = PostForm(instance=post)
   
    return render(request, 'news/editar_post.html',{'form': form, 'post': post})

@login_required
@require_POST  # Asegura que esta vista solo maneje solicitudes POST
def Comentar_Post(request):
    comment_text = request.POST.get('comentario', None)
    post_id = request.POST.get('id_post', None)

    if not post_id or not comment_text:
        # Handle missing data more gracefully, redirecting to the post if ID exists
        if post_id:
            post = get_object_or_404(Post, pk=post_id)
            # Redirect using pk because your URL expects pk
            return redirect(reverse_lazy('news:post_detail', kwargs={"pk": post.pk}))
        else:
            return redirect(reverse_lazy('news:home'))

    post = get_object_or_404(Post, pk=post_id)

    coment = Comentario.objects.create(
        autor=request.user,
        post=post,
        contenido=comment_text
    )

    comentario_padre_id = request.POST.get('comentario_padre_id')
    if comentario_padre_id:
        try:
            parent_comment = Comentario.objects.get(pk=comentario_padre_id)
            coment.comentario_padre = parent_comment
            coment.save()
        except Comentario.DoesNotExist:
            pass
    # Redirige al detalle del post después de comentar
    return redirect(reverse_lazy('news:post_detail', kwargs={"pk": post.pk}))


class EditarComentario(LoginRequiredMixin, View):
    # LoginRequiredMixin se asegura que el usuario esté autenticado antes de acceder a esta vista
    # si no está autenticado, lo redirige a la página de inicio de sesión
    def get(self, request, pk):
        comment = get_object_or_404(Comentario, pk=pk)
        # Verifica si el usuario es el autor del comentario o un superusuario
        # Si no es el autor, redirige a la página de detalle del post        
        if not (comment.autor == request.user or request.user.is_staff or request.user.is_superuser):
            return redirect(reverse_lazy('news:post_detail', kwargs={"pk": comment.post.pk}))
        # Si el usuario es el autor, muestra el formulario para editar el comentario
        # Crea un formulario con los datos del comentario existente
        form = CommentForm(instance=comment) 
        post = comment.post 
        return render(request, 'news/editar_comentario.html', {'form': form, 'comment': comment, 'post': post})
    # Maneja la solicitud POST para actualizar el comentario
    # Verifica si el usuario es el autor del comentario o un superusuario
    def post(self, request, pk):
        comment = get_object_or_404(Comentario, pk=pk) 
        if not (comment.autor == request.user or request.user.is_staff or request.user.is_superuser):
            # Si el usuario no es el autor del comentario, redirige a la página de detalle del post
            return redirect(reverse_lazy('news:post_detail', kwargs={"pk": comment.post.pk}))
        # Si el usuario es el autor, procesa el formulario para editar el comentario
        # Crea un formulario con los datos del comentario existente
        form = CommentForm(request.POST, instance=comment) # vincula el formulario al comentario existente
        # Verifica si el formulario es válido
        # Si es válido, guarda los cambios y redirige al detalle del post    
        if form.is_valid():
            form.save() 
            return redirect(reverse_lazy('news:post_detail', kwargs={"pk": comment.post.pk}))
        else:
            # Si el formulario no es válido, renderiza de nuevo con el formulario y el comentario
            post = comment.post # Obtiene el post asociado al comentario
            return render(request, 'news/editar_comentario.html', {'form': form, 'comment': comment, 'post': post})
        
class CommentDeleteView(LoginRequiredMixin, View):
    # LoginRequiredMixin se asegura que el usuario esté autenticado antes de acceder a esta vista
    # si no está autenticado, lo redirige a la página de inicio de sesión    
    def get(self, request, pk):
        comment = get_object_or_404(Comentario, pk=pk)
        post = comment.post
        if comment.autor == request.user or request.user.is_staff or request.user.is_superuser:
            return render(request, 'news/confirmar_eliminar_comentario.html', {
                'comment': comment,
                'post': post
            })
        else:
            # si el usuario no es el autor del comentario, redirige a la página de detalle del post
            return redirect(reverse_lazy('news:post_detail', kwargs={"pk": post.pk}))

    def post(self, request, pk):
        comment = get_object_or_404(Comentario, pk=pk)
        post = comment.post 
        if comment.autor == request.user or request.user.is_staff or request.user.is_superuser:
            comment.delete()
            return redirect(reverse_lazy('news:post_detail', kwargs={"pk": post.pk}))
        else:
            # si el usuario no es el autor del comentario, redirige a la página de detalle del post
            return redirect(reverse_lazy('news:post_detail', kwargs={"pk": post.pk}))
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('news:post_detail', pk=post.id)
# Vista para dar o quitar like a un comentario
@login_required
def like_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    if request.user in comentario.me_gusta.all():
        comentario.me_gusta.remove(request.user)
    else:
        comentario.me_gusta.add(request.user)
    return redirect('news:post_detail', pk=comentario.post.pk)

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Gracias por contactarnos! Tu mensaje ha sido enviado correctamente.')
            return redirect('news:contacto')
    else:
        form = ContactoForm()
    
    data = {'form': form}
    return render(request, 'contacto/formulario.html', data)