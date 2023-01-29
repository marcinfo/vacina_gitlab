from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from .views import index,vacinas_prazos,encontra_ubs,minhas_vacinas,api,links
from .api import apis
urlpatterns = [

    path('',index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('encontra_ubs/',encontra_ubs,name='encontra_ubs'),
    path('vacinas_prazos/',vacinas_prazos,name='vacinas_prazos'),
    path('minhas_vacinas/',minhas_vacinas,name='minhas_vacinas'),
    path('api/',api,name='api'),
    path('links/',links,name='links'),
    path('', include('django.contrib.auth.urls')),
    path('apis/', apis.urls,name = 'VAcinas API'),

]
