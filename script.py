import os
import pandas as pd
import time
import requests
import json
import reverse_geocoder as rg

FLASK_URL = os.environ.get('FLASK_URL', 'http://127.0.0.1:5000')

# Send a batch of packet data to the Flask server via POST request.
def send_data(data):
    url = f'{FLASK_URL}/receive'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=json.loads(data), headers=headers)
    return (response.status_code, response.text)

# Loading the CSV file
df = pd.read_csv('ip_addresses.csv')

df['timestamp_col'] = pd.to_datetime(df['Timestamp'], unit='s')

# Determine the country for each coordinate using reverse geocoding
coords = list(zip(df['Latitude'], df['Longitude']))
results = rg.search(coords, mode=1)
df['country'] = [r['cc'] for r in results]  # 'cc' contains the two-letter country code

# Calculate time differences to simulate real-time packet arrival
min_time = df['Timestamp'].min()
df['time_diff'] = df['Timestamp'] - min_time

# Group packets by time difference to maintain original intervals
df_grouped = df.groupby('time_diff')

prev_sec = 0
for name, group_df in df_grouped:
    # Sleep for the difference between the current and previous timestamp
    time.sleep(name - prev_sec)
    prev_sec = name

    # Send the grouped packets to the Flask server
    code, text = send_data(group_df.to_json(orient='records'))
    print(code, text)
