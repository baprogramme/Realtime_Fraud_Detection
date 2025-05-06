# Alert.py
# This script monitors MongoDB for new fraudulent transactions and sends an email alert

import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
import time

# SMTP (email) server configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"         # Replace with sender email
EMAIL_PASSWORD = "your_email_password"        # Replace with sender email app password
EMAIL_RECEIVER = "receiver_email@gmail.com"   # Replace with receiver email

def send_email_alert(transaction):
    """
    Send an email alert when fraud is detected.
    """
    subject = "Fraud Alert: Suspicious Transaction Detected!"
    body = f"""
    FRAUD DETECTED
    *****************************
    - Transaction ID: {transaction['transaction_id']}
    - User ID: {transaction['user_id']}
    - Amount: ${transaction['amount']}
    - Merchant: {transaction['merchant']}
    - Location: {transaction['location']}
    ******************************
    Please review this transaction immediately.
    """

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("Email Alert sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# MongoDB configuration
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO_DB = "txn_db"
MONGO_COLLECTION = "fraud_alerts"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def monitor_fraud_transaction():
    """
    Continuously monitor MongoDB for new fraud transactions and trigger email alert.
    """
    print("Monitoring MongoDB for Fraud Transactions...")
    last_checked_id = None

    while True:
        # Get the latest fraud transaction
        latest_fraud = collection.find_one(sort=[("_id", -1)])

        # If it's new, send an email alert
        if latest_fraud and latest_fraud["_id"] != last_checked_id:
            print("New Fraud Transaction Detected:", latest_fraud)
            send_email_alert(latest_fraud)
            last_checked_id = latest_fraud["_id"]
        
        # Check every second
        time.sleep(1)

if __name__ == "__main__":
    monitor_fraud_transaction()
