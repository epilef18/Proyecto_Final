from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario, Comuna, Region


class RegistroUsuarioForm(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(
        choices=PerfilUsuario.USUARIO_TIPOS,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Tipo de Usuario",
    )

    direccion = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), label="Dirección"
    )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Comuna",
    )
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Región",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Contraseña"
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            PerfilUsuario.objects.create(
                user=user,
                tipo_usuario=self.cleaned_data["tipo_usuario"],
                direccion=self.cleaned_data["direccion"],
                comuna=self.cleaned_data["comuna"],
                region=self.cleaned_data["region"],
            )
        return user
