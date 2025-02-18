# Big Data HW 1
## Overview
В работе рассматривается задача классификации. Необходимо предсказать есть ли у пациента диабет или риск развития диабета или он здоров.  
В работе используется 3 продюсера:
- Raw data producer: читает датасет и отправляет случайную запись с топиком raw_data
- Preprocessed data producer: принимает запись от raw data consumer, обрабатывает её при помощи onehot encoding + std scaler и отправляет предобработанную запись с топиком preprocess_data
- ML producer: принимает запись от preprocess data consumer, применяет модель классификатора и отправляет предсказание (и референсный таргет) с топиком prediction  

Соответственно так же используется 3 консюмера: raw data consumer, preprocessed data consumer, ml consumer. Последний работает на стороне streamlit приложения.

В docker compose создаются 2 брокера

## Dataset
В работе использован https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset

## Preprocessing & Model
OneHotEncoder + StandardScaler, в качестве модели был выбран catboost

## Usage
- Raw data producer: python3 generate_data.py
- Raw data consumer + Preprocessed data producer: python3 preprocessing.py
- Preprocessed data consumer + ML producer: python3 ml.py
- ML consumer + metrics visualization: streamlit run app.py

Разные файлы для разных продюсеров дают возможность развернуть всю эту систему на кластере