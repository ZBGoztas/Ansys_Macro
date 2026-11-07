"""Reproduce the evaluation-leakage finding reported in the README.

The original thesis script duplicated rows with noise BEFORE the train/test split,
so near-copies of training rows ended up in the test set. This script scores the
same XGBoost settings model both ways.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor

from common import GEOMETRY_FEATURES, MESH_SETTINGS, QUALITY_METRICS, grouped_cv, load_csv

df = load_csv("MachineLearning.csv")
X = df[GEOMETRY_FEATURES]
y = df[MESH_SETTINGS + QUALITY_METRICS]


def make_model():
    return MultiOutputRegressor(
        XGBRegressor(objective="reg:squarederror", n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
    )


# 1) Original protocol: augment (absolute noise 0.01), then split
X_aug = X + 0.01 * np.random.default_rng(0).standard_normal(X.shape)
X_c = pd.concat([X, pd.DataFrame(X_aug, columns=X.columns)])
y_c = pd.concat([y, y])
X_tr, X_te, y_tr, y_te = train_test_split(X_c, y_c, test_size=0.2, random_state=42)
leaky = r2_score(y_te, make_model().fit(X_tr, y_tr).predict(X_te), multioutput="raw_values")

# 2) Corrected protocol: split by part first, augment training folds only
honest = grouped_cv(make_model, X, y, df["Dizin"], augment=True)["R2"].to_numpy()

table = pd.DataFrame({"R2 (augment, then split)": leaky, "R2 (split, then augment)": honest}, index=y.columns)
print(table.round(2))
print("Mean:", table.mean().round(2).to_dict())
