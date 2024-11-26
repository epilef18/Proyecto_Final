from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm
from .models import Inmueble, Region, PerfilUsuario


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm
from .models import PerfilUsuario


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


def perfil_usuario(request):
    try:
        perfil = PerfilUsuario.objects.get(user=request.user)
    except PerfilUsuario.DoesNotExist:
        # Handle the case where no PerfilUsuario is found for the user
        perfil = (
            None  # Or you could redirect to a create profile page or show a message
        )

    return render(request, "perfil_usuario.html", {"perfil": perfil})
