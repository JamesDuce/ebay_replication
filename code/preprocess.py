import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------
# Step 1: Load Data
# -------------------

df = pd.read_csv('input/PaidSearch.csv')
df['date'] = pd.to_datetime(df['date'])
df['log_revenue'] = np.log(df['revenue'])

# -------------------
# Step 2: Pivot Tables
# -------------------

# Treated group (search turned off)
treated = df[df['search_stays_on'] == 0]

treated_pivot = treated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

treated_pivot.columns = ['log_revenue_pre', 'log_revenue_post']
treated_pivot['log_revenue_diff'] = (
    treated_pivot['log_revenue_post'] -
    treated_pivot['log_revenue_pre']
)

treated_pivot.to_csv('temp/treated_pivot.csv')

# Control group (search stays on)
untreated = df[df['search_stays_on'] == 1]

untreated_pivot = untreated.pivot_table(
    index='dma',
    columns='treatment_period',
    values='log_revenue',
    aggfunc='mean'
)

untreated_pivot.columns = ['log_revenue_pre', 'log_revenue_post']
untreated_pivot['log_revenue_diff'] = (
    untreated_pivot['log_revenue_post'] -
    untreated_pivot['log_revenue_pre']
)

untreated_pivot.to_csv('temp/untreated_pivot.csv')

# -------------------
# Step 3: Summary Stats
# -------------------

print("Treated DMAs:", treated['dma'].nunique())
print("Untreated DMAs:", untreated['dma'].nunique())
print("Date range:", df['date'].min().date(), "to", df['date'].max().date())

# -------------------
# Step 4: Figure 5.2
# -------------------

daily_avg = df.groupby(['date', 'search_stays_on'])['revenue'].mean().reset_index()

control = daily_avg[daily_avg['search_stays_on'] == 1]
treatment = daily_avg[daily_avg['search_stays_on'] == 0]

plt.figure()
plt.plot(control['date'], control['revenue'], label='Control (search stays on)')
plt.plot(treatment['date'], treatment['revenue'], label='Treatment (search goes off)')

plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Figure 5.2: Average Revenue Over Time')
plt.legend()

plt.savefig('output/figures/figure_5_2.png')
plt.close()

# -------------------
# Step 5: Figure 5.3
# -------------------

daily_log = df.groupby(['date', 'search_stays_on'])['log_revenue'].mean().reset_index()

pivot = daily_log.pivot(index='date', columns='search_stays_on', values='log_revenue')

log_diff = pivot[1] - pivot[0]

plt.figure()
plt.plot(log_diff.index, log_diff.values)

plt.axvline(pd.to_datetime('2012-05-22'), linestyle='--')
plt.xlabel('Date')
plt.ylabel('log(rev_control) - log(rev_treat)')
plt.title('Figure 5.3: Log Revenue Difference Over Time')

plt.savefig('output/figures/figure_5_3.png')
plt.close()
