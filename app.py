import json
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS
from confluent_kafka import Consumer, KafkaError
from ksql import KSQLAPI
from threading import Lock
import time

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

socketio = SocketIO(app, cors_allowed_origins="*")
thread = None
thread_lock = Lock()

def avg_speed():
    ksql_client = KSQLAPI('http://localhost:8088')
    query = ksql_client.query(f'select route_id, avg_speed, vehicle_count from avg_speed_table')

    for item in query:
        print(f'item: {item}')
        try:
            res = json.loads(item)
            result = json.dumps({
                'route_id': res['row']['columns'][0], 
                'speed': res['row']['columns'][1], 
                'count': res['row']['columns'][2]
            })
            print(result)
            socketio.emit('avg_speed', {'data': result})
        except Exception as e:
            print(e)
        socketio.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=avg_speed)

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    print('Starting app...')
    socketio.run(app, debug=True, host='127.0.0.1')
