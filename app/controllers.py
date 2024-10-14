from flask import render_template, request, redirect, url_for, flash
from . import app
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Barber, Client, Appointment

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

        if password != confirm_password:
            flash('As senhas não coincidem.')
            return redirect(url_for('register_client'))

        # Verificar se o email já existe
        existing_client = Client.find_by_email(email)
        if existing_client:
            flash('Email já cadastrado.')
            return redirect(url_for('register_client'))

        hashed_password = generate_password_hash(password)
        Client.create(full_name, cpf, address, phone, email, hashed_password)
        flash('Cliente cadastrado com sucesso!')
        return redirect(url_for('login'))

    return render_template('register_client.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        client = Client.find_by_email(email)

        if client and check_password_hash(client[5], password):  # Conferir o índice correto no cliente retornado
            flash('Login realizado com sucesso!')
            return redirect(url_for('list_barbers'))
        else:
            flash('Credenciais inválidas, tente novamente.')
            return redirect(url_for('login'))

    return render_template('login.html')


# ---- Agendamento ----

@app.route('/appointments', methods=['GET', 'POST'])
def create_appointment():
    if request.method == 'POST':
        client_id = request.form['client_id']
        barber_id = request.form['barber_id']
        service_time = request.form['service_time']

        Appointment.create(client_id, barber_id, service_time)
        flash('Agendamento criado com sucesso!')
        return redirect(url_for('list_appointments'))

    clients = Client.get_all()  # Método `get_all()` agora disponível para listar clientes
    barbers = Barber.get_all()  # Listar todos os barbeiros
    return render_template('create_appointment.html', clients=clients, barbers=barbers)

@app.route('/appointments/list')
def list_appointments():
    appointments = Appointment.get_all()
    return render_template('appointments_list.html', appointments=appointments)
