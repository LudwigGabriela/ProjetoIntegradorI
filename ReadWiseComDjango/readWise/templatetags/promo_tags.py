from django import template
from readWise.models import Promocao

register = template.Library()

@register.simple_tag
def get_promo_for(ebook):
    try:
        promo = Promocao.objects.get(ebook=ebook)
        return promo
    except Promocao.DoesNotExist:
        return None

from django import template

register = template.Library()

@register.filter
def dict_get(dictionary, key):
    return dictionary.get(key)
