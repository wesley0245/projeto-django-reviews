
# Register your models here.

from django.contrib import admin
from .models import Categoria, Tenis, Review # Importe seus modelos

# Registrar os modelos
admin.site.register(Categoria)
admin.site.register(Tenis)
admin.site.register(Review)