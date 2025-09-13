# Retail_Index_Construction_and_Monitoring
 Retail Sampling & Indexing Projects

This repository contains three practical projects aligned to the NIQ Data Scientist (PDE) role:
1. Retail Sales Universe Estimation
2. Store Sample Design Optimization
3. Retail Index Construction & Monitoring

## How to run
1. Create a Python environment and install required packages:
   ```bash
   python -m venv niq_env
   source niq_env/bin/activate   # Windows: niq_env\Scripts\activate
   pip install pandas numpy scikit-learn matplotlib pillow
   ```
2. Run the scripts in order (each project has a `notebooks/` script):
   ```bash
   python Retail_Sales_Universe_Estimation/notebooks/universe_estimation.py
   python Store_Sample_Design_Optimization/notebooks/sample_design_optimization.py
   python Retail_Index_Construction_and_Monitoring/notebooks/retail_index.py
   ```
3. Generate the PNG plots for dashboards (each plotter reads produced CSVs):
   ```bash
   python Retail_Sales_Universe_Estimation/plots/plot_stratum_counts.py
   python Retail_Sales_Universe_Estimation/plots/plot_sales_distribution.py
   python Store_Sample_Design_Optimization/plots/plot_cluster_counts.py
   python Store_Sample_Design_Optimization/plots/plot_selected_vs_pop_sales.py
   python Retail_Index_Construction_and_Monitoring/plots/plot_index_timeseries.py
   python Retail_Index_Construction_and_Monitoring/plots/plot_index_pct_change.py
   ```

## Power BI Visualization Instructions (step-by-step)

### A) Retail Sales Universe Estimation — Validation Dashboard
**Data files:** `Retail_Sales_Universe_Estimation/data/retail_population.csv`, `Retail_Sales_Universe_Estimation/output/stratified_sample.csv`, `Retail_Sales_Universe_Estimation/output/estimation_results.csv`

1. Open Power BI Desktop and click **Get Data > Text/CSV**. Import `stratified_sample.csv` and `retail_population.csv`.
2. In the **Model** view, ensure keys match (e.g., `store_id`). You can create relationships if you add SKU/lookup tables.
3. Create visuals:
   - **Clustered bar chart / stacked bar:** `Count of store_id` by `stratum` (top N strata). Use as 'Sample composition' visual.
   - **Slicer:** Add slicer for `region` and `format` to filter charts.
   - **Card visuals:** Use `estimation_results.csv` to show `estimated_total_monthly_sales` and `estimated_mean_monthly_sales` as KPI cards.
   - **Histogram / Distribution visual**: Use the `monthly_sales` column for population vs sample. You can use two layered visuals or use the `small multiples` feature to compare.
   - **Table visual**: Show stratum-level `pop_size`, `stratum_sample_size`, and calculated `weight` (create a measure or calculated column: `Weight = stratum_pop / stratum_sample_size`).
4. Create a calculated measure (DAX) for weighted total sales:
   ```dax
   WeightedSales = SUMX('stratified_sample', 'stratified_sample'[monthly_sales] * 'stratified_sample'[weight])
   ```
5. Add tooltips and conditional formatting to flag strata with low sample size (e.g., < 5). Use `IF` logic in Power Query or DAX to create a `QualityFlag` column.

### B) Store Sample Design Optimization — Sample Design Dashboard
**Data files:** `Store_Sample_Design_Optimization/output/selected_sample.csv`, `Store_Sample_Design_Optimization/output/selection_summary.csv`

1. Import `selected_sample.csv` and `selection_summary.csv` into Power BI.
2. Visuals:
   - **Bar chart:** `selected_count` by `cluster` (from `selection_summary.csv`).
   - **Histogram:** overlay `monthly_sales` distribution for population vs selected sample (use two visuals with synchronized slicers or `small multiples`).
   - **Scatter plot:** `monthly_sales` vs `store_id` (or any numeric attribute) colored by `cluster` (Power BI default palette).
   - **Matrix / Table:** Show `cluster`, `size`, `selected_count`, and `avg_sales_selected` to demonstrate representativeness.
3. Add slicers for `format` and `region`. Use bookmarks to create a "Before / After" view (population vs selected).

### C) Retail Index Construction & Monitoring — Index Dashboard
**Data files:** `Retail_Index_Construction_and_Monitoring/output/index_timeseries.csv`, `Retail_Index_Construction_and_Monitoring/data/price_samples.csv`

1. Import `index_timeseries.csv` and `price_samples.csv`.
2. Visuals:
   - **Line chart:** `index_smooth` over `month` (use `index` as a tooltip or secondary line).
   - **Bar chart:** `pct_change` by `month` with a threshold visual (conditional formatting) to highlight `anomaly_flag` months.
   - **Decomposition tree or drill-through:** allow users to drill into SKU-level or store-level price changes.
   - **Card/KPI:** Current index value and 12-month change (create DAX measures to compute YoY %).
3. Add bookmarks and slicers for SKU categories or time windows. Use `anomaly_flag` to drive conditional alerts in the report.
4. Consider publishing to Power BI Service and creating dashboard alerts for `anomaly_flag` months.

## Generating PNGs (matplotlib + plotly example)
The `plots/` scripts provided use `matplotlib` and produce PNGs you can import into Power BI or include in README. If you'd prefer `plotly` interactive HTML exports, the code below shows a minimal example to create and save a PNG (offline):
```python
# plotly example (requires plotly and kaleido)
import pandas as pd
import plotly.express as px
df = pd.read_csv('Retail_Index_Construction_and_Monitoring/output/index_timeseries.csv')
fig = px.line(df, x='month', y='index_smooth', title='Retail Price Index (smoothed)')
fig.write_image('index_plot.png')  # requires 'kaleido' package
```


