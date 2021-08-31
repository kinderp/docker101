import os
import json
from flask import Flask

import pika
import sys

app = Flask(__name__)

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_DBNAME = os.getenv('MONGO_DBNAME')

RABBIT_HOST = os.getenv('RABBIT_HOST')

#CONNECTION = MongoClient()
CLIENTS = None

RABBIT_CONNECTION = None
RABBIT_CHANNEL = None
RABBIT_EXCHANGE = 'events'

@app.route('/add/<filename>')
def add(filename):
     print('Add {}'.format(filename))
     message = {'type': 'add', 'name': filename}
     RABBIT_CHANNEL.basic_publish(exchange=RABBIT_EXCHANGE, routing_key='', body=json.dumps(message))
     return 'Done'

@app.route('/remove/<filename>')
def remove(filename):
    print('Remove {}'.format(filename))
    message = {'type': 'del', 'name': filename}
    RABBIT_CHANNEL.basic_publish(exchange=RABBIT_EXCHANGE, routing_key='', body=json.dumps(message))
    return 'Done'

if __name__ == '__main__':
    print("Load Configuration:")
    print("MONGO_HOST={}".format(MONGO_HOST))
    print("MONGO_DBNAME={}".format(MONGO_DBNAME))
    print("RABIT_HOST={}".format(RABBIT_HOST))

    RABBIT_CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    RABBIT_CHANNEL = RABBIT_CONNECTION.channel()

    RABBIT_CHANNEL.exchange_declare(exchange='events', exchange_type='fanout')

    # message = ' '.join(sys.argv[1:]) or "info: Hello World!"
    # channel.basic_publish(exchange='logs', routing_key='', body=message)
    # print(" [x] Sent %r" % message)
    # connection.close()
    app.run(host='0.0.0.0')
