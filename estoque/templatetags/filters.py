from django import template
from estoque.models import Imagem

register = template.Library() #para registrar um template

@register.filter(name='get_first_image')
def get_first_image(product):
    imagem = Imagem.objects.filter(produto=product).first() #pego a primeira imagem
    if imagem:
        return imagem.imagem.url #objeto (class) e campo imagem nas models
    else:
        return False


        