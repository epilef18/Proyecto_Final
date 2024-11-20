from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm


def registro_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            # Aquí podrías redirigir a otra página de éxito si lo prefieres
            return render(
                request, "registro.html", {"form": form, "mensaje": "Registro exitoso!"}
            )
    else:
        form = (
            RegistroUsuarioForm()
        )  # Esto debe estar en el else para la primera vez que se carga la página

    return render(request, "registro.html", {"form": form})
