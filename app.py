from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)
#============================================
# Esse hard code é usado quando não houver  =
# autenticação em banco de dados            =
#============================================
# USUARIOS = {                              =
#     'jose':'123',                         =
#     'joao':'456'                          =
# }                                         =
#                                           =
# @auth.verify_password                     =
# def verificacao(login, senha):            =
#     print('Validando usuario.')           =
#     print(USUARIOS.get(login) == senha)   =
#     if not (login, senha):                =
#         return False                      =
#     return USUARIOS.get(login) == senha   =
#============================================

@auth.verify_password # Esse decorador Informa que esse é o método que verifica login e senha.
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login = login, senha = senha).first()

class Pessoa (Resource):
    @auth.login_required # Define que para acessar esse método é preciso estar logado
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome = nome).first()
        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status':'error',
                'mensagem':'Pessoa nao encontrada.'
            }
        return response

    def put(self,nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = 'Pessoa {} excluida com sucesso'.format(pessoa.nome)
        pessoa.delete()
        return {
            'mensagem':mensagem,
            'status':'sucesso'
        }

class ListaPessoas(Resource):
    @auth.login_required # Define que para acessar esse método é preciso estar logado
    def get(self):
        pessoas = Pessoas.query.all()
        #response = [i for i in pessoas] Retorna os objetos e nao o dicionário.
        response = [{'id':i.id,'nome':i.nome,'idade':i.idade} for i in pessoas]
        return response

    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
                }
        return response

class ListaAtividades(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome,'idade':i.pessoa.idade}for i in atividades]
        return response

    def post(self):
        dados = request.json
       # pessoa = Pessoas.query.all()

        #if  dados['pessoa'] not in pessoa.nome:
         #   mensagem = 'Pessoa {} nao cadastrada.'.format(dados['pessoa'])
         #    return {
         #        'status':'Error',
         #        'Mensagem':mensagem
         #    }
        #else:
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome = dados['nome'], pessoa = pessoa)
        atividade.save()
        response = {
                'pessoa':atividade.pessoa.nome,
                'nome':atividade.nome,
                'id':atividade.id
            }
        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/')
if __name__ == '__main__':
    app.run(debug=True)