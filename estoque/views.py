from django.shortcuts import render, redirect, HttpResponse

from estoque.forms import ProdutoForm
from .models import Categoria, Produto, Imagem


from PIL import Image, ImageDraw
from datetime import date
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.urls import reverse
from django.contrib import messages
from rolepermissions.decorators import has_permission_decorator

@has_permission_decorator('cadastrar_produto')
def add_produto(request):
    if request.method == "GET":
        nome = request.GET.get('nome')
        categoria = request.GET.get('categoria')
        preco_min = request.GET.get('preco_min')
        preco_max = request.GET.get('preco_max')
        produtos = Produto.objects.all()

        if nome or categoria or preco_min or preco_max:
            
            if not preco_min:
                preco_min = 0

            if not preco_max:
                preco_max = 9999999

            if nome:
                produtos = produtos.filter(nome__icontains=nome)

            if categoria:
                produtos = produtos.filter(categoria=categoria)
            produtos = produtos.filter(preco_venda__gte=preco_min).filter(preco_venda__lte=preco_max)

        categorias = Categoria.objects.all()
        
        return render(request, 'add_produto.html', {'categorias': categorias, 'produtos': produtos})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        categoria = request.POST.get('categoria')
        qtd = request.POST.get('qtd')
        preco_compra = request.POST.get('preco_compra')
        preco_venda = request.POST.get('preco_venda')
        #imagens = request.FILES.getlist('imagens')
        
        #Cadastrando Produto
        produto = Produto(nome=nome, categoria_id=categoria, qtd=qtd,
                          preco_compra=preco_compra, preco_venda=preco_venda)
        #Salvar no banco
        produto.save()


        for f in request.FILES.getlist('imagens'):
            name = f'{date.today()}-{produto.id}.jpg'

            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((300, 300))
            draw = ImageDraw.Draw(img) #escreve/desenha algo
            draw.text((20, 280), f"CONSTRUCT {date.today()}", (255, 255, 255))
            output = BytesIO()

            img.save(output, format="JPEG", quality=100)
            output.seek(0) #volta o ponteiro para 
            img_final = InMemoryUploadedFile(output,
                                                    'ImageField',
                                                    name,
                                                    'image/jpeg',
                                                    sys.getsizeof(output),
                                                    None)

            img_dj = Imagem(imagem=img_final, produto=produto)
            img_dj.save()
        messages.add_message(request, messages.SUCCESS, 'Produto cadastrado com sucesso!')

        return redirect(reverse('add_produto')) #Inves de colocar o '/estoque/add_produto' e ter que mudar tudo eu uso o REVERSE

def produto(request, slug):
    if request.method == "GET":
        produto = Produto.objects.get(slug=slug)
        data = produto.__dict__
        data['categoria'] = produto.categoria.id
        form = ProdutoForm(initial=data) # poderia fazer para cada campo, mas levaria muito tempo: initial={'nome': produto.nome}
        return render(request, 'produto.html', {'form': form})