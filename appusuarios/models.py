from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    # Tus campos personalizados van aquí, por ejemplo:
    # telefono = models.CharField(max_length=20, blank=True, null=True)
    # direccion = models.CharField(max_length=255, blank=True, null=True)

    # --- IMPORTANTE: Sobrescribe los campos groups y user_permissions ---
    # Esto es necesario para evitar el conflicto de related_name
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="appusuarios_usuario_set", # <--- ¡Este es el cambio clave!
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="appusuarios_usuario_permissions_set", # <--- ¡Este es el cambio clave!
        related_query_name="usuario",
    )

    class Meta(AbstractUser.Meta):
        # Es crucial que tu modelo de usuario personalizado sea 'swappable'
        # para que Django lo reconozca como el modelo de usuario principal.
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

    def __str__(self):
        return self.username
