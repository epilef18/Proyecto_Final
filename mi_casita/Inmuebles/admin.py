from django.contrib import admin
from .models import Inmueble, Region, Comuna


@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion", "precio_mensual")
    search_fields = ("nombre", "direccion")
    list_filter = ("precio_mensual", "comuna")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display = ("region", "nombre")
    search_fields = ("region", "nombre")
    list_filter = ("region", "nombre")
