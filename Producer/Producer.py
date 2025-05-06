# Producer.py
# Author: Your Name
# Description: Kafka producer to generate synthetic transaction data for fraud detection system

from confluent_kafka import Producer
import json
import random
from faker import Faker
import time

# Initialize Faker instance for generating fake data
fake = Faker()

# Kafka configuration
conf = {
    'bootstrap.servers': 'pkc-619z3.us-east1.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': 'DZXTEBYCNH5H6TEB',  # Replace with your Kafka API key or use env variables
    'sasl.password': '7kLHs9wcNu8iMsyIvfkHH+uI+l22UX+4EP+OpVbnHV6+GDkQdr4tIervS2JYL/+m'  # Replace with secret or env variables
}

# Create Kafka producer instance
producer = Producer(conf)

def generated_transactions():
    """
    Generate a fake transaction dictionary.
    """
    transaction = {
        "transaction_id": fake.uuid4(),
        "timestamp": int(time.time()),
        "user_id": random.randint(10000, 99999),
        "amount": round(random.uniform(5, 5000), 2),
        "transaction_type": random.choice(["purchase", "transfer", "withdrawal"]),
        "location": fake.city(),
        "merchant": fake.company(),
        "card_number": fake.credit_card_number()
    }
    return transaction

def delivery_report(err, msg):
    """
    Callback to report the delivery result.
    """
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

if __name__ == "__main__":
    print("Starting Kafka producer to generate transactions...")
    try:
        while True:
            txn = generated_transactions()
            producer.produce(
                "txndata",
                value=json.dumps(txn),
                key=str(txn['user_id']),
                callback=delivery_report
            )
            producer.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Producer stopped.")
