import os, pika, sys, json
import requests
#from flask import Flask
#from pymongo import MongoClient

#app = Flask(__name__)

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_DBNAME = os.getenv('MONGO_DBNAME')

RABBIT_HOST = os.getenv('RABBIT_HOST')
NGINX_HOST = os.getenv('NGINX_HOST')
#CONNECTION = MongoClient()
CLIENTS = None

#@app.route('/notify/<filename>')
#def notify(filename):
#     print('Add {}'.format(filename))
#     return 'Done'

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange='events', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='events', queue=queue_name)

    def callback(ch, method, properties, body):
        print(" [x] %r" % body.decode())
        message = json.loads(body)
        filename = message.get('name')
        url = "http://{}:8080/{}".format(NGINX_HOST, filename)
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)

    print(' [*] Waiting for events. To exit press CTRL+C')
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    print("Load Configuration:")
    print("MONGO_HOST={}".format(MONGO_HOST))
    print("MONGO_DBNAME={}".format(MONGO_DBNAME))
    print("RABBIT_HOST={}".format(RABBIT_HOST))
    #app.run(host='0.0.0.0')
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
