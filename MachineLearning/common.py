"""Shared data loading and evaluation helpers for the mesh ML models."""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import GroupKFold

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "csvFiles"
MODEL_DIR = ROOT / "Model"

# Geometric features extracted from the STEP file with pythonocc
GEOMETRY_FEATURES = ["Hacim", "YuzeyAlani", "Karmasiklik", "MinCap", "MaxCap", "KisaEdge", "UzunEdge"]

# Ansys Mechanical global mesh settings varied in the parameter sweep
MESH_SETTINGS = [
    "MeshElementSize",
    "MeshGrowRate",
    "meshDefeatureTolerance",
    "MeshMinSize",
    "meshProximityMinimumSize",
    "meshCurvatureNormalAngle",
]

# Mesh quality metrics reported by Ansys (element quality mean / std)
QUALITY_METRICS = ["MeshAverage", "MeshStandardDeviation"]


def load_csv(name: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / name)
    return df.replace([np.inf, -np.inf], np.nan).fillna(0)


def augment_with_noise(X: pd.DataFrame, y: pd.DataFrame, rel_noise: float = 0.01, seed: int = 0):
    """Duplicate rows with small multiplicative noise.

    Must only be applied to the TRAINING split. Augmenting before the split
    puts near-copies of training rows into the test set and inflates scores.
    """
    rng = np.random.default_rng(seed)
    X_noisy = X * (1.0 + rel_noise * rng.standard_normal(X.shape))
    return pd.concat([X, X_noisy], axis=0), pd.concat([y, y], axis=0)


def grouped_cv(make_model, X, y, groups, n_splits=5, augment=False):
    """Cross-validate with folds split by part, so no part appears in both train and test.

    Returns per-target R2 and MAE (mean over folds) and a mean-predictor baseline MAE.
    """
    r2, mae, base = [], [], []
    for tr, te in GroupKFold(n_splits).split(X, y, groups):
        X_tr, y_tr = X.iloc[tr], y.iloc[tr]
        if augment:
            X_tr, y_tr = augment_with_noise(X_tr, y_tr)
        model = make_model().fit(X_tr, y_tr)
        pred = model.predict(X.iloc[te])
        y_te = y.iloc[te].to_numpy()
        r2.append(r2_score(y_te, pred, multioutput="raw_values"))
        mae.append(mean_absolute_error(y_te, pred, multioutput="raw_values"))
        base.append(mean_absolute_error(y_te, np.tile(y_tr.mean().to_numpy(), (len(te), 1)), multioutput="raw_values"))
    return (
        pd.DataFrame(
            {"R2": np.mean(r2, 0), "R2_std": np.std(r2, 0), "MAE": np.mean(mae, 0), "MAE_baseline": np.mean(base, 0)},
            index=y.columns,
        )
    )
