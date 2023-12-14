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

channel.queue_declare(queue='register')
channel.queue_declare(queue='resetpwd')
channel.queue_declare(queue='delete')

def email_register(message):
    channel.basic_publish(exchange='', routing_key='register', body=message)

def email_resetpwd(message):
    channel.basic_publish(exchange='', routing_key='resetpwd', body=message)

def email_delete(message):
    channel.basic_publish(exchange='', routing_key='delete', body=message)
