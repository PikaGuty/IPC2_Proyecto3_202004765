from django.contrib import admin

from .models import Registrados

class AdminRegistrado(admin.ModelAdmin):
    list_display = ["email","nombre","timestamp"]
    list_filter=["timestamp"]
    list_editable=["nombre"]
    search_fields = ["email","nombre"]
    class Meta:
        model = Registrados
admin.site.register(Registrados)
