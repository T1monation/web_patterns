import pika
import random
import time
import requests

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='repair')


def callback(ch, method, properties, body):
    """
    Обработка чтения из очереди
    """
    phone = body
    # Начинаем процедуру ремонта
    repair_time = random.randint(3, 40)
    time.sleep(repair_time)
    # После окончания отправляем запрос на обновление статуса заказа
    requests.post('http://127.0.0.1:5000/change/',
                  data={'phone': phone, 'status': 'DONE'})


channel.basic_consume(queue='repair', on_message_callback=callback)

print('start')
channel.start_consuming()
