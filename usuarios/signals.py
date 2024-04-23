from django.dispatch import receiver  # para saber se ouve ou não uma mudança de estado
from django.db.models.signals import post_save #é a ação, Após salvar (action)
from .models import Users
from rolepermissions.roles import assign_role #define em um user qual q é o comportamento/permissão deve ter

#sender - Qual é a classe que foi feita essa observação, quem é observado?
#instance - Instância Que foi feita a observação. ex: se eu adcionei em user, eu sei o email, o first name etc
#created - Booleano, aquela modificação é a primeira vez? f ou v
#**kwargs é obrigatório

# SIGNAL, implementação do desing patterns OBSERVER - colocar algo para ficar observando determinada classe e, quando a classe mudar de comportamento/estado (ex: salvar no banco), ela vai soltar um sinal e vai chamar uma
#...função para executar uma ação


@receiver(post_save, sender=Users)
def define_permissoes(sender, instance, created, **kwargs):
    if created: # se estiver criando
        if instance.cargo == "V":
            assign_role(instance, 'vendedor')
        elif instance.cargo == "G":
            assign_role(instance, 'gerente')