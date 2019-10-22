from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.core.validators import MinValueValidator

# Create your models here.
class Usuario(models.Model):
    email = models.EmailField(
        max_length=255, verbose_name='E-mail', unique=True
    )
    senha = models.CharField(
        max_length=16, verbose_name='Senha'
    )
    USER_CHOICES = (
        ("funcionario", "Funcionário"),
        ("cliente", "Cliente")
    )
    tipo_usuario = models.CharField(
        max_length = 255,
        choices = USER_CHOICES,
        blank = True,
        null = True,
        verbose_name=u"Tipo de Usuário",
    )

    def __str__(self):
        return self.email


class Pessoa(models.Model):
    nome = models.CharField(
        max_length=255, verbose_name='Nome'
    )
    dt_nascimento = models.DateField(
        blank=True, null=True, verbose_name=u"Data de Nascimento"
    )
    endereco_cep = models.CharField(
        max_length=200, blank=True, null=True, verbose_name=u"CEP"
    )
    endereco_sigla_estado = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=u"Estado"
    )
    endereco_cidade = models.CharField(
        max_length=500, blank=True, null=True, verbose_name=u"Cidade"
    )
    endereco_bairro = models.CharField(
        max_length=500, blank=True, null=True, verbose_name=u"Bairro"
    )
    endereco_rua = models.CharField(
        max_length=500, blank=True, null=True, verbose_name=u"Rua"
    )
    endereco_numero = models.CharField(
        max_length=500, blank=True, null=True, verbose_name=u"Numero endereço"
    )
    endereco_complemento = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name=u"Complemento"
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, null=True
    )
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome
