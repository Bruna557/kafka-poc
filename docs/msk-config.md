# MSK

## MSK Overview

Brokers are the EC2 instances on which Amazon MSK runs the Apache Kafka service. They store messages from producers and serve them to consumers. The performance of an MSK cluster depends on the number and type of brokers.

MSK data storage is backed by Elastic Block Storage (EBS) volumes. Amazon Elastic Block Store (Amazon EBS) provides persistent block-storage volumes for use with Amazon EC2 instances in the AWS Cloud.

## Config

- Cluster name: kafka-poc
- Kafka version: 2.6.2
- Zones: sa-east-1a, sa-east-1b, sa-east-1c
- Brokers per zone: 1
- Total number of brokers: 3
- Broker type: kafka.t3.small
- EBS storage volume per broker: 100 GB
- Cluster configuration: [default MSK configuration]([The Default Amazon MSK Configuration - Amazon Managed Streaming for Apache Kafka](https://docs.aws.amazon.com/msk/latest/developerguide/msk-default-configuration.html))
  - auto.create.topics.enable=false
  - default.replication.factor=3
  - min.insync.replicas=2