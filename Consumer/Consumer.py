# Consumer.py
# Kafka Consumer that reads transactions and stores fraudulent and non-fraudulent data into MongoDB

from confluent_kafka import Consumer, KafkaException
from pymongo import MongoClient
import json

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVER = "pkc-619z3.us-east1.gcp.confluent.cloud:9092"
KAFKA_API_KEY = "DZXTEBYCNH5H6TEB"
KAFKA_API_SECRET = "7kLHs9wcNu8iMsyIvfkHH+uI+l22UX+4EP+OpVbnHV6+GDkQdr4tIervS2JYL/+m"
KAFKA_TOPIC = "txndata"
KAFKA_GROUP_ID = "fraud-detection-group"

# MongoDB Configuration
MONGO_URI = "mongodb+srv://atstu98:<Your Password>@cluster0.qjsj9xk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB = "txn_db"
MONGO_COLLECTION = "fraud_alerts"

# Initialize MongoDB client and collections
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
collection_non_fraud = db["non_fraud"]

def is_fraudulent(transaction):
    """
    Simple fraud detection logic:
    If amount > 80% of max (5000), mark as fraud.
    """
    fraud_score = transaction['amount'] / 5000
    return fraud_score > 0.8

# Kafka Consumer configuration
conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': KAFKA_API_KEY,
    'sasl.password': KAFKA_API_SECRET,
    'group.id': KAFKA_GROUP_ID,
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([KAFKA_TOPIC])

print(f"Listening for messages on Kafka topic: {KAFKA_TOPIC}")

try:
    while True:
        msg = consumer.poll(1.0)  # Poll every 1 second
        if msg is None:
            continue
        if msg.error():
            print(f"Kafka error: {msg.error()}")
            continue
        
        # Parse transaction from message
        transaction = json.loads(msg.value().decode('utf-8'))
        print(f"Received message from Kafka: {transaction}")

        # Check for fraud and insert into the appropriate MongoDB collection
        if is_fraudulent(transaction):
            print("Fraud detected:", transaction)
            collection.insert_one(transaction)
        else:
            collection_non_fraud.insert_one(transaction)

except Exception as e:
    print(f"Error in consumer: {e}")

finally:
    consumer.close()
