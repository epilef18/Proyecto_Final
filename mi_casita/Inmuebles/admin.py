from django.contrib import admin
from .models import Inmueble, Region, Comuna

@admin.register(Inmueble)
class InmuebleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'precio_mensual')
    search_fields = ('nombre', 'direccion')
    list_filter = ('precio_mensual', 'comuna')

admin.site.register(Region)
admin.site.register(Comuna)
# Register your models here.
