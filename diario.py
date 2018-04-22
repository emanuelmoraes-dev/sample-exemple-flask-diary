from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    return render_template('index.html')

@app.route("/escrita")
def escrita():
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
    return render_template('escrevaaqui.html')

@app.route("/salvado")
def salva():
    dia = request.args.get("dia")
    anotacao = Anotacao(texto = dia, date = datetime.now())
    db.session.add(anotacao)
    db.session.flush()
    db.session.commit()
    return render_template('escrevaaqui.html')

if __name__ == "__main__":
    app.run()
