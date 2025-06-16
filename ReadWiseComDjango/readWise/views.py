from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def Index(request):
    return render(request, 'readWise/front/index.html')

def Catalogo(request):
    return render(request, 'readWise/front/Catalogo.html')

def Biblioteca(request):
    return render(request, 'readWise/front/Biblioteca.html')

def Planos(request):
    return render(request, 'readWise/front/Planoss.html')

def Entrar(request):
    return render(request, 'readWise/front/entrar.html')

def Questionario(request):
    return render(request, 'readWise/front/questionario.html')

def Carrinho(request):
    return render(request, 'readWise/front/carrinho.html')

def ContaUsuario(request):
    return render(request, 'readWise/front/conta_usuario.html')

def Pedidos(request):
    return render(request, 'readWise/front/pedidos_status.html')

def Login(request):
    return render(request, 'readWise/front/login.html')

def Cadastro(request):
    return render(request, 'readWise/front/cadastro.html')

def Adm_index(request):
    return render(request, 'readWise/front/index2.html')

def CadastroEbooks(request):
    return render(request, 'readWise/front/ebooks.html')

def CadastroUsuarios(request):
    return render(request, 'readWise/front/usuarios.html')

def CadastroAssinaturas(request):
    return render(request, 'readWise/front/assinaturas.html')

def PedidosETransacoes(request):
    return render(request, 'readWise/front/pedidosEtransacoes.html')

def Configuracoes(request):
    return render(request, 'readWise/front/configuracoes.html')

def Promocoes(request):
    return render(request, 'readWise/front/promocoesSemana.html')

def SugestoesAssinatura(request):
    return render(request, 'readWise/front/sugestoesAssinatura.html')