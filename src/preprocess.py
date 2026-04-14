import pandas as pd

def load_data():
    data = pd.read_csv("data/sensor_data.csv")
    return data

def preprocess(data):
    # Handle missing values
    data.fillna(method='ffill', inplace=True)

    # Features and target
    X = data[['temperature', 'vibration', 'current']]
    y = data['failure']

    return X, y