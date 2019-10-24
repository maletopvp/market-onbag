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

class Mercado(models.Model):
    nome_fantasia = models.CharField(
        max_length=255, verbose_name='Nome Fantasia'
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, null=True
    )
    razao_social = models.CharField(
        max_length=255, verbose_name='Razão Social'
    )
    cnpj = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=u"CNPJ"
    )
    endereco_cep = models.CharField(
        max_length=14, blank=True, null=True, verbose_name=u"CEP"
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
    taxa_entrega = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, verbose_name=u"Taxa de entrega", default=0.00
    )
    criado_em = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome_fantasia

class Produto(models.Model):
    nome = models.CharField(
        max_length=255, verbose_name='Nome Produto'
    )
    quantidade = models.IntegerField(
        blank=True, null=True, verbose_name=u"Quatidade Produto", default=0, validators=[MinValueValidator(0)]
    )
    nome_fabricante = models.CharField(
        max_length=255, verbose_name='Nome Fabricante'
    )
    tipo = models.CharField(
        max_length=255, verbose_name='Tipo de Produto'
    )
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, verbose_name=u"Valor Produto", default=0.00
    )
    desc = models.CharField(
        max_length=1000, blank=True, null=True, verbose_name=u"Descrição Produto"
    )
    mercado = models.ForeignKey(
        Mercado, on_delete=models.CASCADE, null=True
    )
    criado_em = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Carrinho(models.Model):
    quantidade = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    valor = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00
    )
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE
    )
    pessoa = models.ForeignKey(
        Pessoa, on_delete=models.CASCADE
    )
    mercado = models.ForeignKey(
        Mercado, on_delete=models.CASCADE
    )

    criado_em = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return "%s - %s" % (self.pessoa, self.mercado)
