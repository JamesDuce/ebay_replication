# did_analysis.py
# Computes the difference-in-differences estimate for the eBay paid search experiment.
# Method: Compare pre-post log revenue changes between treatment and control DMAs.
# Estimates the average treatment effect of turning off eBay's paid search.
# Uses preprocessed pivot tables from preprocess.py.
# Output: LaTeX table in output/tables/did_table.tex
# Reference: Blake et al. (2014), Taddy Ch. 5
import pandas as pd
import numpy as np
import os

# Ensure output directory exists
os.makedirs("output/tables", exist_ok=True)

# Load pivot tables
treated_pivot = pd.read_csv('temp/treated_pivot.csv', index_col='dma')
untreated_pivot = pd.read_csv('temp/untreated_pivot.csv', index_col='dma')

# Extract log revenue differences
treated_diffs = treated_pivot['log_revenue_diff']
untreated_diffs = untreated_pivot['log_revenue_diff']

# Means
r1_bar = treated_diffs.mean()
r0_bar = untreated_diffs.mean()

# DID estimate
gamma_hat = r1_bar - r0_bar

# Sample sizes
n1 = len(treated_diffs)
n0 = len(untreated_diffs)

# Variances (sample variance, Bessel corrected)
var1 = treated_diffs.var()
var0 = untreated_diffs.var()

# Standard Error
se = np.sqrt(var1 / n1 + var0 / n0)

# 95% CI
ci_lower = gamma_hat - 1.96 * se
ci_upper = gamma_hat + 1.96 * se

# Print results
print("DID Results (Log Scale)")
print("=======================")
print(f"Gamma hat: {gamma_hat:.4f}")
print(f"Std Error: {se:.4f}")
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

# Create LaTeX table
latex = r"""\begin{table}[h]
\centering
\caption{Difference-in-Differences Estimate of the Effect of Paid Search on Revenue}
\begin{tabular}{lc}
\hline
& Log Scale \\
\hline
Point Estimate ($\hat{\gamma}$) & $%.4f$ \\
Standard Error & $%.4f$ \\
95\%% CI & $[%.4f, \; %.4f]$ \\
\hline
\end{tabular}
\label{tab:did}
\end{table}""" % (gamma_hat, se, ci_lower, ci_upper)

with open('output/tables/did_table.tex', 'w') as f:
    f.write(latex)
