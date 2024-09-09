from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = b'\xf0\xf1\xd8\x1d\xab3\x82\xb8\xf58Jp\x0c\x80\x93\xd1\xbf/L\xb2\xd8/\x9d0'

# Configurações de conexão com o MySQL
app.config['MYSQL_HOST'] = '137.184.186.98'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'QuR5trECHoxuhetHlk#p'
app.config['MYSQL_DB'] = 'Barbearia'

mysql = MySQL(app)

# Rota inicial que redireciona para a lista de barbeiros
@app.route('/')
def index():
    return redirect(url_for('list_barbers'))

# C - Criar (Cadastro de Barbeiro)
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

# R - Ler (Listar Barbeiros)
@app.route('/barbers')
def list_barbers():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM barbers')
    barbers = cursor.fetchall()
    cursor.close()
    return render_template('barbers_list.html', barbers=barbers)

# U - Atualizar (Editar Barbeiro)
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

# D - Deletar (Remover Barbeiro)
@app.route('/delete/<int:id>')
def delete_barber(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM barbers WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    flash('Barbeiro deletado com sucesso!')
    return redirect(url_for('list_barbers'))

if __name__ == '__main__':
    app.run(debug=True)
