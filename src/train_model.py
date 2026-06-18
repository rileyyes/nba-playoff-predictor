import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)

import joblib

# Load dataset
df = pd.read_csv("../data/ml_dataset.csv")

# Features
X = df[
    [
        "ORTG_DIFF",
        "DRTG_DIFF",
        "PACE_DIFF"
    ]
]

# Target
y = df["WON"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create model
model = LogisticRegression()

# Train model
model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy:.2f}")

# Confusion matrix
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))

# Classification report
print("\nClassification Report:")
print(classification_report(y_test, predictions))

# Feature importance
feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": model.coef_[0]
})

print("\nFeature Importance:")
print(feature_importance)

# Save model
joblib.dump(model, "../models/logistic_regression_model.pkl")

print("\nModel saved successfully!")