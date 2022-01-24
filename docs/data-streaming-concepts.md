# Data Streaming

## What is Data Streaming?

The term "streaming" is used to describe continuous, never-ending data streams with no beginning or end, that provide a constant feed of data that can be utilized/acted upon without needing to be downloaded first.

<img src=".\img\batch-vs-stream.jpg" alt="batch-vs-stream" style="zoom:80%;" />

## What is Stream Processing

Stream processing is a programming paradigm for computing over events as they arrive.

## What is Kafka?

Apache Kafka is an open-source distributed event streaming platform.

- Permanent storage: store streams of data safely in a distributed, durable, fault-tolerant cluster.
- Scalable: scale production clusters up to a thousand brokers, trillions of messages per day; elastically expand and contract storage and processing.
- High availability: stretch clusters efficiently over availability zones or connect separate clusters across geographic regions.

<img src=".\img\kafka-broker.png" alt="kafka-broker" style="zoom:30%;" />

## How does Kafka work?

- Topic: In Kafka, messages are stored in objects called topics, where the original order messages were produced is maintained. Producers and consumers must always specify a target topic to communicate with.
- Cluster: A Kafka Cluster is composed by a set of broker nodes. Messages can be stored indefinitely in the cluster so applications can process and reprocess messages at their own pace. Keep in mind that storage limitations may arise so you might want to configure retention periods to free up storage.
- Partitions: For redundancy and scalability, topics can be split into multiple partitions, each partition keeping its own ordered log of messages. This means that a single topic may live across multiple brokers.
- Replicas: Replicas are partition copies and every partition has an elected leader replica where producers write messages to and consumer reads messages from. In case of broker failure, one of the follower replicas assume the role of leader to reduce (or avoid) downtime.

We can configure replication for a Kafka cluster, providing default values for new topics. When creating a new topic, however, we can overwrite those values.

- Replication factor: Specifies how many copies of the data we want to have.

- Minimum in sync replicas: Specifies the minimum number of replicas that must acknowledge a write for the write to be considered successful. If this minimum can't be met, the producer raises an exception (either NotEnoughReplicas or NotEnoughReplicasAfterAppend).

If for example we spin up a cluster with 5 brokers and create a topic with a default replication factor of 5 it means that every broker will have a copy of the message. However, by setting the minimum in sync replicas to 4 we ensure that new messages can still be produced even if we lose one node.

**Zookeeper**

ZooKeeper is used in distributed systems for service synchronization and as a naming registry.  For any distributed system, there needs to be a way to coordinate tasks. Technologies like Elasticsearch and MongoDB have their own built-in mechanisms for coordinating tasks, while Kafka was built to use ZooKeeper.

In a Kafka cluster, ZooKeeper is primarily used to track the status of nodes and maintain a list of topics and their configuration, including number of partitions for each topic and location of the replicas.

### Schema Registry

Kafka Producers and Consumers work separately and can be strategically scaled to accommodate distinct workloads. This implies that they don’t know about each other and consequently messages can be written from Producers without respecting a schema that Consumers expect on their end. 

Schema registry is a framework that creates a contract between Producers and Consumers by using Apache Avro schemas. This guarantees messages are written (serialized) and read (deserialized) with the same structure. It also accounts for schema evolution so new messages will not break the Producer/Consumer communication.

### KSQL

With KSQL, you can write real-time streaming applications by using a SQL-like query language.

While in Kafka you store a collection of events in a topic, in ksqlDB you store events in a stream. A stream is a topic with a strongly defined schema. You can issue a *persistent query* to *transform* one stream into another. Persistent queries are little stream processing programs that run indefinitely. It continually reads rows from the source stream, applies the transformation logic, and writes rows to the output stream.

With KSQL you can join messages from multiple topics to produce a unified resultset, and you can also write aggregations.

<img src="C:\Users\SchrodeB\Desktop\kafka-poc\docs\img\ksql-window-aggregation.png" alt="ksql-window-aggregation" style="zoom:25%;" />

### Kafka Streams

Kafka Streams is the Apache Kafka library for writing streaming applications and microservices in Java and Scala. KSQL is an abastraction on top o Kafka Streams.

<img src=".\img\ksql-vs-streams.png" alt="ksql-vs-streams" style="zoom:30%;" />

## Kafka vs Message Queue

**Message queue**:

- Allows asynchronous message delivery;
- Messages get queued if the receiver is not available or can't process messages as fast as they are sent;
- The queue is FIFO;
- Once consumed, the message is removed from the queue;
- Like Kafka, RabitMQ is distributed and scalable.

**Kafka**:

- The key difference is persistence, allowing more than one consumer per topic;
- Since the history of events is preserved, Kafka can be used for event storming.

### KSQL vs Spark SQL

Spark SQL is different from KSQL in the following ways:
- Spark SQL is not an interactive Streaming SQL interface. To do stream processing, you have to switch between writing code using Java/Scala/Python and SQL statements. KSQL, on the other hand, is a completely interactive Streaming SQL engine. You can do sophisticated stream processing operations interactively using SQL statements alone.

- KSQL is a true event-at-a-time Streaming SQL engine. Spark SQL is micro-batch.

> PySpark is an interface for Apache Spark in Python. It supports most of Spark’s features such as Spark SQL, DataFrame, Streaming, MLlib (Machine Learning) and Spark Core.

## References

Kafka documentation: https://kafka.apache.org/documentation/

PENZ, Maikel: Building a Kafka playground on AWS — Part 1: Setting the Foundation. 2020. Available on: https://maikelpenz.medium.com/building-a-kafka-playground-on-aws-part-1-setting-the-foundation-3065ecf51c19.

