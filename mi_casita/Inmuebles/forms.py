from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario, Comuna, Region, Inmueble


class RegistroUsuarioForm(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(
        choices=PerfilUsuario.USUARIO_TIPOS,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Tipo de Usuario",
    )

    direccion = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), label="Dirección"
    )

    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_region"}),
        label="Región",
    )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.none(),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_comuna"}),
        label="Comuna",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Contraseña"
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "region" in self.data:
            try:
                region_id = int(self.data.get("region"))
                self.fields["comuna"].queryset = Comuna.objects.filter(
                    region_id=region_id
                ).order_by("nombre")
            except (ValueError, TypeError):
                pass  # inválido o valor vacío, omite el queryset
        elif self.instance.pk:
            self.fields["comuna"].queryset = self.instance.region.comunas.order_by(
                "nombre"
            )

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


class InmuebleForm(forms.ModelForm):
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_region"}),
        label="Región",
    )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.none(),
        widget=forms.Select(attrs={"class": "form-control", "id": "id_comuna"}),
        label="Comuna",
    )

    class Meta:
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "region" in self.data:
            try:
                region_id = int(self.data.get("region"))
                self.fields["comuna"].queryset = Comuna.objects.filter(
                    region_id=region_id
                ).order_by("nombre")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["comuna"].queryset = self.instance.region.comunas.order_by(
                "nombre"
            )
