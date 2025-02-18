from confluent_kafka import Producer
import pandas as pd
import time
import random
import json
import logging

conf = {
    'bootstrap.servers': 'localhost:9095,localhost:9097'
}

def main():
    logging.getLogger().setLevel(logging.INFO)

    producer = Producer(conf)
    df = pd.read_csv('data.csv')
    num_records = df.shape[0]

    while True:
        rec_idx = random.randint(0, num_records - 1)
        data = df.iloc[[rec_idx]]
        json_data = data.to_json()
        
        producer.produce('raw_data', key="data", value=json.dumps(json_data))
        producer.flush()
        
        logging.info(f"Raw data producer produced: {json_data}")

        tsleep = random.expovariate(1/5)
        time.sleep(tsleep)

if __name__ == '__main__':
    main()