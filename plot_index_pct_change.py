# plot_index_pct_change.py
import os, pandas as pd, matplotlib.pyplot as plt
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
OUTPUT_DIR = os.path.join(ROOT, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

idx = pd.read_csv(os.path.join(OUTPUT_DIR, 'index_timeseries.csv')) if os.path.exists(os.path.join(OUTPUT_DIR, 'index_timeseries.csv')) else None
if idx is None:
    print('index_timeseries.csv missing; run retail_index.py first')
else:
    fig, ax = plt.subplots(figsize=(8,5))
    ax.bar(idx['month'], idx['pct_change'].astype(float))
    ax.set_title('Month-over-Month % Change (smoothed index)')
    ax.set_xlabel('Month')
    ax.set_ylabel('Pct Change')
    plt.xticks(rotation=45)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'index_pct_change.png')
    fig.savefig(out)
    plt.close(fig)
    print('Wrote', out)
