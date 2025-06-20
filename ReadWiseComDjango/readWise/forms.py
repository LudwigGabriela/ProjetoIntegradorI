from django import forms
from .models import Ebook

class EbookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = ['titulo', 'autor', 'categoria', 'capa', 'preco']

class EscolhaLivroForm(forms.Form):
    genero = forms.ChoiceField(choices=[
        ('Romance', 'Romance'),
        ('Fantasia', 'Fantasia'),
        ('Policial/Suspense', 'Policial/Suspense'),
        ('Acadêmico', 'Acadêmico'),
        ('Completo', 'Completo'),
    ])
    ebook = forms.ModelChoiceField(queryset=Ebook.objects.all())