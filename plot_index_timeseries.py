# plot_index_timeseries.py
import os, pandas as pd, matplotlib.pyplot as plt
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
OUTPUT_DIR = os.path.join(ROOT, 'output')
DATA_DIR = os.path.join(ROOT, 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

idx = pd.read_csv(os.path.join(OUTPUT_DIR, 'index_timeseries.csv')) if os.path.exists(os.path.join(OUTPUT_DIR, 'index_timeseries.csv')) else None
if idx is None:
    print('index_timeseries.csv missing; run retail_index.py first')
else:
    idx['month'] = pd.to_datetime(idx['month'])
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(idx['month'], idx['index'], marker='o')
    ax.plot(idx['month'], idx['index_smooth'], marker='x')
    ax.set_title('Retail Price Index - raw and smoothed')
    ax.set_xlabel('Month')
    ax.set_ylabel('Index')
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'index_timeseries.png')
    fig.savefig(out)
    plt.close(fig)
    print('Wrote', out)
