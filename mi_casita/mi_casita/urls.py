from django.contrib import admin
from django.urls import path
from Inmuebles.views import (
    perfil_usuario,
    registro_usuario,
    home,
    lista_inmuebles_por_region,
    detalle_inmueble,
)
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path("admin/", admin.site.urls),
    path("registro/", registro_usuario, name="registro"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("", home, name="home"),
    path(
        "region/<int:region_id>/inmuebles/",
        lista_inmuebles_por_region,
        name="lista_inmuebles_por_region",
    ),
    path("inmueble/<int:id>/", detalle_inmueble, name="detalle_inmueble"),
    path("perfil/", perfil_usuario, name="perfil_usuario"),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

