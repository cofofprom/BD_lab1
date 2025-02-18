from confluent_kafka import Producer, Consumer
import json
import pandas as pd
from joblib import load
from catboost import CatBoostClassifier
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

consumer_conf = {
    'bootstrap.servers': 'localhost:9095,localhost:9097',
    'group.id': 'ml_consumers'
}

producer_conf = {'bootstrap.servers': 'localhost:9095,localhost:9097'}

def main():
    consumer = Consumer(consumer_conf)
    consumer.subscribe(['preprocess_data'])

    producer = Producer(producer_conf)

    clf = CatBoostClassifier().load_model('catboost.model')

    while True:
        msg = consumer.poll(1)
        if msg is None: continue
        json_msg = json.loads(msg.value().decode('utf-8'))
        df = pd.read_json(json_msg)

        features = df.drop('Diabetes_012', axis=1)
        ref_target = df['Diabetes_012']

        y_pred = clf.predict(features)

        data = {'true': ref_target.item(), 'pred': int(y_pred[0][0])}
        producer.produce('prediction', key="data", value=json.dumps(data))
        producer.flush()

if __name__ == '__main__':
    main()