from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import app, mysql
from .models import Client, Barber
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from .models import Client  # Certifique-se de que está importando o modelo Client corretamente


@app.route('/')
def index():
    return redirect(url_for('list_barbers'))

@app.route('/register', methods=['GET', 'POST'])
def register_barber():
    if request.method == 'POST':
        full_name = request.form['full_name']
        cpf = request.form['cpf']
        address = request.form['address']
        nickname = request.form['nickname']
        specialty = request.form['specialty']

        Barber.create(full_name, cpf, address, nickname, specialty)
        flash('Barbeiro cadastrado com sucesso!')
        return redirect(url_for('list_barbers'))
    
    return render_template('register_barber.html')

@app.route('/barbers')
def list_barbers():
    barbers = Barber.get_all()
    return render_template('barbers_list.html', barbers=barbers)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_barber(id):
    barber = Barber.get_by_id(id)
    
    if request.method == 'POST':
        full_name = request.form['full_name']
        cpf = request.form['cpf']
        address = request.form['address']
        nickname = request.form['nickname']
        specialty = request.form['specialty']

        Barber.update(id, full_name, cpf, address, nickname, specialty)
        flash('Barbeiro atualizado com sucesso!')
        return redirect(url_for('list_barbers'))

    return render_template('edit_barber.html', barber=barber)

@app.route('/delete/<int:id>')
def delete_barber(id):
    Barber.delete(id)
    flash('Barbeiro deletado com sucesso!')
    return redirect(url_for('list_barbers'))

@app.route('/register_client', methods=['GET', 'POST'])
def register_client():
    if request.method == 'POST':
        full_name = request.form['full_name']
        cpf = request.form['cpf']
        address = request.form['address']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Verifica se as senhas coincidem
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('register_client'))

        # Verificação de e-mail e CPF únicos
        existing_client = Client.find_by_email_or_cpf(email, cpf)
        if existing_client:
            if existing_client['email'] == email:
                flash('E-mail já cadastrado.', 'danger')
            elif existing_client['cpf'] == cpf:
                flash('CPF já cadastrado.', 'danger')
            return redirect(url_for('register_client'))

        # Hash da senha
        hashed_password = generate_password_hash(password)

        # Inserção do cliente no banco de dados
        Client.create(full_name, cpf, address, phone, email, hashed_password)
        flash('Cliente cadastrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('register_client.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Busca cliente pelo e-mail
        client = Client.find_by_email(email)

        # Verifica se o cliente foi encontrado e se a senha está correta
        if client and check_password_hash(client['password'], password):
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('E-mail ou senha incorretos. Por favor, tente novamente.', 'danger')

    return render_template('login.html')



@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
