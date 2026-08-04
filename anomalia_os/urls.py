from django.contrib import admin
from django.urls import path
from arquivos_scp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.painel_terminal, name='terminal_raiz'),
    path('api/buscar/<str:designacao>/', views.buscar_entidade, name='api_buscar_entidade'),
]

