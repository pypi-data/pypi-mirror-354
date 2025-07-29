import pandas as pd
import numpy as np
from scipy.stats import pearsonr, ttest_ind, f_oneway, chi2_contingency

def is_categorical(series, threshold=15):
    return series.dtype == 'object' or series.nunique() <= threshold

def auto_bivariate_test(df, col1, col2, plot=True):
    from .viz import plot_bivariate

    print(f"\n🔍 Analyzing: {col1} vs {col2}")
    data = df[[col1, col2]].dropna()
    if data.empty:
        print("⚠️ No data to analyze (empty after dropping NaNs).")
        return

    var1_cat = is_categorical(data[col1])
    var2_cat = is_categorical(data[col2])

    if not var1_cat and not var2_cat:
        x, y = data[col1], data[col2]
        r, p = pearsonr(x, y)
        print(f"📊 Pearson Correlation: r = {r:.3f}, p = {p:.4f}")
        if plot:
            plot_bivariate(data, col1, col2, var1_cat, var2_cat)

    elif var1_cat and not var2_cat:
        categories = data[col1].unique()
        groups = [data[data[col1] == cat][col2] for cat in categories]
        if len(categories) == 2:
            stat, p = ttest_ind(*groups)
            print(f"📊 t-test between {categories[0]} & {categories[1]}: t = {stat:.3f}, p = {p:.4f}")
        elif len(categories) > 2:
            stat, p = f_oneway(*groups)
            print(f"📊 ANOVA across {len(categories)} groups: F = {stat:.3f}, p = {p:.4f}")
        else:
            print("⚠️ Not enough categories to compare.")
        if plot:
            plot_bivariate(data, col1, col2, var1_cat, var2_cat)

    elif not var1_cat and var2_cat:
        return auto_bivariate_test(df, col2, col1, plot=plot)

    elif var1_cat and var2_cat:
        contingency = pd.crosstab(data[col1], data[col2])
        if contingency.shape[0] < 2 or contingency.shape[1] < 2:
            print("⚠️ Not enough categories for Chi-Squared test.")
            return
        chi2, p, dof, expected = chi2_contingency(contingency)
        print(f"📊 Chi-Squared Test: χ² = {chi2:.2f}, p = {p:.4f}")
        if plot:
            plot_bivariate(data, col1, col2, var1_cat, var2_cat)

    else:
        print("⚠️ Unrecognized variable types.")

