from asyncio import sleep
from prometheus_client import PrometheusException, Summary, Counter, start_http_server, Gauge
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY, CollectorRegistry
import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler 

INTERVAL=input("enter the time interval in seconds for next prediction ")

while True:

    # Step 1: Query the data from Prometheus
    query = 'your_promql_query_here'
    # irate(http_requests_total{method="GET", endpoint="/hello"}[1m])
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=10) # last 10 data points
    step = '15s' # adjust this based on your data resolution
    url = 'http://your_prometheus_url/api/v1/query_range?query={}&start={}&end={}&step={}'.format(query, start_time.isoformat(), end_time.isoformat(), step)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['data']['result']
    else:
        raise PrometheusException("Failed to query Prometheus: {}".format(response.content))

    # Step 2: Preprocess the data
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df.set_index('timestamp', inplace=True)
    df.drop(['__name__', 'job', 'instance'], axis=1, inplace=True)
    input_data = df.values # convert to NumPy array

    scaler = MinMaxScaler(feature_range=(0, 1))
    input_data_scaled = scaler.fit_transform(input_data)

    # Step 3: Load the pre-trained modelbi_lstmwith_paper_specs.h5
    model = load_model('bi_lstmwith_paper_specs.h5')

    # Step 4: Make predictions using the loaded model
    predictions = model.predict(input_data_scaled)

  
    


            

    

