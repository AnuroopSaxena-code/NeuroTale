from kafka import KafkaProducer
import pandas as pd 
import json 
import time 
df = pd.read_csv('data/books_large.csv')
df['description'] = 'Placeholder'
df = df[['title','description']].dropna().reset_index(drop=True)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

for index, row in df.iterrows():
    book = {'title': row['title'], 'description': row['description']}
    producer.send('books-topic', value=book)
    print(f"Sent book {index + 1}: {book['title']}")
    time.sleep(1)