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

channel.queue_declare(queue='contactus')

def email_contactus(message):
    channel.basic_publish(exchange='', routing_key='contactus', body=message)
