# Gerekli kütüphaneleri yükle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
import joblib
import matplotlib.pyplot as plt

# Veri setini yükle
df = pd.read_csv("<local-path>")

# Gereksiz sütunları kaldır ve eksik/sonsuz değerleri düzelt
df.drop(columns=['Dizin'], inplace=True)
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(0, inplace=True)

# Giriş (X) ve çıkış (y) değişkenlerini ayır
X = df[[
        "Hacim",
        "YuzeyAlani",
        "Karmasiklik", 
        "MinCap", 
        "MaxCap", 
        "KisaEdge", 
        "UzunEdge",
        "MeshElementSize",
        "MeshGrowRate",
        "meshDefeatureTolerance",
        "MeshMinSize",
        "meshProximityMinimumSize",
        "meshCurvatureNormalAngle",]]
y = df[[
    "MeshAverage",
    "MeshStandardDeviation"
]]

# Gürültü ekleyerek veri arttırma
noise_level = 0.01
X_augmented = X + noise_level * np.random.normal(size=X.shape)

# Yeni veri setini birleştir
X_combined = pd.concat([X, pd.DataFrame(X_augmented, columns=X.columns)], axis=0)
y_combined = pd.concat([y, y], axis=0)

# Veriyi normalleştirme

# Veriyi eğitim ve test setlerine böl
X_train, X_test, y_train, y_test = train_test_split(
    X_combined, 
    y_combined, 
    test_size=0.2, 
    random_state=42
)

# XGBoost modeli
xgb_model = MultiOutputRegressor(
    XGBRegressor(
        objective="reg:squarederror",
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        random_state=42
    )
)

# Modeli eğit
xgb_model.fit(X_train, y_train)

# Tahmin yap
y_pred = xgb_model.predict(X_test)

# Performans metriklerini hesapla
mse = mean_squared_error(y_test, y_pred, multioutput='uniform_average')
r2 = r2_score(y_test, y_pred, multioutput='uniform_average')
print("XGBoost (MultiOutputRegressor) Sonuçları:")
print("MSE (ortalama):", mse)
print("R2 (ortalama):", r2)

# Her bir hedef için ayrı R2 skorları
r2_individual = r2_score(y_test, y_pred, multioutput='raw_values')
print("\nHer bir hedef için R2 skorları:", r2_individual)

# Hiperparametre optimizasyonu
param_dist = {
    'estimator__n_estimators': [50, 100, 200],
    'estimator__max_depth': [3, 6, 9],
    'estimator__learning_rate': [0.01, 0.1, 0.2],
}

scoring_metrics = {
    'r2': 'r2',
    'mse': 'neg_mean_squared_error'
}

random_search = RandomizedSearchCV(
    estimator=xgb_model,
    param_distributions=param_dist,
    cv=3,
    scoring=scoring_metrics,
    refit='r2',
    n_iter=5,
    random_state=42
)

random_search.fit(X_train, y_train)

# En iyi parametreler ve skorlar
print("En iyi parametreler:", random_search.best_params_)
print("En iyi R2 skoru:", random_search.best_score_)

# Sonuçları bir DataFrame olarak kaydet
results = pd.DataFrame(random_search.cv_results_)
results["true_mse"] = -results["mean_test_mse"]
print(results[[
    'param_estimator__n_estimators',
    'param_estimator__max_depth',
    'param_estimator__learning_rate',
    'mean_test_r2',
    'true_mse'
]])

# En iyi modeli kaydet
joblib.dump(random_search.best_estimator_, "MeshkaliteTahmini.pkl")
