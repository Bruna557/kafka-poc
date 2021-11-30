# README

## Running the application

Run Kafka and ksqlDB:

```bash
$ docker-compose up
```

> You may need to allow Docker to access `data/kafka/data` and `data/zookeeper/data`.

Install requirements:

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

Connect to ksql-cli:

```bash
$ docker exec -it ksql-cli ksql http://ksql-server:8088
```

## KSQL commands

create stream car_track_stream (route_id string, vehicle_speed double) with (kafka_topic='car_track',value_format='json');

create table avg_speed_table as select route_id, count(*) as vehicle_count, sum(vehicle_speed)/count(*) as avg_speed from car_track_stream window hopping (size 1 minute, advance by 10 seconds) group by route_id;

select * from avg_speed_table;