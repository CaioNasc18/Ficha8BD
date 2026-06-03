from django.contrib import admin
from django.urls import path, include  # Não se esqueça de importar o include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Encaminha os acessos para as rotas da aplicação cybersecurity
    path('', include('cybersecurity.urls')), 
]
