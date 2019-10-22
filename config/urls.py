"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from marketOnBag import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login),
    path('usuario/cadastro', views.cadastrar),
    path('mercados/lista/', views.listar_mercados),
    path('mercados/lista/<int:id>/produtos', views.listar_produtos),
    path('carrinho/adicionar/produto', views.adicionar_produto_carrinho),
    path('mercados/lista/<int:id>/carrinho', views.carrinho),
    path('carrinho/deletar/produto/<int:id>', views.delete_produto_carrinho),
]
