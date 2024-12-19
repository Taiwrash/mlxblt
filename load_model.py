#!/usr/bin/python3
import pickle
import numpy as np
import pandas as pd

def predict(ipaddr, uacc, dacc, age, tdate, payment_type, oldbalance, newbalance, withdraw):
    with open('./tran_fraud.pkl', 'rb') as file:
        mod = pickle.load(file)
    model = mod['model']
    encoder = mod['encoder']
    payment = mod['payment']
    tdate = pd.to_datetime(tdate, format='%Y-%m-%d', errors='coerce')

    day = tdate.day
    month = tdate.month
    year = tdate.year

    day_sin = np.sin(day * (2. * np.pi / 31))
    day_cos = np.cos(day * (2. * np.pi / 31))
    month_sin = np.sin((month - 1) * (2. * np.pi / 12))
    month_cos = np.cos((month - 1) * (2. * np.pi / 12))

    input_data = pd.DataFrame([[uacc, dacc]], columns=['UserAccount', 'DestinationAccount'])
    transformed = encoder.transform(input_data)
    uacc = transformed.iloc[0, 0]
    dacc = transformed.iloc[0, 1]
    
    payment_type = payment[payment_type]

    X = np.array([ipaddr, uacc, dacc, age, payment_type, withdraw, oldbalance, newbalance,\
                            0.0, 0.0, day, month, year, day_sin, day_cos, month_sin, month_cos])
    print(X)
    res = model.predict(X.reshape(1, -1))[0]
    return res

if __name__ == "__main__":
    print(predict('102896975', 'M1979787155', 'C1231006815', 21, '12/12/2021', 'PAYMENT', 10000, 5000, 5000))