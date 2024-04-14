from flask import Flask, render_template, request, jsonify
from kafka import KafkaProducer
import json
from json import dumps  # Importing dumps for JSON serialization

app = Flask(__name__)

# Home page with form to choose transaction input method
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle transaction submission based on user choice
@app.route('/submit', methods=['POST'])
def submit_transaction():
    if request.form.get('choice') == 'single':
        # User chose to enter a single transaction text
        transaction = request.form['transaction']
        produce_to_kafka(transaction)
        return 'Transaction submitted successfully!'
    elif request.form.get('choice') == 'file':
        # User chose to upload a JSON file containing multiple transactions
        file = request.files['file']
        if file and file.filename.endswith('.json'):
            try:
                transactions = json.load(file)
                produce_to_kafka(transactions)
                return 'Transactions submitted successfully!'
            except json.JSONDecodeError:
                return 'Invalid JSON format'
        else:
            return 'Invalid file format or no file uploaded'
    else:
        return 'Invalid choice'

# Kafka producer function to send transactions to Kafka
def produce_to_kafka(transactions):
    # Create a Kafka producer instance
    producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                             api_version=(0, 11, 5),
                             value_serializer=lambda x: dumps(x).encode('utf-8'))

    if isinstance(transactions, list):
        # Send each transaction to Kafka as a JSON-encoded message
        for transaction in transactions:
            producer.send('my-topic', {"transaction": transaction})
    else:
        # For single transaction input, send it as a JSON-encoded message
        producer.send('my-topic', {"transaction": transactions})

    # Flush messages to ensure they are sent to Kafka
    producer.flush()



if __name__ == '__main__':
    app.run(debug=True)
