from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header = 'Vacina paulistana'
admin.site.index_title = 'Painel do Administrador'
urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('vacina_admin_painel/', admin.site.urls),
    path('', include('vacina.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
