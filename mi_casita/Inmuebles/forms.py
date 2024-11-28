from django import forms
from django.contrib.auth.models import User
from .models import PerfilUsuario, Comuna, Region, Inmueble


class RegistroUsuarioForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nombre de Usuario"}
        ),
        label="Nombre de Usuario",
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Correo Electrónico"}
        ),
        label="Correo Electrónico",
    )

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
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Contraseña"}
        ),
        label="Contraseña",
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
                pass
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
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nombre del Inmueble"}
        ),
        label="Nombre",
    )
    descripcion = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Descripción del Inmueble",
                "rows": 3,
            }
        ),
        label="Descripción",
    )
    m2_construidos = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Metros Construidos"}
        ),
        label="Metros Construidos",
    )
    m2_totales = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Metros Totales"}
        ),
        label="Metros Totales",
    )
    estacionamientos = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Número de Estacionamientos"}
        ),
        label="Estacionamientos",
    )
    habitaciones = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Número de Habitaciones"}
        ),
        label="Habitaciones",
    )
    banos = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Número de Baños"}
        ),
        label="Baños",
    )
    direccion = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Dirección del Inmueble"}
        ),
        label="Dirección",
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
    tipo_inmueble = forms.ChoiceField(
        choices=Inmueble.TIPO_INMUEBLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Tipo de Inmueble",
    )
    precio_mensual = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Precio Mensual"}
        ),
        label="Precio Mensual",
    )
    imagen_inmueble = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Imagen del Inmueble",
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


class PerfilUsuarioForm(forms.ModelForm):
    tipo_usuario = forms.ChoiceField(
        choices=PerfilUsuario.USUARIO_TIPOS,
        widget=forms.Select(attrs={"class": "form-control", "id": "id_tipo_usuario"}),
        label="Tipo de Usuario",
    )
    direccion = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "id": "id_direccion"}),
        label="Dirección",
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

    class Meta:
        model = PerfilUsuario
        fields = ["tipo_usuario", "direccion", "comuna", "region"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.region:
            self.fields["comuna"].queryset = Comuna.objects.filter(
                region=self.instance.region
            ).order_by("nombre")
        elif "region" in self.data:
            try:
                region_id = int(self.data.get("region"))
                self.fields["comuna"].queryset = Comuna.objects.filter(
                    region_id=region_id
                ).order_by("nombre")
            except (ValueError, TypeError):
                self.fields["comuna"].queryset = Comuna.objects.none()
        else:
            self.fields["comuna"].queryset = Comuna.objects.none()
