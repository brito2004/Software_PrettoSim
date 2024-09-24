from . import mysql  # Apenas importa o mysql inicializado no __init__.py
import MySQLdb.cursors

class Barber:
    @staticmethod
    def get_all():
        # Use DictCursor para garantir que os resultados sejam dicionários
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM barbers')
        barbers = cursor.fetchall()
        cursor.close()
        return barbers


    @staticmethod
    def get_by_id(id):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM barbers WHERE id = %s', (id,))
        barber = cursor.fetchone()
        cursor.close()
        return barber

    @staticmethod
    def create(full_name, cpf, address, nickname, specialty):
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO barbers (full_name, cpf, address, nickname, specialty) VALUES (%s, %s, %s, %s, %s)', 
                       (full_name, cpf, address, nickname, specialty))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def update(id, full_name, cpf, address, nickname, specialty):
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE barbers SET full_name = %s, cpf = %s, address = %s, nickname = %s, specialty = %s WHERE id = %s',
                       (full_name, cpf, address, nickname, specialty, id))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def delete(id):
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM barbers WHERE id = %s', (id,))
        mysql.connection.commit()
        cursor.close()




class Client:
    @staticmethod
    def find_by_email(email):
        # Use DictCursor para retornar resultados como dicionário
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM clients WHERE email = %s', (email,))
        client = cursor.fetchone()  # Retorna apenas um registro
        cursor.close()
        return client


    @staticmethod
    def create(full_name, cpf, address, phone, email, password):
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO clients (full_name, cpf, address, phone, email, password) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (full_name, cpf, address, phone, email, password))
        mysql.connection.commit()
        cursor.close()
