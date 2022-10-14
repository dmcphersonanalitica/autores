from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mecs/', include('MECS_Autores.urls')),
    path('', include('Login.urls')),
    path('administration/', include('Login.urls2')),
]

if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )