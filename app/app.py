from flask import Flask, jsonify
import pika
import threading
import json
import spacy
from collections import defaultdict

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

inference_results = defaultdict(dict)

# RabbitMQ connection parameters
rabbitmq_host = 'rabbitmq'
rabbitmq_port = 5672
rabbitmq_user = 'guest'
rabbitmq_password = 'guest'
queue_name = 'inference_queue'


def process_message(channel, method, properties, body):
    message = json.loads(body)
    message_id = message['id']
    input_text = message['input_text']
    
    # Perform NER prediction
    doc = nlp(input_text)
    prediction = [(entity.text, entity.label_) for entity in doc.ents]
    
    # Store the result in the in-memory data structure
    inference_results[message_id] = {'input_text': input_text, 'prediction': prediction}
    
    # Send acknowledgement once the message has been processed
    channel.basic_ack(delivery_tag=method.delivery_tag)


def consume_messages():
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=process_message)
    channel.start_consuming()


@app.route('/prediction/<message_id>', methods=['GET'])
def get_prediction(message_id):
    if message_id in inference_results:
        return jsonify(inference_results[message_id])
    else:
        return jsonify({'error': 'Prediction not found'}), 404


@app.route('/v1/health/live', methods=['GET'])
def liveness():
    return "OK", 200

@app.route('/v1/health/ready', methods=['GET'])
def readiness():
    return "OK", 200


if __name__ == '__main__':
    threading.Thread(target=consume_messages).start()
    app.run(host='0.0.0.0', port=5000)
