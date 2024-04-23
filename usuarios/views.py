from django.shortcuts import render, HttpResponse
from rolepermissions.decorators import has_permission_decorator
from .models import Users
from django.shortcuts import redirect #redireciona
from django.urls import reverse #transforma o nome na url
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.contrib import messages


@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor(request):
    if request.method == "GET":
        vendedores = Users.objects.filter(cargo="V") #select de todos os users que são vendedores
        return render(request, 'cadastrar_vendedor.html', {'vendedores': vendedores}) #renderizar html
    if request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        ## TODO: Fazer validações dos dados
        # O GERENTE está tentando cadastrar um vendedor que já existe?
        user = Users.objects.filter(email=email) #filtra por email

        if user.exists():
            # TODO: Utilizar messages do Django
            return HttpResponse('Email já existe!')
        
        #Estamos herdando o Users do Django
        user = Users.objects.create_user(username=email, email=email, password=senha, first_name=nome, last_name=sobrenome, cargo="V")
        # TODO: Redirecionar com uma mensagem
        return HttpResponse('Conta criada!')
   
def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse('plataforma'))
        return render(request, 'login.html')
    elif request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = auth.authenticate(username=login, password=senha)

        #Caso o usuário não exista
        if not user:
            # TODO: redirecionar com mensa de erro
            return HttpResponse('Usuário inválido!')
            
        auth.login(request, user)
        return HttpResponse('Usuário logado com sucesso!')
        
def logout(request):
    request.session.flush() #flush limpa a sessão
    return redirect(reverse('login'))

@has_permission_decorator('cadastrar_vendedor')
def excluir_usuario(request, id):
    vendedor = get_object_or_404(Users, id=id)
    vendedor.delete()
    messages.add_message(request, messages.SUCCESS, 'Vendedor excluido com sucesso!')
    return redirect(reverse('cadastrar_vendedor'))