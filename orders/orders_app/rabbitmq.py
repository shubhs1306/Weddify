import pika
from django.conf import settings
import logging
logging.getLogger("pika").setLevel(logging.CRITICAL)


credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host=settings.RABBITMQ_VHOST,
            heartbeat=0,
            blocked_connection_timeout=300,
            credentials=credentials
        )
connection = pika.BlockingConnection(parameters)
channel=connection.channel()

channel.queue_declare(queue='book')
channel.queue_declare(queue='bookvendor')
channel.queue_declare(queue='cancelbook')
channel.queue_declare(queue='cancelbookvendor')

def email_book(message):
    channel.basic_publish(exchange='', routing_key='book', body=message)

def email_bookvendor(message):
    channel.basic_publish(exchange='', routing_key='bookvendor', body=message)

def email_cancelbook(message):
    channel.basic_publish(exchange='', routing_key='cancelbook', body=message)

def email_cancelbookvendor(message):
    channel.basic_publish(exchange='', routing_key='cancelbookvendor', body=message)
