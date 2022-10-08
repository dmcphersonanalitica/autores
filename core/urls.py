from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('mecs/', include('MECS_Autores.urls')),
    path('', include('Login.urls')),
    path('administration/', include('Login.urls2')),
]
