from kafka import KafkaConsumer
import json
import pandas as pd
import os
import re

OUTPUT_FILE = '../data/streamed_books.csv'

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

if os.path.exists(OUTPUT_FILE):
    df = pd.read_csv(OUTPUT_FILE)
else:
    df = pd.DataFrame(columns=['title', 'description'])

consumer = KafkaConsumer(
    'books-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='book-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening and cleaning messages...")

for message in consumer:
    book = message.value
    title = clean_text(book.get('title', 'Unknown'))
    desc = clean_text(book.get('description', ''))

    df = df._append({'title': title, 'description': desc}, ignore_index=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved: {title}")