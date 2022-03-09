import pika
from django.conf import settings

def get_connection():

    credentials = pika.PlainCredentials(
        settings.RABBIT_USER,
        settings.RABBIT_PASS
    )

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBIT_HOST,
        port=settings.RABBIT_PORT,
        credentials=credentials,
    ))

    return connection