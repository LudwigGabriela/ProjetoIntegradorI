"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from readWise.views import Index, Catalogo, Biblioteca, Planos, Entrar, Questionario, Carrinho, ContaUsuario, Pedidos, Login, Cadastro, Adm_index, CadastroEbooks, CadastroUsuarios, CadastroAssinaturas, PedidosETransacoes, Configuracoes, SugestoesAssinatura, Promocoes

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Index, name='index'),
    path("catalogo/", Catalogo, name='catalogo'),
    path("biblioteca/", Biblioteca, name='biblioteca'),
    path("planos/", Planos, name='planos'),
    path("entrar", Entrar, name='entrar'),
    path("questionario", Questionario, name='questionario'),
    path("carrinho", Carrinho, name='carrinho'),
    path("usuario", ContaUsuario, name='usuario'),
    path("pedidos", Pedidos, name='pedidos'),
    path("login", Login, name='login'),
    path("cadastro", Cadastro, name='cadastro'),
    path("adm_index", Adm_index, name='adm_index'),
    path("ebooks", CadastroEbooks, name="ebooks"),
    path("cadastro_usuarios", CadastroUsuarios, name='cadastro_usuarios'),
    path("assinaturas", CadastroAssinaturas, name='assinaturas'),
    path("pedidosEtransacoes", PedidosETransacoes, name='pedidosEtransacoes'),
    path("configuracoes", Configuracoes, name='configuracoes'),
    path("promocoes", Promocoes, name='promocoes'),
    path("sugestoesAssinatura", SugestoesAssinatura, name='sugestoesAssinatura')
]
