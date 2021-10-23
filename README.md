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
$ docker exec -it ksql-cli bash
$ ksql http://ksql-server:8088
```
