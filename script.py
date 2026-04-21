import pandas as pd
import time
import requests
import json
import reverse_geocoder as rg  # pip install reverse_geocoder — определяет страну по координатам оффлайн

def send_data(data):
    url = 'http://127.0.0.1:5000/receive'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=json.loads(data), headers=headers)
    return (response.status_code, response.text)


df = pd.read_csv('ip_addresses.csv')

df['timestamp_col'] = pd.to_datetime(df['Timestamp'], unit='s')

# определяем страну для каждой строки по её координатам
coords = list(zip(df['Latitude'], df['Longitude']))
results = rg.search(coords, mode=1)
df['country'] = [r['cc'] for r in results]  # cc это двухбуквенный код страны типо US, RU, CN

min_time = df['Timestamp'].min()
df['time_diff'] = df['Timestamp'] - min_time

# группируем по разнице времени чтобы отправлять пакеты с теми же интервалами что и в данных
df_grouped = df.groupby('time_diff')

prev_sec = 0
for name, group_df in df_grouped:
    time.sleep(name - prev_sec)
    prev_sec = name
    code, text = send_data(group_df.to_json(orient='records'))
    print(code, text)
