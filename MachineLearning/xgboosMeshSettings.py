"""Train the model that predicts Ansys mesh settings from part geometry.

Input:  csvFiles/MachineLearning.csv  (one row per part: geometry + best settings from the sweep)
Output: Model/MeshSettings.pkl
"""
import joblib
import numpy as np
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor

from common import GEOMETRY_FEATURES, MESH_SETTINGS, MODEL_DIR, QUALITY_METRICS, augment_with_noise, grouped_cv, load_csv

df = load_csv("MachineLearning.csv")
X = df[GEOMETRY_FEATURES]
y = df[MESH_SETTINGS + QUALITY_METRICS]
groups = df["Dizin"]  # one row per part here, so this is plain K-fold


def make_model():
    return MultiOutputRegressor(
        XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
    )


# Honest evaluation: split first, augment the training folds only
report = grouped_cv(make_model, X, y, groups, augment=True)
print("5-fold CV (split by part, augmentation on train folds only):")
print(report.round(3))
print("Mean R2:", round(report["R2"].mean(), 3))

# Final model on all data
X_all, y_all = augment_with_noise(X, y)
model = make_model().fit(X_all, y_all)
MODEL_DIR.mkdir(exist_ok=True)
joblib.dump(model, MODEL_DIR / "MeshSettings.pkl")
print("Saved", MODEL_DIR / "MeshSettings.pkl")
