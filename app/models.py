from . import mysql
import MySQLdb.cursors

class Barber:
    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, full_name FROM barbers')
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
    def get_all():
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT id, full_name FROM clients')
        clients = cursor.fetchall()
        cursor.close()
        return clients

    @staticmethod
    def find_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM clients WHERE email = %s', (email,))
        client = cursor.fetchone()
        cursor.close()
        return client

    @staticmethod
    def create(full_name, cpf, address, phone, email, password):
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO clients (full_name, cpf, address, phone, email, password) VALUES (%s, %s, %s, %s, %s, %s)',
                       (full_name, cpf, address, phone, email, password))
        mysql.connection.commit()
        cursor.close()


class Appointment:
    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor()
        query = '''
            SELECT appointments.id, clients.full_name as client_name, barbers.full_name as barber_name, appointments.service_time
            FROM appointments
            INNER JOIN clients ON appointments.client_id = clients.id
            INNER JOIN barbers ON appointments.barber_id = barbers.id
        '''
        cursor.execute(query)
        appointments = cursor.fetchall()
        cursor.close()
        return appointments

    @staticmethod
    def create(client_id, barber_id, service_time):
        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO appointments (client_id, barber_id, service_time) VALUES (%s, %s, %s)',
            (client_id, barber_id, service_time)
        )
        mysql.connection.commit()
        cursor.close()
