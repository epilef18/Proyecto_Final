from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm
from .models import Inmueble, Region, PerfilUsuario, Comuna
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import ArrendadorRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from .forms import InmuebleForm, PerfilUsuarioForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


@login_required
def editar_perfil(request, pk):
    perfil = get_object_or_404(PerfilUsuario, pk=pk)
    if request.method == "POST":
        form = PerfilUsuarioForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect("perfil_usuario")
    else:
        form = PerfilUsuarioForm(instance=perfil)
    return render(request, "editar_perfil.html", {"form": form})


def load_comunas(request):
    region_id = request.GET.get("region_id")  # Obtiene el ID de la región
    if region_id:
        try:
            comunas = Comuna.objects.filter(region_id=region_id).order_by("nombre")
            data = [{"id": comuna.id, "nombre": comuna.nombre} for comuna in comunas]
        except Comuna.DoesNotExist:
            data = []  # Si no hay comunas, retorna lista vacía
    else:
        data = []  # Si no se recibe `region_id`, retorna lista vacía
    return JsonResponse(data, safe=False)


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


class MiInmueblesListView(LoginRequiredMixin, ArrendadorRequiredMixin, ListView):
    model = Inmueble
    template_name = "inmuebles_list.html"
    context_object_name = "inmuebles"

    def get_queryset(self):
        return Inmueble.objects.filter(usuario=self.request.user)


class MiInmueblesDetailView(LoginRequiredMixin, ArrendadorRequiredMixin, DetailView):
    model = Inmueble
    template_name = "vista_inmueble.html"

    def get_queryset(self):
        return Inmueble.objects.filter(usuario=self.request.user)


class MiInmueblesCreateView(LoginRequiredMixin, ArrendadorRequiredMixin, CreateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = "inmuebles_creacion.html"
    success_url = reverse_lazy("inmuebles_list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class MiInmueblesUpdateView(LoginRequiredMixin, ArrendadorRequiredMixin, UpdateView):
    model = Inmueble
    form_class = InmuebleForm
    template_name = "inmuebles_form.html"
    success_url = reverse_lazy("inmuebles_list")

    def get_queryset(self):
        return Inmueble.objects.filter(usuario=self.request.user)


class MiInmueblesDeleteView(LoginRequiredMixin, ArrendadorRequiredMixin, DeleteView):
    model = Inmueble
    template_name = "inmuebles_borrar.html"
    success_url = reverse_lazy("inmuebles_list")

    def get_queryset(self):
        return Inmueble.objects.filter(usuario=self.request.user)


def acceso_denegado(request):
    """Vista para mostrar advertencia a usuarios no autorizados."""
    return render(request, "acceso_denegado.html")


# ======= Perfil Usuario
def perfil_usuario(request):
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
    except PerfilUsuario.DoesNotExist:
        perfil = None

    return render(request, "perfil_usuario.html", {"perfil": perfil})


def buscar(request):
    query = request.GET.get("query", "")  # Obtiene el término de búsqueda
    resultados = []

    if query:
        resultados = Inmueble.objects.filter(nombre__icontains=query).order_by("nombre")

    data = [{"id": r.id, "nombre": r.nombre} for r in resultados]
    return JsonResponse(data, safe=False)

def invertir(request):
    return render(request, "invertir.html", {})

def elegirarrendatario(request):
    return render(request, "elegirarrendatario.html", {})

def arriendocompartido(request):
    return render(request, "arriendocompartido.html", {})

def elegircasa(request):
    return render(request, "elegircasa.html", {})


