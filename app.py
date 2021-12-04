import json
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from confluent_kafka import Consumer
from ksql import KSQLAPI
from threading import Lock

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

socketio = SocketIO(app, cors_allowed_origins="*")
car_count_thread = None
avg_speed_thread = None
thread_lock = Lock()

consumer = Consumer({
    'bootstrap.servers': 'localhost:9091',
    'group.id': 'counting-group',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'earliest'}
})
consumer.subscribe(['car_track'])

vehicle_count = {
    '7f788538-9be8-4510-8f01-1758ac269e01': 0,
    'e11d1b63-6724-45c4-b70c-1b8382bb504e': 0,
    'dbaac5ca-5bd5-48dc-b665-70c77619d7f0': 0
}

def car_count():
    print('starting count')
    while True:
        socketio.sleep(1)
        msg = consumer.poll(0.1)
        if msg is None:
            continue
        if not msg.error():
            res = json.loads(msg.value())
            route = res['route_id']
            vehicle_count[route] += 1
            data = json.dumps({
                'route_id': route,
                'count': vehicle_count[route]
            })
            print(data)
            socketio.emit('car_detected', {'data': data})


def avg_speed():
    ksql_client = KSQLAPI('http://localhost:8088')
    query = ksql_client.query(f'select route_id, avg_speed from avg_speed_table')

    print('starting avg_speed')
    for item in query:
        try:
            res = json.loads(item)
            data = json.dumps({
                'route_id': res['row']['columns'][0],
                'speed': res['row']['columns'][1]
            })
            print(data)
            socketio.emit('avg_speed', {'data': data})
        except Exception as e:
            print(e)
        socketio.sleep(.1)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')

    global car_count_thread
    global avg_speed_thread

    with thread_lock:
        if car_count_thread is None:
            car_count_thread = socketio.start_background_task(target=car_count)
        if avg_speed_thread is None:
            avg_speed_thread = socketio.start_background_task(target=avg_speed)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    print('Starting app...')
    socketio.run(app, debug=True, host='127.0.0.1')
