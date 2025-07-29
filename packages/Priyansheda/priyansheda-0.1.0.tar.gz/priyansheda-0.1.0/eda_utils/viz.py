
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_bivariate(data, col1, col2, col1_cat, col2_cat):
    plt.figure(figsize=(8, 5))
    if not col1_cat and not col2_cat:
        sns.scatterplot(x=col1, y=col2, data=data)
    elif col1_cat and not col2_cat:
        sns.boxplot(x=col1, y=col2, data=data)
    elif col1_cat and col2_cat:
        contingency = pd.crosstab(data[col1], data[col2])
        sns.heatmap(contingency, annot=True, fmt='d', cmap='Blues')
    else:
        sns.boxplot(x=col2, y=col1, data=data)
    plt.title(f"{col1} vs {col2}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()