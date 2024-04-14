%spark.pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StringType
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import mysql.connector

# Initialize NLTK's sentiment analyzer
nltk.download('vader_lexicon')  # Download required NLTK data
sid = SentimentIntensityAnalyzer()

# Function to perform sentiment analysis on text
def analyze_sentiment(text):
    sentiment_scores = sid.polarity_scores(text)
    # Return the sentiment score (positive, neutral, negative)
    if sentiment_scores['compound'] >= 0.05:
        return 'positive'
    elif sentiment_scores['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# Function to process and insert records into MySQL database
def insert_record(row):
    transaction_value = row["transaction"]
    sentiment = analyze_sentiment(transaction_value)
    print(f"Transaction value: {transaction_value}, Sentiment: {sentiment}")
    
    try:
        # Connect to MySQL database
        connection = mysql.connector.connect(host="mysql", port=3306, database="FRAUDSDB", user="root", password="abc")
        
        if not connection.is_connected():
            print("Failed to connect to MySQL")
            return
        
        sql_insert_query = "INSERT INTO fraudtrans (transaction, sentiment) VALUES (%s, %s)"
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()
        cursor.execute(sql_insert_query, (transaction_value, sentiment))
        connection.commit()
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
    finally:
        # Close the cursor and connection
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Create Spark Session
spark = SparkSession.builder \
    .appName("KafkaSentimentAnalysis") \
    .getOrCreate()

# Connect and read from Kafka topic
kafka_servers = "kafka:9092"
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_servers) \
    .option("subscribe", "my-topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Define JSON schema and parse the value
json_schema = StructType().add("transaction", StringType())
parsed_df = df \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", json_schema).alias("data")) \
    .select("data.*")

# Process each record and write to MySQL with sentiment analysis
query = parsed_df \
    .writeStream \
    .foreach(insert_record) \
    .start()

# Wait for data from Kafka topic
query.awaitTermination()

# Stop the Spark session
spark.stop()
