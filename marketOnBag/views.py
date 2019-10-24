from django.shortcuts import render, redirect
from django.http import HttpResponse
from marketOnBag.models import *
from datetime import date, datetime

# Create your views here.

def diffDate(data):
    data_atual = date.today()

    data_atual = data_atual.toordinal() #Convertendo em dias
    data = data.toordinal() #Convertendo em dias
    dias = data_atual - data #Diferenca em dias
    anos, dias = dias // 365, dias % 365
    return anos

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        senha = request.POST['senha']

        m = Usuario.objects.get(email=email)
        if m.tipo_usuario == "cliente":
            if m.senha == senha:
                request.session['member_id'] = m.id
                return redirect('/mercados/lista/')
            else:
                args = {
                    'msg': 'Credenciais inválidas'
                }
                return render(request, 'login.html', args)
        else:
            args = {
                'msg': 'Credenciais inválidas'
            }
            return render(request, 'login.html', args)
    return render(request, 'login.html')

def cadastrar(request):
    if request.method == 'POST':
        usuario = Usuario.objects.filter(email = request.POST['email']).first()

        if usuario is None:
            str_date = request.POST['dtnascimento']
            data_nasc = datetime.strptime(str_date, '%Y-%m-%d').date()
            idade = diffDate(data_nasc)

            if idade >= 18:
                data_usuario = Usuario()
                data_usuario.email = request.POST['email']
                data_usuario.tipo_usuario = request.POST['tipo_usuario']
                data_usuario.senha = request.POST['senha']
                data_usuario.save()

                data_pessoa = Pessoa()
                data_pessoa.nome = request.POST['nome']
                data_pessoa.dt_nascimento = request.POST['dtnascimento']
                data_pessoa.usuario = data_usuario
                data_pessoa.endereco_cep = request.POST['cep']
                data_pessoa.endereco_sigla_estado = request.POST['uf']
                data_pessoa.endereco_cidade = request.POST['cidade']
                data_pessoa.endereco_bairro = request.POST['bairro']
                data_pessoa.endereco_rua = request.POST['endereco']
                data_pessoa.endereco_numero = request.POST['numero']
                data_pessoa.endereco_complemento = request.POST['complemento']
                data_pessoa.save()

                args = {
                    'msg': 'Usuário Cadastrado com sucesso!!'
                }
            else: 
                args = {
                    'error': 'Você deve tem que ter pelo menos 18 anos!!'
                }
            return render(request, 'cadastrar-usuario.html', args)
        else:
            args = {
                'error': 'Esse usuário já existe'
            }
        return render(request, 'cadastrar-usuario.html', args)
    return render(request, 'cadastrar-usuario.html')
def listar_mercados(request):

    usuario_email = Usuario.objects.filter(id=request.session['member_id']).first()
    usuario = Pessoa.objects.get(usuario=usuario_email)
    
    listar_mercados = Mercado.objects.filter(ativo=True,endereco_cidade=usuario.endereco_cidade).all()

    args = None
    if listar_mercados.first() is None:
        args = {
            'msg': 'Não existe nenhum mercado cadastrado',
            'usuario': usuario.nome
        }
    else:
        args = {
            'listar_mercados': listar_mercados,
            'usuario': usuario.nome,
            'regiao_usuario': usuario.endereco_cidade
        }

    return render(request, 'mercados.html', args)

def listar_produtos(request, id):
    usuario_email = Usuario.objects.filter(id=request.session['member_id']).first()
    usuario = Pessoa.objects.get(usuario=usuario_email)
    mercado = Mercado.objects.get(id=id)

    listar_produtos = Produto.objects.filter(mercado=mercado.id).all()

    args = None
    if listar_produtos.first() is None:
        args = {
            'msg': 'Não existe nenhum produto cadastrado',
            'mercado': mercado.nome_fantasia,
            'mercado_id': mercado.id,
            'usuario': usuario.nome
        }
    else:
        args = {
            'listar_produtos': listar_produtos,
            'mercado': mercado.nome_fantasia,
            'mercado_id': mercado.id,
            'usuario': usuario.nome,
            'usuario_id': usuario.id
        }

    return render(request, 'produtos.html', args)

def carrinho(request, id):

    usuario_email = Usuario.objects.filter(id=request.session['member_id']).first()
    usuario = Pessoa.objects.get(usuario=usuario_email)
    mercado = Mercado.objects.get(id=id)

    carrinho = Carrinho.objects.filter(pessoa=usuario.id, mercado=mercado.id).all()

    valor_total_produtos = 0
    quantidade_total_produtos = 0

    for item in carrinho:
        valor_total_produtos += item.valor
        quantidade_total_produtos += item.quantidade

    args = None
    if carrinho.first() is None:
        args = {
            'msg': 'Nenhum produto no carrinho',
            'mercado': mercado.nome_fantasia,
            'usuario': usuario.nome
        }
    else:
        args = {
            'carrinho': carrinho,
            'usuario': usuario.nome,
            'mercado': mercado.nome_fantasia,
            'valor_total': valor_total_produtos,
            'quantidade_total': quantidade_total_produtos
        }

    return render(request, 'carrinho.html', args)

def adicionar_produto_carrinho(request):
    if request.method == 'POST':
            
        produto = Produto.objects.get(id=request.POST['produto-id'])

        data_carrinho = Carrinho()
        data_carrinho.quantidade = request.POST['quantidade-produto']
        data_carrinho.valor = float(request.POST['quantidade-produto']) * float(produto.valor)
        data_carrinho.mercado = Mercado.objects.get(ativo=True, id=request.POST['mercado-id'])  
        data_carrinho.produto = Produto.objects.get(id=request.POST['produto-id'])
        data_carrinho.pessoa = Pessoa.objects.get(id=request.POST['usuario-id'])
        data_carrinho.save()

        args = {
            'msg': 'Produto adicionado no carrinho'
        }
    
    return redirect('/mercados/lista/'+str(request.POST['mercado-id'])+'/carrinho')

def delete_produto_carrinho(request, id):
    item = Carrinho.objects.filter(id=id).first()
    carrinho = Carrinho.objects.get(id=id)

    if item is not None:
        item.delete()
    return redirect('/mercados/lista/'+str(carrinho.mercado.id)+'/carrinho')

