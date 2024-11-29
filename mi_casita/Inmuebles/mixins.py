from django.shortcuts import redirect


class ArrendadorRequiredMixin:
    """Mixin para permitir acceso solo a usuarios de tipo 'arrendador'."""

    def dispatch(self, request, *args, **kwargs):
        if (
            not hasattr(request.user, "perfil")
            or request.user.perfil.tipo_usuario != "arrendador"
        ):
            return redirect("acceso_denegado")
        return super().dispatch(request, *args, **kwargs)
