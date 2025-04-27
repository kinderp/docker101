import os
import json
import pika
from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_DBNAME = os.getenv('MONGO_DBNAME')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PWD = os.getenv('MONGO_PWD')
RABBIT_HOST = os.getenv('RABBIT_HOST')

MONGO_CONNECTION = None
MONGO_DB_CONNECTION = None
CLIENTS = None

RABBIT_CONNECTION = None
RABBIT_CHANNEL = None
RABBIT_EXCHANGE = os.getenv('RABBIT_EXCHANGE')


@app.route('/add/<filename>')
def add(filename):
    print('Add {}'.format(filename))
    message = {'type': 'add', 'name': filename}
    to_rabbit = json.dumps(message)
    data = MONGO_DB_CONNECTION.data
    data.insert_one(message)
    RABBIT_CHANNEL.basic_publish(
            exchange=RABBIT_EXCHANGE, routing_key='', body=to_rabbit
    )
    return 'Done'


@app.route('/remove/<filename>')
def remove(filename):
    print('Remove {}'.format(filename))
    message = {'type': 'del', 'name': filename}
    RABBIT_CHANNEL.basic_publish(
            exchange=RABBIT_EXCHANGE, routing_key='', body=json.dumps(message)
    )
    return 'Done'


if __name__ == '__main__':
    print("Load Configuration:")
    print("MONGO_HOST={}".format(MONGO_HOST))
    print("MONGO_DBNAME={}".format(MONGO_DBNAME))
    print("RABIT_HOST={}".format(RABBIT_HOST))

    MONGO_CONNECTION = MongoClient(
            MONGO_HOST,
            username=MONGO_USER,
            password=MONGO_PWD
    )
    MONGO_DB_CONNECTION = MONGO_CONNECTION[MONGO_DBNAME]

    RABBIT_CONNECTION = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_HOST, heartbeat=0)
    )
    RABBIT_CHANNEL = RABBIT_CONNECTION.channel()

    RABBIT_CHANNEL.exchange_declare(exchange='events', exchange_type='fanout')

    app.run(host='0.0.0.0')
