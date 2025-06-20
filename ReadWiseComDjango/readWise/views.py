from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Ebook
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import Http404
from .forms import EbookForm, EscolhaLivroForm
from .models import PerfilUsuario, LivroAdquirido, PlanosAssinatura, ConfiguracaoSistema, Pedido, ItemCarrinho, ItemPedido, Promocao, LivroGratuitoSelecionado
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django import template

# Create your views here.

def criar_admin():
    admin_email = 'admin@readwise.com'
    admin_senha = 'admin123'

    if not User.objects.filter(username=admin_email).exists():
        User.objects.create_superuser(
            username=admin_email,
            email=admin_email,
            password=admin_senha,
            first_name='Administrador'
        )

def Index(request):
    return render(request, 'readWise/front/index.html')

def Catalogo(request):
    hoje = timezone.now().date()
    ebooks = Ebook.objects.all()
    recomendados = Ebook.objects.all()[:6] 
    promocoes_ativas = Promocao.objects.filter(inicio__lte=hoje, fim__gte=hoje)

    # Cria um dicionário {ebook_id: promocao}
    promocoes_dict = {p.ebook.id: p for p in promocoes_ativas}

    context = {
        'ebooks': ebooks,
        'recomendados': recomendados,
        'promocoes': promocoes_dict
    }
    return render(request, 'readWise/front/Catalogo.html', context)

@login_required(login_url='entrar')
def Biblioteca(request):
    user = request.user

    # Busca os livros comprados pelo usuário
    livros_adquiridos = LivroAdquirido.objects.filter(user=user)
    livros = [item.ebook for item in livros_adquiridos]

    # Verifica se o usuário é assinante
    perfil = PerfilUsuario.objects.filter(user=user).first()
    assinante = perfil.assinante if perfil else False

    # Sugestões só para assinantes
    sugestoes = []
    if assinante:
        sugestoes_qs = LivroGratuitoSelecionado.objects.filter(usuario=user)
        sugestoes = [sugestao.ebook.titulo for sugestao in sugestoes_qs]

    return render(request, 'readWise/front/Biblioteca.html', {
        'usuario': user,
        'livros': livros,
        'sugestoes': sugestoes
    })


def Planos(request):
    return render(request, 'readWise/front/Planoss.html')

@csrf_exempt
def cadastrar_plano(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nome = data.get('nome_plano')
        quantidade = data.get('quantidade')
        generos = data.get('generos')
        preco = data.get('preco')

        if not all([nome, quantidade, generos, preco]):
            return JsonResponse({'erro': 'Todos os campos são obrigatórios'}, status=400)

        plano = PlanosAssinatura.objects.create(
            nome=nome,
            quantidade_livros=quantidade,
            generos=generos,
            preco=preco
        )
        return JsonResponse({'mensagem': 'Plano cadastrado com sucesso!'}, status=201)
    
def listar_planos(request):
    planos = PlanosAssinatura.objects.all().values()
    return JsonResponse(list(planos), safe=False)

def api_listar_planos(request):
    planos = PlanosAssinatura.objects.all()
    dados = [
        {
            "nome": plano.nome,
            "quantidade_livros": plano.quantidade_livros,
            "generos": plano.generos,
            "preco": str(plano.preco)
        }
        for plano in planos
    ]
    return JsonResponse(dados, safe=False)

@csrf_exempt
def api_criar_plano(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            plano = PlanosAssinatura.objects.create(
                nome=data["nome_plano"],
                quantidade_livros=int(data["quantidade"]),
                generos=data["generos"],
                preco=float(data["preco"])
            )
            return JsonResponse({"mensagem": "Plano criado com sucesso!"})
        except Exception as e:
            return JsonResponse({"erro": f"Erro ao criar plano: {str(e)}"}, status=400)
    else:
        return JsonResponse({"erro": "Método não permitido"}, status=405)
    
@csrf_exempt
def excluir_plano(request, id):
    if request.method == 'DELETE':
        plano = get_object_or_404(PlanosAssinatura, id=id)
        plano.delete()
        return JsonResponse({'mensagem': 'Plano excluído com sucesso!'})
    return JsonResponse({'erro': 'Método não permitido'}, status=405)



@csrf_exempt
def editar_plano(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            plano = get_object_or_404(PlanosAssinatura, id=id)
            plano.nome = data.get("nome", plano.nome)
            plano.quantidade_livros = data.get("quantidade_livros", plano.quantidade_livros)
            plano.generos = data.get("generos", plano.generos)
            plano.preco = data.get("preco", plano.preco)
            plano.save()
            return JsonResponse({'mensagem': 'Plano editado com sucesso!'})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)
    return JsonResponse({'erro': 'Método não permitido'}, status=405)

@csrf_exempt
def plano_detalhe(request, id):
    plano = get_object_or_404(PlanosAssinatura, id=id)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            plano.nome = data.get("nome_plano", plano.nome)
            plano.quantidade_livros = int(data.get("quantidade", plano.quantidade_livros))
            plano.generos = data.get("generos", plano.generos)
            plano.preco = float(data.get("preco", plano.preco))
            plano.save()
            return JsonResponse({'mensagem': 'Plano editado com sucesso!'})
        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)

    elif request.method == 'DELETE':
        plano.delete()
        return JsonResponse({'mensagem': 'Plano excluído com sucesso!'})

    return JsonResponse({'erro': 'Método não permitido'}, status=405)


def Entrar(request):
    criar_admin()  

    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        user = authenticate(request, username=username, password=senha)
        
        if user is not None:
            login(request, user)
            if user.username == 'admin@readwise.com':
                return redirect('adm_index')
            else:
                return redirect('index')
        else:
            return render(request, 'readWise/front/entrar.html', {'erro': 'Usuário ou senha inválidos'})
    
    return render(request, 'readWise/front/entrar.html')


def Questionario(request):
    return render(request, 'readWise/front/questionario.html')

@login_required
def Carrinho(request):
    itens = ItemCarrinho.objects.filter(user=request.user)
    total = sum([item.subtotal() for item in itens])
    return render(request, 'readWise/front/carrinho.html', {
        'itens': itens,
        'total': total
    })

@login_required
@csrf_exempt
def adicionar_ao_carrinho(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ebook_id = data.get('ebook_id')

        ebook = get_object_or_404(Ebook, id=ebook_id)
        item, criado = ItemCarrinho.objects.get_or_create(user=request.user, ebook=ebook)

        if not criado:
            item.quantidade += 1
            item.save()

        return JsonResponse({'mensagem': 'Adicionado ao carrinho'})

@login_required
@csrf_exempt
def remover_do_carrinho(request, ebook_id):
    if request.method == 'DELETE':
        item = get_object_or_404(ItemCarrinho, user=request.user, ebook_id=ebook_id)
        item.delete()
        return JsonResponse({'mensagem': 'Removido com sucesso'})

@login_required(login_url='entrar')
def ContaUsuario(request):
    perfil = PerfilUsuario.objects.filter(user=request.user).first()
    livros_comprados = request.user.ebook_set.all() if hasattr(request.user, 'ebook_set') else []

    return render(request, 'readWise/front/conta_usuario.html', {
        'user': request.user,
        'perfil': perfil,
        'livros': [item.ebook for item in livros_comprados]
    })

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

def is_admin(user):
    return user.is_authenticated and user.username == 'admin@readwise.com'


@login_required
def Adm_index(request):
    if not is_admin(request.user):
        return redirect('adm_index')
    return render(request, 'readWise/front/index2.html')



def CadastroEbooks(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        categoria = request.POST.get('categoria')
        capa = request.FILES.get('capa')  # <- recebe imagem enviada
        preco = request.POST.get('preco')

        if titulo and autor and categoria and capa:
            Ebook.objects.create(
                titulo=titulo,
                autor=autor,
                categoria=categoria,
                capa=capa,
                preco=preco
            )
            return redirect('ebooks')

    ebooks = Ebook.objects.all()
    return render(request, 'readWise/front/ebooks.html', {'ebooks': ebooks})


def CadastroUsuarios(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        status = request.POST.get('status')
        assinante = request.POST.get('assinante') == 'Sim'

        if User.objects.filter(username=email).exists():
            return JsonResponse({'erro': 'Usuário já existe'}, status=400)
        
        user = User.objects.create_user(username=email, email=email, password='senha_padrao123', first_name=nome)
        PerfilUsuario.objects.create(user=user, status=status, assinante=assinante)

        return JsonResponse({'mensagem': 'Usuário cadastrado com sucesso!'})

    perfis = PerfilUsuario.objects.select_related('user').all()
    return render(request, 'readWise/front/usuarios.html', {'perfis': perfis})

@csrf_exempt
def editar_usuario(request, id):
    if request.method == 'POST':
        dados = json.loads(request.body)
        nome = dados['nome']
        status = dados['status']
        assinante = dados['assinante'] == 'Sim'

        user = get_object_or_404(User, id=id)
        perfil = get_object_or_404(PerfilUsuario, user=user)

        user.first_name = nome
        perfil.status = status
        perfil.assinante = assinante

        user.save()
        perfil.save()

        return JsonResponse({'mensagem': 'Usuário atualizado com sucesso!'})
    
@csrf_exempt
def excluir_usuario(request, id):
    if request.method == 'DELETE':
        user = get_object_or_404(User, id=id)
        user.delete()
        return JsonResponse({'mensagem': 'Usuário excluído com sucesso!'})

         

def CadastroAssinaturas(request):
    return render(request, 'readWise/front/assinaturas.html')

def PedidosETransacoes(request):
    return render(request, 'readWise/front/pedidosEtransacoes.html')

def Configuracoes(request):
    config = ConfiguracaoSistema.objects.first()
    
    if request.method == "POST":
        if not config:
            config = ConfiguracaoSistema()

        config.nome_site = request.POST.get("nome_site")
        config.email_suporte = request.POST.get("email_suporte")
        config.moeda_padrao = request.POST.get("moeda_padrao")
        config.livros_gratis_geral = request.POST.get("livros_gratis_geral", 0)
        config.livros_gratis_romance = request.POST.get("livros_gratis_romance", 0)
        config.livros_gratis_policial = request.POST.get("livros_gratis_policial", 0)
        config.livros_gratis_fantasia = request.POST.get("livros_gratis_fantasia", 0)
        config.livros_gratis_academico = request.POST.get("livros_gratis_academico", 0)
        config.save()
        return redirect("configuracoes")  

    return render(request, 'readWise/front/configuracoes.html',{"config": config})


def Promocoes(request):
    return render(request, 'readWise/front/promocoesSemana.html')

@csrf_exempt
def cadastrar_promocao(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            ebook = Ebook.objects.get(titulo=data['titulo'])
            desconto = float(data['desconto'].replace(",", "."))
            inicio = datetime.strptime(data['inicio'], "%Y-%m-%d").date()
            fim = datetime.strptime(data['fim'], "%Y-%m-%d").date()

            promocao = Promocao.objects.create(
                ebook=ebook,
                preco_desconto=desconto,
                inicio=inicio,
                fim=fim
            )
            return JsonResponse({"status": "ok", "id": promocao.id})
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)
        
def promocoes_ativas(request):
    hoje = timezone.now().date()
    promocoes = Promocao.objects.filter(inicio__lte=hoje, fim__gte=hoje)
    dados = [{
        "titulo": p.ebook.titulo,
        "autor": p.ebook.autor,
        "capa": p.ebook.capa.url,
        "preco_desconto": str(p.preco_desconto)
    } for p in promocoes]
    return JsonResponse(dados, safe=False)

@csrf_exempt
def editar_promocao(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            promocao = get_object_or_404(Promocao, id=id)
            promocao.preco_desconto = float(data['desconto'].replace(",", "."))
            promocao.inicio = datetime.strptime(data['inicio'], "%Y-%m-%d").date()
            promocao.fim = datetime.strptime(data['fim'], "%Y-%m-%d").date()
            promocao.save()
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)

@csrf_exempt
def remover_promocao(request, id):
    if request.method == 'DELETE':
        try:
            promocao = get_object_or_404(Promocao, id=id)
            promocao.delete()
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "erro", "mensagem": str(e)}, status=400)

@login_required
def SugestoesAssinatura(request):
    form = EscolhaLivroForm()
    livros_selecionados = LivroGratuitoSelecionado.objects.filter(usuario=request.user)

    if request.method == 'POST':
        form = EscolhaLivroForm(request.POST)
        if form.is_valid():
            genero = form.cleaned_data['genero']
            ebook = form.cleaned_data['ebook']

            # Verifica se já foi adicionado
            if not LivroGratuitoSelecionado.objects.filter(usuario=request.user, genero=genero, ebook=ebook).exists():
                LivroGratuitoSelecionado.objects.create(usuario=request.user, genero=genero, ebook=ebook)
            return redirect('sugestoesAssinatura')

    return render(request, 'readWise/front/sugestoesAssinatura.html', {
        'form': form,
        'livros_selecionados': livros_selecionados
    })

def remover_sugestao(request, id):
    if request.method == "POST":
        sugestao = get_object_or_404(LivroGratuitoSelecionado, id=id)
        sugestao.delete()
    return redirect('sugestoesAssinatura') 


@login_required
def Pagamento(request):
    user = request.user
    itens = ItemCarrinho.objects.filter(user=user)

    if request.method == "POST":
        total = sum(item.ebook.preco for item in itens)

        pedido = Pedido.objects.create(user=user, total=total, pago=True)

        for item in itens:
            ItemPedido.objects.create(
                pedido=pedido,
                ebook=item.ebook,
                preco=item.ebook.preco
            )

        # Limpar o carrinho após pagamento
        itens.delete()

        messages.success(request, "Pagamento realizado com sucesso!")
        return redirect('pagina_pedido_realizado')  # crie essa página

    context = {
        'itens': itens,
        'total': sum(item.ebook.preco for item in itens)
    }
    return render(request, 'readWise/front/pagamento.html', context)

@login_required
def Pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).prefetch_related('itens__ebook') 

    return render(request, 'readWise/front/pedidos_status.html', {
        'pedidos': pedidos
    })


@csrf_exempt
def ebooks_api(request):
    if request.method == 'GET':
        ebooks = list(Ebook.objects.values())
        return JsonResponse(ebooks, safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        ebook = Ebook.objects.create(
            titulo=data['titulo'],
            autor=data['autor'],
            categoria=data['categoria'],
            capa_url=data['capa_url']
        )
        return JsonResponse({'mensagem': 'eBook cadastrado com sucesso!'}, status=201)
    
@csrf_exempt
def ebook_detalhe(request, id):
    ebook = get_object_or_404(Ebook, pk=id)

    if request.method == 'DELETE':
        ebook.delete()
        return JsonResponse({'mensagem': 'eBook excluído com sucesso!'}, status=200)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        ebook.titulo = data['titulo']
        ebook.autor = data['autor']
        ebook.categoria = data['categoria']
        ebook.capa_url = data['capa_url']
        ebook.save()
        return JsonResponse({'mensagem': 'eBook atualizado com sucesso!'}, status=200)
    
def editar_ebook(request, id):
    ebook = get_object_or_404(Ebook, pk=id)
    
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES, instance=ebook)
        if form.is_valid():
            form.save()
            return redirect('ebooks')  
    else:
        form = EbookForm(instance=ebook)

    return render(request, 'readWise/front/editar_ebook.html', {'form': form, 'ebook': ebook})

def excluir_ebook(request, id):
    if request.method == 'POST':
        try:
            ebook = Ebook.objects.get(id=id)
            ebook.delete()
        except Ebook.DoesNotExist:
            raise Http404("eBook não encontrado")
    return redirect('ebooks') 