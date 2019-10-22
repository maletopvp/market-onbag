from django.shortcuts import render, redirect
from django.http import HttpResponse
from marketOnBag.models import *

# Create your views here.

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
                'error': 'Esse usuário já existe'
            }

        return render(request, 'cadastrar-usuario.html', args)

    return render(request, 'cadastrar-usuario.html')
