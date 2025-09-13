# retail_index.py
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DATA_DIR = os.path.join(ROOT, 'data')
OUTPUT_DIR = os.path.join(ROOT, 'output')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(123)
months = pd.date_range('2024-01-01', periods=12, freq='MS')
skus = [f'SKU_{i:03d}' for i in range(1,51)]
stores = range(1,501)

rows = []
for m in months:
    for s in stores:
        for sku in skus:
            base = np.random.uniform(20,200)
            seasonal = 1 + 0.02*np.sin((m.month/12)*2*np.pi)
            price = base * seasonal * np.random.normal(1, 0.02)
            rows.append({'month': m, 'store_id': s, 'sku': sku, 'price': round(price,2)})
df = pd.DataFrame(rows)
df.to_csv(os.path.join(DATA_DIR, 'price_samples.csv'), index=False)

item_mean = df.groupby(['month','sku'])['price'].mean().reset_index()
base_month = item_mean['month'].min()
base_prices = item_mean[item_mean['month']==base_month][['sku','price']].rename(columns={'price':'base_price'})
merged = item_mean.merge(base_prices, on='sku', how='left')
merged['price_rel'] = merged['price'] / merged['base_price']

index_ts = merged.groupby('month')['price_rel'].mean().reset_index().rename(columns={'price_rel':'index'})

index_ts['index_smooth'] = index_ts['index'].rolling(window=3, min_periods=1).mean()
index_ts['pct_change'] = index_ts['index_smooth'].pct_change().fillna(0)
index_ts['anomaly_flag'] = (index_ts['pct_change'].abs() > 0.05).astype(int)

index_ts.to_csv(os.path.join(OUTPUT_DIR, 'index_timeseries.csv'), index=False)

print('Retail index: price samples and index timeseries created.')
