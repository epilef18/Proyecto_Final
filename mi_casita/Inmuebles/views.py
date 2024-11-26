from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm
from .models import Inmueble, Region, PerfilUsuario
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

def registro_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Check if the profile exists, if not create it
            if not hasattr(user, "perfil"):
                PerfilUsuario.objects.create(
                    user=user,
                    tipo_usuario=form.cleaned_data["tipo_usuario"],
                    direccion=form.cleaned_data["direccion"],
                    comuna=form.cleaned_data["comuna"],
                    region=form.cleaned_data["region"],
                )
            # Add a success message to be shown after redirect
            messages.success(request, "Registro exitoso!")
            return redirect("home")  # Redirect to the root URL (or any other view)
    else:
        form = RegistroUsuarioForm()

    return render(request, "registro.html", {"form": form})


def home(request):
    regions = Region.objects.all()
    return render(request, "home.html", {"regions": regions})


def lista_inmuebles_por_region(request, region_id):
    region = get_object_or_404(Region, id=region_id)
    inmuebles = Inmueble.objects.filter(region=region)
    return render(
        request,
        "lista_inmuebles.html",
        {"inmuebles": inmuebles, "region": region},
    )


def detalle_inmueble(request, id):
    inmueble = get_object_or_404(Inmueble, id=id)
    return render(request, "detalle_inmueble.html", {"inmueble": inmueble})


# ------------------manejo de inmuebles por usuario--------------------------
class MiInmueblesListView(LoginRequiredMixin, ListView):
    model = Inmueble
    template_name = "inmuebles_list.html"
    context_object_name = "inmuebles"

    def get_queryset(self):
        return Inmueble.objects.filter(usuario=self.request.user)


class MiInmueblesDetailView(LoginRequiredMixin, DetailView):
    model = Inmueble
    template_name = "vista_inmueble.html"

    def get_queryset(self):
        return Inmueble.objects.filter(usuario=self.request.user)


class MiInmueblesCreateView(LoginRequiredMixin, CreateView):
    model = Inmueble
    fields = [
        "nombre",
        "descripcion",
        "m2_construidos",
        "m2_totales",
        "estacionamientos",
        "habitaciones",
        "banos",
        "direccion",
        "region",
        "comuna",
        "tipo_inmueble",
        "precio_mensual",
        "imagen_inmueble",
    ]
    template_name = "inmuebles_creacion.html"
    success_url = reverse_lazy("inmuebles_list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class MiInmueblesUpdateView(LoginRequiredMixin, UpdateView):
    model = Inmueble
    fields = [
        "nombre",
        "descripcion",
        "m2_construidos",
        "m2_totales",
        "estacionamientos",
        "habitaciones",
        "banos",
        "direccion",
        "region",
        "comuna",
        "tipo_inmueble",
        "precio_mensual",
        "imagen_inmueble",
    ]
    template_name = "inmuebles_form.html"
    success_url = reverse_lazy("inmuebles_list")

    def get_queryset(self):
        return Inmueble.objects.filter(usuario=self.request.user)


class MiInmueblesDeleteView(LoginRequiredMixin, DeleteView):
    model = Inmueble
    template_name = "inmuebles_borrar.html"
    success_url = reverse_lazy("inmuebles_list")

    def get_queryset(self):
        return Inmueble.objects.filter(usuario=self.request.user)
#======= Perfil Usuario
def perfil_usuario(request):
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
    except PerfilUsuario.DoesNotExist:
        # Handle the case where no PerfilUsuario is found for the user
        perfil = (
            None  # Or you could redirect to a create profile page or show a message
        )

    return render(request, "perfil_usuario.html", {"perfil": perfil})
