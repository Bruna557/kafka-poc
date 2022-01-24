# README

This is a POC developed to showcase the use of Apache Kafka and KSQL to process events in real time.

Consider three Smart Sensors in three different routes. The sensors detect cars and are capable of measuring the speed and publishing an event in a Kafka topic called car_track.

<img src="C:\Users\SchrodeB\Desktop\kafka-poc\docs\img\poc.png" alt="poc" style="zoom: 67%;" />

In `scripts/producer.py` you will find a script that simulates those three sensors publishing events with random data.

The application (app.py) consists of:
- A Kafka Consumer subscribed to car_track topic that will update a counter when new events arrive (giving the number of cars detected per route)
- A KSQL client running a query against avg_speed_table (a KSQL table) to obtain the average speed per route in the last 1 minute (real-time moving window)

Both will emit websocket events (using Flask SocketIO) to update a dashboard in real time.

<img src="C:\Users\SchrodeB\Desktop\kafka-poc\docs\img\poc-architecture.png" alt="poc-architecture" style="zoom:60%;" />

## Running the application

Run Kafka and ksqlDB:

```bash
$ docker-compose up
```

> You may need to allow Docker to access `data/kafka/data` and `data/zookeeper/data`.

Connect to ksql-cli:

```bash
$ docker exec -it ksql-cli ksql http://ksql-server:8088
```

Before running the application, you need to create a KSQL stream and a KSQL table. In order to do so, using ksql-cli, run the following commands:

```
ksql> create stream car_track_stream (route_id string, vehicle_speed double) with (kafka_topic='car_track',value_format='json');
```

```
ksql> create table avg_speed_table as select route_id, count(*) as vehicle_count, sum(vehicle_speed)/count(*) as avg_speed from car_track_stream window hopping (size 1 minute, advance by 10 seconds) group by route_id;
```

Install the application requirements:

```bash
$ pip install -r requirements.txt
```

Run Flask app:

```bash
$ python app.py
```

Start producing events:

```bash
$ venv/Scripts/activate
$ python
>>> from scripts import producer
>>> producer.start()
```
