from confluent_kafka import Producer
import json
import uuid
import random
import time

p = Producer({'bootstrap.servers': 'localhost:9091'})

ROUTES = [
    '7f788538-9be8-4510-8f01-1758ac269e01',
    'e11d1b63-6724-45c4-b70c-1b8382bb504e',
    'dbaac5ca-5bd5-48dc-b665-70c77619d7f0',
    '63827b6a-1402-467b-8976-517a8afea3cd',
    'de909b40-fec9-4a7e-907c-f8e411862e5f'
]

def publish_random_event():
    event_id = str(uuid.uuid4())
    event = {
        'event_time': time.time(),
        'route_id': random.choice(ROUTES),
        'vehicle_id': str(uuid.uuid4()),
        'vehicle_speed': round(random.uniform(80,120), 1) # 80.0 to 120.9 km/h
    }
    print(f'event_id: {event_id}, event: {event}')
    p.produce(topic='car_track', key=event_id, value=json.dumps(event))

def start():
    while True:
        publish_random_event()
        time.sleep(5)
