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
from readWise.views import Index, Catalogo, Biblioteca, Planos, Entrar, Questionario, Carrinho, ContaUsuario, Pedidos, Login, Cadastro, Adm_index, CadastroEbooks, CadastroUsuarios, CadastroAssinaturas, PedidosETransacoes, Configuracoes, SugestoesAssinatura, Promocoes, Pagamento, Logout, ebooks_api, ebook_detalhe, editar_ebook, excluir_ebook, editar_usuario, excluir_usuario, cadastrar_plano, listar_planos, api_criar_plano, api_listar_planos, editar_plano, excluir_plano, adicionar_ao_carrinho, remover_do_carrinho, plano_detalhe, cadastrar_promocao, promocoes_ativas, editar_promocao, remover_promocao, remover_sugestao
from django.conf import settings
from django.conf.urls.static import static

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
    path("sugestoesAssinatura", SugestoesAssinatura, name='sugestoesAssinatura'),
    path("pagamento", Pagamento, name='pagamento'),
    path("logout", Logout, name='logout'),
    path("ebooks_api", ebooks_api, name='ebooks_api'),
    path("api/ebooks/<int:id>", ebook_detalhe, name='ebook_detalhe'),
    path('ebooks/editar/<int:id>/', editar_ebook, name='editar_ebook'),
    path('ebooks/excluir/<int:id>/', excluir_ebook, name='excluir_ebook'),
    path('editar_usuario/<int:id>/', editar_usuario, name='editar_usuario'),
    path('excluir_usuario/<int:id>/', excluir_usuario, name='excluir_usuario'),
    path('api/planos/', api_listar_planos, name='api_listar_planos'),
    path('api/planos/cadastrar', api_criar_plano, name='api_criar_plano'),
    path("api/planos/editar/<int:id>/", editar_plano, name="editar_plano"),
    path("api/planos/excluir/<int:id>/", excluir_plano, name="excluir_plano"),
    path("carrinho/adicionar", adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path("carrinho/remover/<int:ebook_id>/", remover_do_carrinho, name='remover_do_carrinho'),
    path("api/planos/<int:id>/", plano_detalhe, name="plano_detalhe"),
    path('api/promocoes/cadastrar/', cadastrar_promocao, name='cadastrar_promocao'),
    path('api/promocoes/ativas/', promocoes_ativas, name='promocoes_ativas'),
    path('api/promocoes/<int:id>/editar/', editar_promocao, name='editar_promocao'),
    path('api/promocoes/<int:id>/remover/', remover_promocao, name='remover_promocao'),
    path('remover-sugestao/<int:id>/', remover_sugestao, name='remover_sugestao'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)