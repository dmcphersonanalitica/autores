from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mecs/', include('MECS_Autores.urls')),
    path('', include('Login.urls')),
    path('administration/', include('Login.urls2')),
]

urlpatterns = ('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )