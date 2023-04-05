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

    #step 5: calculate the number of pods required

    system_running = True 

    while system_running:
        for cdt in CDT:
            # Get predicted workload for next interval
            workload_t_plus_one = Workloadt_plus_one
            # Get current number of pods
            pod_st_plus_one = pod
            # Check if scaling out is required
            if workload_t_plus_one > pod_st_plus_one:
                # Execute scale out command
                EXECUTE_SCALE_OUT_COMMAND(workload_t_plus_one)
            # Check if scaling in is required
            elif workload_t_plus_one < pod_st_plus_one:
                # Calculate number of surplus pods
                pod_surplus = max(pod_st - workload_t_plus_one, 0) * RRS
                # Calculate new number of pods
                pod_st_plus_one = max(workload_t_plus_one, podsmin)
                pod_st_plus_one = max(pod_st - pod_surplus, pod_st_plus_one)
                # Execute scale in command
                EXECUTE_SCALE_IN_COMMAND(pod_st_plus_one)
           # Do nothing if no scaling is required
            else:
                pass
    sleep(INTERVAL)
            

    

