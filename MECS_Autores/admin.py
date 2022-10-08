from django.contrib import admin

# Register your models here.
from MECS_Autores.models import *

admin.site.register(Autores)
admin.site.register(Libros)
admin.site.register(Ventas)
