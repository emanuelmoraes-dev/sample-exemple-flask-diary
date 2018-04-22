from flask import Flask, render_template, request, session, flash, url_for, redirect
from flask.ext.session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

SESSION_TYPE = 'memcache'

sess = Session()
app = Flask(__name__, template_folder=".", static_folder="static")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Anotacao(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    texto = db.Column(db.String(1000))
    date = db.Column(db.DateTime)

db.create_all()
db.session.commit()

@app.route("/")
def menu():
    if 'login' not in session or not session['login']:
        return redirec('/login')
    return render_template('index.html')

@app.route("/escrita")
def escrita():
    if 'login' not in session or not session['login']:
        return redirec('/login')

    date_ini = request.args.get('date_ini')
    date_fim = request.args.get('date_fim')

    anotacoes = []

    if date_ini != None and date_fim != None:
        date_ini = datetime.strptime(date_ini, '%d/%m/%Y')
        date_fim = datetime.strptime(date_fim, '%d/%m/%Y')

        date_ini = date_ini.replace(hour=0, minute=0, second=0)
        date_fim = date_fim.replace(hour=23, minute=59, second=59)

        anotacoes = Anotacao.query.filter(Anotacao.date >= date_ini, Anotacao.date <= date_fim).all()
    else:
        anotacoes = Anotacao.query.all()

    return render_template('escrita.html', anotacoes=anotacoes)

@app.route("/escrevaaqui")
def escreva():
    if 'login' not in session or not session['login']:
        return redirec('/login')

    return render_template('escrevaaqui.html')

@app.route("/salvado")
def salva():

    if 'login' not in session or not session['login']:
        return redirec('/login')

    dia = request.args.get("dia")
    anotacao = Anotacao(texto = dia, date = datetime.now())
    db.session.add(anotacao)
    db.session.flush()
    db.session.commit()
    return render_template('escrevaaqui.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    senha = request.form.get('senha')

    if request.method == 'GET':
        return render_template("login.html")

    if username == 'admin' and senha == 'admin':
        session['login'] = True
        return render_template("index.html")
    else:
        flash("Login Inválido")
        return render_template("login.html")

@app.route("/logout")
def logout():
    session['login'] = False
    return redirec('/login')

if __name__ == "__main__":
    app.secret_key = 'Shhhh! This is a Secret!'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run()
