"""Train the model that forecasts mesh quality from geometry + mesh settings.

Input:  csvFiles/lastDataSet.csv  (the full parameter sweep: ~20k meshing runs over ~300 parts)
Output: Model/MeshQuality.pkl

Earlier versions trained on the 317 best-setting rows only. The full sweep gives
the model every setting combination tried on each part, and folds are split by
part so the score reflects performance on parts the model has never seen.
"""
import joblib
import numpy as np
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor

from common import GEOMETRY_FEATURES, MESH_SETTINGS, MODEL_DIR, QUALITY_METRICS, grouped_cv, load_csv

df = load_csv("lastDataSet.csv")
df = df[df["MeshAverage"] > 0]  # drop failed meshing runs
X = df[GEOMETRY_FEATURES + MESH_SETTINGS]
y = df[QUALITY_METRICS]
groups = df["Dizin"]


def make_model():
    return MultiOutputRegressor(
        XGBRegressor(
            objective="reg:squarederror",
            n_estimators=400,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
        )
    )


print(f"{len(df)} meshing runs over {groups.nunique()} parts")
report = grouped_cv(make_model, X, y, groups)
print("5-fold CV, split by part (unseen parts):")
print(report.round(4))

model = make_model().fit(X, y)
MODEL_DIR.mkdir(exist_ok=True)
joblib.dump(model, MODEL_DIR / "MeshQuality.pkl")
print("Saved", MODEL_DIR / "MeshQuality.pkl")
