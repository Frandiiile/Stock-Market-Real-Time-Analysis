from confluent_kafka import Producer
import json
import time
import logging
import pandas as pd

# Configure logger
logging.basicConfig(format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='producer.log',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create Kafka Producer
p = Producer({'bootstrap.servers': 'localhost:9092'})

# Callback function
def receipt(err, msg):
    if err is not None:
        print('Failed to deliver message: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        logger.info(message)
        print(message)

# Read data from CSV file
df = pd.read_csv('stock_data.csv')

# Write Producer loop to publish CSV data
def main():
    for index, row in df.iterrows():
        data = {
            'Open': row['Open'],
            'High': row['High'],
            'Low': row['Low'],
            'Close': row['Close'],
            'Volume': row['Volume'],
            'Stock': row['Stock'],
            'Date': row['Date']
        }
        m = json.dumps(data)
        p.produce('Stock_Topic', m.encode('utf-8'), callback=receipt)
        p.poll(1)
        p.flush()
        time.sleep(1)

if __name__ == '__main__':
    main()
