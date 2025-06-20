from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ReadWise(models.Model):
    titulo = models.CharField(max_length=255, null=False, blank=False)
    autor = models.CharField(max_length=255, null=False, blank=False)
    data_lancamento = models.DateTimeField(auto_now_add=True, null=False, blank=False)

from django.db import models

class Ebook(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    capa = models.ImageField(upload_to='capas/', blank=True, null=True)  # Salva em media/capas/
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.titulo
    
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Ativo', 'Ativo'), ('Não ativo', 'Não ativo')])
    assinante = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name
    
class LivroAdquirido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    data_aquisicao = models.DateTimeField(auto_now_add=True)

class PlanosAssinatura(models.Model):
    nome = models.CharField(max_length=100)
    quantidade_livros = models.PositiveIntegerField()
    generos = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome
    
# models.py
from django.db import models

class ConfiguracaoSistema(models.Model):
    nome_site = models.CharField(max_length=100)
    email_suporte = models.EmailField()
    moeda_padrao = models.CharField(max_length=10)

    livros_gratis_geral = models.PositiveIntegerField(default=0)
    livros_gratis_romance = models.PositiveIntegerField(default=0)
    livros_gratis_policial = models.PositiveIntegerField(default=0)
    livros_gratis_fantasia = models.PositiveIntegerField(default=0)
    livros_gratis_academico = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Configurações do Sistema"
    
    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"

class Pedido(models.Model):
    STATUS_PAGAMENTO = [
        ('analise', 'Pagamento em análise'),
        ('confirmado', 'Pagamento confirmado'),
        ('disponivel', 'Pedido pronto para download'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    status_pagamento = models.CharField(max_length=20, choices=STATUS_PAGAMENTO, default='analise')
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.ebook.titulo}"
    
class ItemCarrinho(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    adicionado_em = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.ebook.preco * self.quantidade

    def __str__(self):
        return f"{self.ebook.titulo} - {self.quantidade}x"
    
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    pago = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=6, decimal_places=2)

class Promocao(models.Model):
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    preco_desconto = models.DecimalField(max_digits=6, decimal_places=2)
    inicio = models.DateField()
    fim = models.DateField()

    def __str__(self):
        return f"{self.ebook.titulo} - R$ {self.preco_desconto}"
    
class LivroGratuitoSelecionado(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    genero = models.CharField(max_length=100)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    mes = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.ebook}"