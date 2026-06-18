import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("../data/ml_dataset.csv")

# Select features
features = df[
    [
        "ORTG_DIFF",
        "DRTG_DIFF",
        "PACE_DIFF",
        "WON"
    ]
]

# Correlation heatmap
plt.figure(figsize=(8, 6))

sns.heatmap(
    features.corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Feature Correlation Heatmap")

plt.show()