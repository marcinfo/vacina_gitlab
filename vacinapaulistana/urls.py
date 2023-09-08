from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
admin.AdminSite.site_header = 'Vacina Paulistana'
admin.AdminSite.site_title = 'Painel do Administrador'
admin.AdminSite.index_title ='Painel do Administrador'
urlpatterns = [
    #path('grappelli/', include('grappelli.urls')),
    path('vacina_admin_painel/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
