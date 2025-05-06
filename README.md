
# Real-time Fraud Detection System using Kafka, MongoDB, and Python

## Overview

This project simulates real-time financial transactions, detects fraudulent activities using a Kafka consumer, stores the results in MongoDB, and sends automated email alerts for suspicious transactions.

The system is divided into three key components:
1. **Kafka Producer**: Generates synthetic transaction data in real-time and pushes it to Kafka topics.
2. **Kafka Consumer**: Consumes the transaction data from Kafka, processes it, and segregates fraudulent and non-fraudulent data.
3. **MongoDB Storage & Email Alerts**: Stores the fraud and non-fraud data in MongoDB collections and triggers an email alert whenever a fraudulent transaction is detected.

---

## Project Structure

```
fraud-detection-system/
│
├── producer/
│   ├── producer.py  # Kafka producer to generate synthetic transaction data
│   └── requirements.txt  # Python dependencies for producer
│
├── consumer/
│   ├── consumer.py  # Kafka consumer to detect fraud and store data in MongoDB
│   └── requirements.txt  # Python dependencies for consumer
│
├── alert/
│   ├── alert.py  # Sends email alerts for fraud transactions
│   └── requirements.txt  # Python dependencies for email alerts
│
└── README.md  # Project overview and instructions
```

---

## Installation

To get started with this project, you'll need to install the required Python dependencies.

### Dependencies

The project uses `confluent_kafka`, `pymongo`, and other essential libraries. To install the dependencies for each component, follow the steps below:


## Components

### 1. Kafka Producer (Generating Synthetic Transactions)

This component generates fake transaction data using the `Faker` library and pushes it to Kafka topics.

#### How it works:
- The producer continuously generates random transactions, including:
  - `transaction_id`, `user_id`, `amount`, `timestamp`, `location`, `merchant`, `card_number`, etc.
- These transactions are sent to the Kafka topic `txndata`.
  
**Producer Code:**
```python
from confluent_kafka import Producer
import json
import random
from faker import Faker
import time

# Kafka configuration and transaction generation logic
...
```

---

### 2. Kafka Consumer (Fraud Detection and MongoDB Storage)

This component consumes transaction data from Kafka and determines whether a transaction is fraudulent or not.

#### How it works:
- It processes the transaction data in real-time.
- If the fraud score (calculated by dividing the amount by 5000) exceeds a certain threshold, it classifies the transaction as fraudulent.
- Fraudulent and non-fraudulent transactions are stored in separate MongoDB collections (`fraud_alerts` and `non_fraud`).

**Consumer Code:**
```python
from confluent_kafka import Consumer
from pymongo import MongoClient
import json

# Kafka and MongoDB configuration, fraud detection logic
...
```

---

### 3. Email Alerts (Fraud Notification)

This component sends an email notification whenever a fraudulent transaction is detected.

#### How it works:
- It monitors the MongoDB collection `fraud_alerts` for any new fraudulent transactions.
- Upon detecting a new fraud entry, an email is sent using Gmail's SMTP service to the designated email receiver.

**Email Alert Code:**
```python
import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
import time

# Email sending logic, MongoDB monitoring, fraud detection
...
```

---

## Running the Project

1. **Start the Kafka Producer:**
    - Run the Kafka producer to generate transaction data:
  
    python producer.py
    ```

2. **Start the Kafka Consumer:**
    - Run the Kafka consumer to detect fraudulent transactions and store them in MongoDB:
    ```bash
    python consumer.py
    ```

3. **Start the Email Alert System:**
    - Run the email alert system to monitor fraud transactions and send notifications:
    ```bash
    python alert.py
    ```

---

## Configuration

1. **Kafka Configuration**:  
    Ensure that the Kafka configuration details (e.g., `bootstrap.servers`, `sasl.username`, and `sasl.password`) are correctly set in all components.

2. **MongoDB Configuration**:  
    Update the MongoDB URI with your connection details in the **Consumer** and **Email Alert** components.

3. **Email Credentials**:  
    For sending emails, update the Gmail credentials in the **Email Alert** component.

---

## Contributions

Contributions to improve the fraud detection logic or the system architecture are welcome! Feel free to open a pull request or create an issue if you find any bugs or have suggestions.


---

## Conclusion

This real-time fraud detection system is designed to showcase the integration of Kafka, MongoDB, and email notifications to detect and alert on fraudulent transactions. It's a robust solution for monitoring financial transactions and ensuring secure operations.
