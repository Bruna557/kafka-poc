from confluent_kafka import Consumer, KafkaError
import json

c = Consumer({
    'bootstrap.servers': 'localhost:9091',
    'group.id': 'counting-group',
    'enable.auto.commit': True,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
})

c.subscribe(['car_track'])

def start():
    while True:
        msg = c.poll(0.1)
        if msg is None:
            continue
        elif not msg.error():
            data = json.loads(msg.value())
            result = {data['route_id']: data['vehicle_speed']}
            print(result)
        elif msg.error().code() == KafkaError._PARTITION_EOF:
            print("End of partition reached")
        else:
            print("Error")
