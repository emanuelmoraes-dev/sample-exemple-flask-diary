# Inclui para o sistema as dependências do Flask (O Flask irá disponibilizar ferramentas para criarmos nossa aplicação)
from flask import Flask, render_template, request, session, flash, url_for, redirect
# Inclui para o sistema a classe "Session" que irá dispor de um objeto para armazenar infotmaçoes do usuário que estiver logado no sistema
from flask.ext.session import Session
# Inclui para o sistema o "SQLAlchemy" que irá dispor de ferramentas para a manipulação do banco de dados
from flask_sqlalchemy import SQLAlchemy
# Inclui para o sistema o "datetime" que irá dispor de ferramentas para a monipulação de data e hora
from datetime import datetime

SESSION_TYPE = 'memcache'

# Cria o objeto que representa e gerencia o sistema
# __name__ = nome da aplicação
# template_folder = local onde se localiza os html (o ponto representa a pasta onde se encontra este arquivo)
# static_folder = local onde se localiza os css, javascript e o bootstrap
app = Flask(__name__, template_folder=".", static_folder="static")

# Cria um objeto de sessão que armazenará informações sobre o usuário logado
sess = Session()
# Cria uma senha de criptografia para o objeto de sessão
app.secret_key = 'Shhhh! This is a Secret!'
app.config['SESSION_TYPE'] = 'filesystem'
# Inicializa o objeto de sessão
sess.init_app(app)

'''
OBS: O objeto "session" armazena informações sobre cada usuário logado (usuário que entrou) no sistema.
     session['login'] será igual a "True" se o usuário atual estiver entrado no sistema.
     Se o usuário não estiver logado no sistema, o valor de login será "False" ou inexistente
'''

# Informa para a aplicação a localização do banco de dados Sqlite, que neste caso se localizará na mesma pasta deste arquivo
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Cria um objeto que irá representar, gerenciar o manipular o banco de dados
db = SQLAlchemy(app)

# Classe que informa os valores do objeto a ser salvo no banco de dados (neste caso as anotações digitadas pelo usuário)
class Anotacao(db.Model):
    # Identificador numérico de uma anotação
    id = db.Column(db.Integer, primary_key = True)
    # Conteúdo digitado pelo usuário para a anotação
    texto = db.Column(db.String(1000))
    # Data e hora que a anotação foi realizada
    date = db.Column(db.DateTime)

# Cria toda a estrutura do banco de dados (tabelas) caso a estrutura não tenha sido criada ainda
db.create_all()
db.session.commit()

# Disponibiliza um endereço para ser exibido a página principal do sistema
@app.route("/")
def menu():
    # Se o usuário não estiver logado no sistema será mostrado a tela de login
    if 'login' not in session or not session['login']:
        # mostra a tela de login
        return redirect(url_for('login'))
    # caso o usuário esteja logado, mostra-se a tela principal do sistema
    return render_template('index.html')

# Disponibiliza um endereço para ser exibido a página onde o usuário irá buscar suas anotações
@app.route("/escrita")
def escrita():
    # Se o usuário não estiver logado no sistema será mostrado a tela de login
    if 'login' not in session or not session['login']:
        # mostra a tela de login
        return redirect(url_for('login'))

    # O usuário irá fornecer uma data inicial e uma data final, e todas as anotações
    # realizadas entre estas datas serão exibidas

    # recebe a data inicial por onde será buscado as anotações
    date_ini = request.args.get('date_ini')
    # recebe a data final por onde será buscado as anotações
    date_fim = request.args.get('date_fim')

    # cria uma lista por onde será colocada as anotações buscadas no banco e dados
    anotacoes = []

    # Se o usuário realmente passou uma data inicial e uma data final, então busca-se
    # todas as anotações que foram geradas ente este intervalo e coloca as anotações
    # buscadas na lista "anotacoes"
    if date_ini != None and date_fim != None:
        # converte a data de inicio de texto para uma data real
        date_ini = datetime.strptime(date_ini, '%d/%m/%Y')
        # converte a data de término de texto para uma data real
        date_fim = datetime.strptime(date_fim, '%d/%m/%Y')

        # a data de início começará à meia noite
        date_ini = date_ini.replace(hour=0, minute=0, second=0)
        # a data de termino terminará às 23 horas, 59 minutos e 59 segundos
        date_fim = date_fim.replace(hour=23, minute=59, second=59)

        # Busca as anotações cuja a data de criação é maior ou igual a data_ini
        # e cuja a data de criação é menor ou igual a data_fim
        anotacoes = Anotacao.query.filter(Anotacao.date >= date_ini, Anotacao.date <= date_fim).all()
    else:
        # Caso o usuário não tenha fornecido as duas datas (inicial e final), será buscada
        # todas as anotações do banco de dados
        anotacoes = Anotacao.query.all()

    # mostra para o usuário a tela por onde será exibido as anotações realizadas no diário
    # envia-se para o computador do usuário a lista de anotações buscadas no banco de dados
    return render_template('escrita.html', anotacoes=anotacoes)

# Disponibiliza um endereço por onde será exibido a tela para escrever uma nova anotação
@app.route("/escrevaaqui")
def escreva():
    # Se o usuário não estiver logado no sistema será mostrado a tela de login
    if 'login' not in session or not session['login']:
        # mostra a tela de login
        return redirect(url_for('login'))
    # mostra para o usuário a tela por onde será exibido um campo para escrever uma nova anotação
    return render_template('escrevaaqui.html')

# Disponibiliza um endereço por onde o usuário irá enviar sua anotação para ser salva no banco de dados
@app.route("/salvado")
def salva():
    # Se o usuário não estiver logado no sistema será mostrado a tela de login
    if 'login' not in session or not session['login']:
        # mostra a tela de login
        return redirect(url_for('login'))

    # Coloca na variavel "texto" a anotação digitada pelo cliente
    texto = request.args.get("anotacao")
    # Cria-se um objeto que irá receber o texto digitado e a data atual
    # Este objeto é a representação de uma anotação e será salva no banco
    anotacao = Anotacao(texto = texto, date = datetime.now())
    # Salva no banco a anotação digitada pelo usuário
    db.session.add(anotacao)
    # Confirma a inserção da anotação no banco
    db.session.flush()
    db.session.commit()
    # mostra uma tela pra escrever uma nova anotação, caso o usuário deseje
    return render_template('escrevaaqui.html')

# Disponibiliza um endereço por onde o usuário poderá efetuar login (entrar) no sistema
@app.route("/login", methods=['GET', 'POST'])
def login():

    # Obtém-se o usuário da tela de login
    username = request.form.get('username')
    # Obtém a sena do usuário da tela de login
    senha = request.form.get('senha')

    # Se o usuário está entrando no login pela primeira vez, mostra-se a tela de login
    if request.method == 'GET':
        # mostra a tela de login
        return render_template("login.html")

    # Se o usuário e a senha digitados for "diário" então o usuário irá se logar (entrar) no sistema
    if username == 'diario' and senha == 'diario':
        # Armazena no objeto de sessão que este usuário está logado
        session['login'] = True
        # Mostra a tela principal do sistema
        return render_template("index.html")
    else:
        # Se o usuário ou a senha digitados for inválido mostra-se uma mensagem de erro
        flash("Login Inválido")
        # Se o usuário ou a senha digitados for inválido mostra-se novamente a tela de login
        return render_template("login.html")

# Disponibiliza um endereço por onde o usuário poderá fazer logout (sair do sistema)
@app.route("/logout")
def logout():
    # Armazena no objeto de sessão que este usuário não está mais logado
    session['login'] = False
    # Mostra a tela de login
    return redirect(url_for('login'))

# Se este arquivo foi executado na primeira chamada (ou seja, se é a primeira vez que este arquivo é executado)
if __name__ == "__main__":
    # Executa-se o sistema
    app.run()
