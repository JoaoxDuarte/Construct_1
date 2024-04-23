from django.db import models
from django.template.defaultfilters import slugify #Ela recebe uma str e converte para o padrão de slug

class Categoria(models.Model):
    titulo = models.CharField(max_length=40)
    objects = models.Manager()

    def __str__(self):
        return self.titulo
        
    
class Produto(models.Model):
    nome = models.CharField(max_length=40, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    qtd = models.FloatField()
    preco_compra = models.DecimalField(max_digits=8, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=8, decimal_places=2) #"Tem q ser feito em binario(BinaryField) e não (FloatField), jamais float para não dar problemas com o calculo. Está float apenas para estudo"
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.nome
   
    # slugify
    def save(self, *args, **kwargs):
        # Se não existe um Slug para ele = slugify(self.nome) — ele cria (um slug) baseado no nome
        if not self.slug:
            self.slug = slugify(self.nome)

        # Execute a models da classe pai, só que ele cria antes o self.slug
        return super().save(*args, **kwargs)
    


    def gerar_desconto(self, desconto):
        return self.preco_venda - ((self.preco_venda * desconto)/100)
    
    def lucro(self):
        lucro = self.preco_venda - self.preco_compra
        return (lucro * 100)/self.preco_compra #calculo o valor da variavel lucro em porcentagem %
    
    
class Imagem(models.Model):
    imagem = models.ImageField(upload_to='imagem_produto')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)