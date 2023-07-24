from flask import Flask, json, request
import sqlite3
import pika
from settings import TABLE_NAME, DB_NAME

app = Flask(__name__)
connection = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = connection.cursor()


@app.route('/')
def index():
    statement = f"SELECT * FROM {TABLE_NAME}"
    cursor.execute(statement)
    result = cursor.fetchall()
    print(result)
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/sale/', methods=['POST'])
def sale():
    data = request.form
    phone = data['phone']
    price = data['price']
    is_sale = True
    status = 'DONE'
    statement = f"INSERT INTO {TABLE_NAME}(phone,price," \
        f"is_sale,status) values (?,?,?,?)"
    cursor.execute(statement, (phone, price, is_sale, status))
    response = app.response_class(
        response=json.dumps({'STATUS': 'OK'}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/repair/', methods=['POST'])
def repair():
    data = request.form
    phone = data['phone']
    price = data['price']
    is_sale = False
    status = 'IN PROCESS'
    statement = f"INSERT INTO {TABLE_NAME}(phone,price," \
        f"is_sale,status) values (?,?,?,?)"
    cursor.execute(statement, (phone, price, is_sale, status))

    # Публикуем сообщение
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='repair')
    channel.basic_publish(exchange='',
                          routing_key='repair',
                          body=phone)
    connection.close()

    response = app.response_class(
        response=json.dumps({'STATUS': 'OK'}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/change/', methods=['POST'])
def change_status():
    data = request.form
    phone = data['phone']
    status = data['status']
    print(status)
    statement = f"UPDATE {TABLE_NAME} set status = ? where phone = ?"
    cursor.execute(statement, (status, phone))

    response = app.response_class(
        response=json.dumps({'STATUS': 'OK'}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(debug=True)
