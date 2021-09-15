from models import Pessoas,Usuarios
# Insere dados na tabela pessoa
def insere_pessoas():
    pessoa = Pessoas(nome='Rafael', idade =26)
    print(pessoa)
    pessoa.save()

# Realiza consulta na tabela pessoa.
def consulta_pessoas():
    #pessoa = Pessoas.query.filter_by(nome = 'Rafael')
    # O comando abaixo traz uma lista de objeto.
    pessoas = Pessoas.query.all()
    print(pessoas)
    #pessoa = Pessoas.query.filter_by(nome='Rafael').first()# pega o primeiro registro
    #print(pessoa.idade)

# Realiza alteração de dados na tabela pessoa.
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Galleani').first()
    pessoa.nome = 'Felipe'
    pessoa.save()

# Realiza exclusão de dados na tabela pessoa.
def exclui_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Fernando').first()
    pessoa.delete()

def insere_usuario(login, senha):
    usuario = Usuarios(login = login, senha = senha)
    usuario.save()

def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)

if __name__ == '__main__':
    #insere_pessoas()
   # altera_pessoa()
    # exclui_pessoa()
    #consulta_pessoas()
    #insere_usuario('Rafael','1234')
    #insere_usuario('Fernando', '777')
    consulta_todos_usuarios()