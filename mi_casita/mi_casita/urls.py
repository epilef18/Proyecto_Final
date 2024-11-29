from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from Inmuebles.views import (
    buscar,
    perfil_usuario,
    registro_usuario,
    load_comunas,
    home,
    lista_inmuebles_por_region,
    detalle_inmueble,
    editar_perfil,
    MiInmueblesListView,
    MiInmueblesDetailView,
    MiInmueblesCreateView,
    MiInmueblesUpdateView,
    MiInmueblesDeleteView,
    elegircasa,
    invertir,
    elegirarrendatario,
    arriendocompartido,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("registro/", registro_usuario, name="registro"),
    path("ajax/load-comunas/", load_comunas, name="ajax_load_comunas"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("", home, name="home"),
    path(
        "region/<int:region_id>/inmuebles/",
        lista_inmuebles_por_region,
        name="lista_inmuebles_por_region",
    ),
    path(
        "inmueble/user/<int:pk>/",
        MiInmueblesDetailView.as_view(),
        name="vista_inmueble",
    ),
    path("inmuebles/", MiInmueblesListView.as_view(), name="inmuebles_list"),
    path("inmuebles/nuevo/", MiInmueblesCreateView.as_view(), name="inmueble_creacion"),
    path(
        "inmuebles/<int:pk>/editar/",
        MiInmueblesUpdateView.as_view(),
        name="inmueble_form",
    ),
    path(
        "inmuebles/<int:pk>/eliminar/",
        MiInmueblesDeleteView.as_view(),
        name="inmueble_eliminar",
    ),
    path("inmueble/<int:id>/", detalle_inmueble, name="detalle_inmueble"),
    path("perfil/", perfil_usuario, name="perfil_usuario"),
    path("perfil/editar/<int:pk>/", editar_perfil, name="editar_perfil"),
    path("buscar/", buscar, name="buscar"),
    path("elegircasa/", elegircasa, name="Elegir Casa"),
    path("invertir/", invertir, name="Invertir" ),
    path("elegirarrendatario/", elegirarrendatario, name="Elegir Arrendatario" ),
    path("arriendocompartido/", arriendocompartido, name="Arriendo Compartido" ),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
