from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Reemplaza o añade parámetros GET en la URL actual.
    Uso: {% url_replace param1="value1" param2="value2" %}
    Establezca el valor de un parámetro en Ninguno para eliminarlo.
    """
    query = context['request'].GET.copy()

    # Actualiza o remueve los parámetros según kwargs.
    for key, value in kwargs.items():
        if value is None:
            if key in query:
                del query[key]
        else:
            query[key] = value

    # Asegura de que 'id_categoria', 'buscar', 'fecha' y 'orden' se gestionen correctamente.
    # Esta parte garantiza que, si proporcionas un nuevo 'id_categoria', por ejemplo,
    # este reemplace el anterior correctamente.
    # Esto es más importante si no eliminamos parámetros existentes en kwargs.
    # El diccionario kwargs ya gestiona la configuración del nuevo valor.

    # Convertir a cadena codificada en URL
    return query.urlencode()

@register.simple_tag(takes_context=True)
def url_with_new_params(context, **kwargs):
    """
    Creates a new query string from current GET params,
    overriding or adding parameters specified in kwargs.
    Usage: <a href="?{% url_with_new_params param1='value1' param2='value2' %}">

    This is a simpler version where provided kwargs override existing,
    and other existing params are kept.
    """
    query_params = context['request'].GET.copy()
    for key, value in kwargs.items():
        query_params[key] = value

    # Necesitamos asegurarnos de que "fecha_publicacion" y "orden" sean mutuamente excluyentes.
    # e "id" se sobreescribe correctamente. Esto se gestiona mejor con kwargs explícitos.
    # Por ejemplo, si se configura "fecha_publicacion", se elimina "orden".
    if 'fecha_publicacion' in kwargs and 'orden' in query_params:
        del query_params['orden']
    if 'orden' in kwargs and 'fecha_publiacion' in query_params:
        del query_params['fecha_publicacion']

    return query_params.urlencode()