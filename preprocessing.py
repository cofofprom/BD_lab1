from confluent_kafka import Producer, Consumer
import json
import pandas as pd
from joblib import load
import logging

logging.getLogger().setLevel(logging.INFO)

consumer_conf = {
    'bootstrap.servers': 'localhost:9095,localhost:9097',
    'group.id': 'preproc_consumers'
}

producer_conf = {'bootstrap.servers': 'localhost:9095,localhost:9097'}

def preprocess(data, cat_pr, num_pr, num_features_cols):
    data_cat = data.drop(num_features_cols, axis=1)
    oh_data_cat = pd.DataFrame(cat_pr.transform(data_cat),
                               columns=cat_pr.get_feature_names_out(),
                               dtype=int,
                               index=data.index)

    data_num = data[num_features_cols]
    sc_data_num = pd.DataFrame(num_pr.transform(data_num), columns=num_pr.get_feature_names_out(), index=data.index)

    pr_data = pd.concat([oh_data_cat, sc_data_num], axis=1)
    return pr_data

def main():
    consumer = Consumer(consumer_conf)
    consumer.subscribe(['raw_data'])

    producer = Producer(producer_conf)

    cat_prep = load('cat.prep')
    num_prep = load('num.prep')

    non_cat_cols = ['BMI', 'MentHlth', 'PhysHlth', 'Age', 'Income']

    while True:
        msg = consumer.poll(1)
        if msg is None: continue
        json_msg = json.loads(msg.value().decode('utf-8'))
        df = pd.read_json(json_msg)

        features = df.drop('Diabetes_012', axis=1)
        target = df['Diabetes_012']
        
        pr_df = preprocess(features, cat_prep, num_prep, non_cat_cols)

        result = pd.concat([pr_df, target], axis=1)
        result = result.to_json()

        producer.produce('preprocess_data', key="data", value=json.dumps(result))
        producer.flush()

        logging.info(f"Preprocessed data produced")

if __name__ == '__main__':
    main()