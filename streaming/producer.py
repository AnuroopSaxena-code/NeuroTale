from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
# Dummy books for now ^^
books = [
    {"title": "Dracula", "genre": "Horror"},
    {"title": "Harry Potter", "genre": "Fantasy"},
    {"title": "Dune", "genre": "Sci-Fi"}
]

for book in books:
    producer.send('books-topic', book)
    print(f"Sent: {book}")
    time.sleep(1)

producer.flush()