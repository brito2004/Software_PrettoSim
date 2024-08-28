from flask import render_template, request, redirect, url_for
from app import app
from app.models import Cliente

@app.route('/')
def home():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def register():
    nome_completo = request.form['nome_completo']
    cpf = request.form['cpf']
    endereco = request.form['endereco']
    apelido = request.form['apelido']
    especialidade = request.form['especialidade']
    
    new_user = Cliente(nome_completo, cpf, endereco, apelido, especialidade)
    return redirect(url_for('home'))
