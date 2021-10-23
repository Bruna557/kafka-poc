# Data Streaming

## What is Data Streaming?

The term "streaming" is used to describe continuous, never-ending data streams with no beginning or end, that provide a constant feed of data that can be utilized/acted upon without needing to be downloaded first.

<img src=".\img\batch-vs-stream.jpg" alt="batch-vs-stream" style="zoom:80%;" />

## What is Kafka

Apache Kafka is an open-source distributed event streaming platform.

- Permanent storage: store streams of data safely in a distributed, durable, fault-tolerant cluster.
- Scalable: ccale production clusters up to a thousand brokers, trillions of messages per day; elastically expand and contract storage and processing.
- High availability: stretch clusters efficiently over availability zones or connect separate clusters across geographic regions.

<img src=".\img\kafka-broker.png" alt="kafka-broker" style="zoom:30%;" />

**Zookeeper**: Kafka uses Apache ZooKeeper to store its metadata, such as the location of partitions and the configuration of topics.

### Kafka vs Message Queue
Message queue
- Allows asynchronous message delivery;
- Messages get queued if the receiver is not available or can't process messages as fast as they are sent;
- The queue is FIFO
- Once consumed, the message is removed from the queue
- Like Kafka, RabitMQ is distributed and scalable

Kafka
- The key difference is persistence, allowing more than one consumer per topic
- Since the history of events is preserved, Kafka can be used for event storming
- Together with real time processing, batch jobs can process events that happened on the last hour or the last 30 days

### KSQL vs Spark SQL

Spark SQL is different from KSQL in the following ways:
- Spark SQL is not an interactive Streaming SQL interface. To do stream processing, you have to switch between writing code using Java/Scala/Python and SQL statements. KSQL, on the other hand, is a completely interactive Streaming SQL engine. You can do sophisticated stream processing operations interactively using SQL statements alone.

- KSQL is a true event-at-a-time Streaming SQL engine. Spark SQL is micro-batch.