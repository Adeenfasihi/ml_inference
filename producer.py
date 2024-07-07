import pika
import uuid
import json

rabbitmq_host = 'localhost'
rabbitmq_port = 5672
rabbitmq_user = 'guest'
rabbitmq_password = 'guest'
queue_name = 'inference_queue'

credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
channel = connection.channel()

message = {
    "id": str(uuid.uuid4()),
    "input_text": "If you ever want to go to London, make sure to visit the British Museum to immerse yourself in centuries of art and history."
}

print(message)
print()

# Use default exchange
channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
connection.close()
