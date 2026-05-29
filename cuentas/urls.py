from django.urls import path
from . import views # <-- El punto significa "busca en esta misma carpeta cuentas"

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_usuario, name='login'),
    path('registro/', views.registro_usuario, name='registro'),
]