from flask import render_template, request, redirect, url_for, flash
from . import app, mysql
from werkzeug.security import generate_password_hash

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

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO barbers (full_name, cpf, address, nickname, specialty) VALUES (%s, %s, %s, %s, %s)', 
                       (full_name, cpf, address, nickname, specialty))
        mysql.connection.commit()
        cursor.close()
        flash('Barbeiro cadastrado com sucesso!')
        return redirect(url_for('list_barbers'))
    
    return render_template('register_barber.html')

@app.route('/barbers')
def list_barbers():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM barbers')
    barbers = cursor.fetchall()
    cursor.close()
    return render_template('barbers_list.html', barbers=barbers)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_barber(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM barbers WHERE id = %s', (id,))
    barber = cursor.fetchone()

    if request.method == 'POST':
        full_name = request.form['full_name']
        cpf = request.form['cpf']
        address = request.form['address']
        nickname = request.form['nickname']
        specialty = request.form['specialty']

        cursor.execute('UPDATE barbers SET full_name = %s, cpf = %s, address = %s, nickname = %s, specialty = %s WHERE id = %s',
                       (full_name, cpf, address, nickname, specialty, id))
        mysql.connection.commit()
        cursor.close()
        flash('Barbeiro atualizado com sucesso!')
        return redirect(url_for('list_barbers'))
    
    return render_template('edit_barber.html', barber=barber)

@app.route('/delete/<int:id>')
def delete_barber(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM barbers WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
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

        # Lógica de validação (e-mail único, CPF, senhas)
        if password != confirm_password:
            flash('As senhas não coincidem.')
            return redirect(url_for('register_client'))

        # Verificação de e-mail único
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM clients WHERE email = %s', (email,))
        if cursor.fetchone():
            flash('Email já cadastrado.')
            return redirect(url_for('register_client'))

        # Hash da senha
        hashed_password = generate_password_hash(password)

        # Inserir cliente no banco de dados
        cursor.execute('INSERT INTO clients (full_name, cpf, address, phone, email, password) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (full_name, cpf, address, phone, email, hashed_password))
        mysql.connection.commit()
        cursor.close()
        flash('Cliente cadastrado com sucesso!')
        return redirect(url_for('login'))

    return render_template('register_client.html')

