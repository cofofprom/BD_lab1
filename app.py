from confluent_kafka import Consumer
import json
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import streamlit as st

DISPLAY_LIMIT=100

st.set_page_config('Diabetes prediction')

consumer_conf = {
    'bootstrap.servers': 'localhost:9095,localhost:9097',
    'group.id': 'visualization_consumers'
}

if 'preds' not in st.session_state:
    st.session_state['preds'] = []
if 'trues' not in st.session_state:
    st.session_state['trues'] = []

if 'accuracy' not in st.session_state:
    st.session_state['accuracy'] = []
if 'f1' not in st.session_state:
    st.session_state['f1'] = []
if 'precision' not in st.session_state:
    st.session_state['precision'] = []
if 'recall' not in st.session_state:
    st.session_state['recall'] = []

consumer = Consumer(consumer_conf)
consumer.subscribe(['prediction'])

st.title("Diabetes prediction model metrics view")

st.title("Accuracy")
acc_chart = st.empty()
st.title("F1")
f1_chart = st.empty()
st.title("Precision")
prec_chart = st.empty()
st.title("Recall")
rec_chart = st.empty()

while True:
    msg = consumer.poll(1)
    if msg is None: continue
    json_msg = json.loads(msg.value().decode('utf-8'))
    st.session_state['preds'].append(json_msg['pred'])
    st.session_state['trues'].append(json_msg['true'])

    y_true = st.session_state['trues'][-DISPLAY_LIMIT:]
    y_pred = st.session_state['preds'][-DISPLAY_LIMIT:]
    
    st.session_state['accuracy'].append(accuracy_score(y_true, y_pred))
    acc_chart.line_chart(st.session_state['accuracy'])

    st.session_state['f1'].append(f1_score(y_true, y_pred, average='micro'))
    f1_chart.line_chart(st.session_state['f1'])

    st.session_state['precision'].append(precision_score(y_true, y_pred, average='micro'))
    prec_chart.line_chart(st.session_state['precision'])

    st.session_state['recall'].append(recall_score(y_true, y_pred, average='micro'))
    rec_chart.line_chart(st.session_state['recall'])
