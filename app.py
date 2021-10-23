import json
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from confluent_kafka import Consumer, KafkaError
from threading import Lock
import time

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

socketio = SocketIO(app, cors_allowed_origins="*")
thread = None
thread_lock = Lock()

consumer = Consumer({
    'bootstrap.servers': 'localhost:9091',
    'group.id': 'counting-group',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
})
consumer.subscribe(['car_track'])

def background_thread():
    while True:
        socketio.sleep(3)
        msg = consumer.poll(0.1)
        if msg is None:
            continue
        elif not msg.error():
            data = json.loads(msg.value())
            result = json.dumps({data['route_id']: data['vehicle_speed']})
            print(result)
            socketio.emit('car_detected', {'data': result})
        elif msg.error().code() == KafkaError._PARTITION_EOF:
            print("End of partition reached")
        else:
            print("Error")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    print('Starting app...')
    socketio.run(app, debug=True, host='127.0.0.1')
