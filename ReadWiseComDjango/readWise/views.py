from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


User.objects.create_superuser(username='admin', email='administrador@readwise.com', password='readwise2025')


# Create your views here.
def Index(request):
    return render(request, 'readWise/front/index.html')

def Catalogo(request):
    return render(request, 'readWise/front/Catalogo.html')

@login_required(login_url='entrar')
def Biblioteca(request):
    return render(request, 'readWise/front/Biblioteca.html')

def Planos(request):
    return render(request, 'readWise/front/Planoss.html')

def Entrar(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect('index')  # <--- redireciona para a tela principal
        else:
            return render(request, 'entrar.html', {'erro': 'Usuário ou senha inválidos'})
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
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'readWise/front/login.html', {'erro': 'Email ou senha inválidos'})

    return render(request, 'readWise/front/login.html')

def Logout(request):
    logout(request)
    return redirect('login')

def Cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmacao = request.POST.get('confirmacao')

        if senha != confirmacao:
            return render(request, 'readWise/front/cadastro.html', {'erro': 'Senhas não coincidem'})
        
        if User.objects.filter(username=email).exists():
            return render(request, 'readWise/front/cadastro.html', {'erro': 'Usuário já existe'})
        
        user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
        user.save()
        return redirect('login')
    
    return render(request, 'readWise/front/cadastro.html')

@login_required
def Adm_index(request):
    if request.user.email != 'administrador@readWise.com':
        return redirect('index')

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

def Pagamento(request):
    return render(request, 'readWise/front/pagamento.html')