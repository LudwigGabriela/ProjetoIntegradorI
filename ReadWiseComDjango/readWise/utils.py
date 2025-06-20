from django import template

register = template.Library()

@register.filter
def dict_get(dicionario, chave):
    try:
        return dicionario.get(chave)
    except:
        return None
