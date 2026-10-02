"""
========================================================================================
⚡ STREAMLIT CLOUD OPTIMIZED MACHINE LEARNING ENGINE (LIGHTGBM + XGBOOST + CATBOOST)
========================================================================================
Engineered for fast, memory-safe execution on 200,000+ row tabular datasets.
Includes memory downcasting, automated preprocessing, CV/train-val splits, and ensembling.
========================================================================================
"""

import gc
import io
import time
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional

from sklearn.model_selection import StratifiedKFold, KFold, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    roc_auc_score,
    log_loss,
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)

import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier, CatBoostRegressor


# ======================================================================================
# 1. MEMORY OPTIMIZATION (CRITICAL FOR STREAMLIT CLOUD's ~1GB-2GB RAM CEILING)
# ======================================================================================
def reduce_mem_usage(df: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    """
    Downcasts numeric columns from 64-bit to 32/16-bit to prevent Streamlit Cloud OOM.
    """
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtype
        if col_type != object and not pd.api.types.is_categorical_dtype(df[col]):
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == "int":
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            if df[col].nunique() / max(len(df[col]), 1) < 0.5:
                df[col] = df[col].astype("category")

    end_mem = df.memory_usage().sum() / 1024**2
    if verbose:
        print(f"Memory reduced: {start_mem:.2f} MB -> {end_mem:.2f} MB")
    return df


# ======================================================================================
# 2. SYNTHETIC BENCHMARK DATASET GENERATOR
# ======================================================================================
def generate_demo_dataset(n_rows: int = 50_000, problem_type: str = "classification") -> pd.DataFrame:
    """Creates a sample benchmark dataset with mixed dtypes and realistic signals."""
    np.random.seed(42)
    age = np.random.randint(18, 70, size=n_rows).astype(float)
    income = np.random.normal(55000, 20000, size=n_rows)
    credit_score = np.random.randint(300, 850, size=n_rows).astype(float)
    txn_count = np.random.poisson(lam=15, size=n_rows).astype(float)
    
    # Introduce missing values in 2% of rows
    income[np.random.rand(n_rows) < 0.02] = np.nan
    credit_score[np.random.rand(n_rows) < 0.02] = np.nan

    education = np.random.choice(["High School", "Bachelor", "Master", "PhD"], size=n_rows, p=[0.3, 0.4, 0.2, 0.1])
    city_tier = np.random.choice(["Tier 1", "Tier 2", "Tier 3"], size=n_rows)
    occupation = np.random.choice(["Tech", "Healthcare", "Finance", "Education", "Retail"], size=n_rows)

    signal = (
        0.00003 * np.nan_to_num(income, nan=50000)
        + 0.004 * np.nan_to_num(credit_score, nan=650)
        + 0.03 * txn_count
        - 0.02 * age
        + (education == "Master").astype(float) * 0.5
        + np.random.normal(0, 0.5, size=n_rows)
    )

    if problem_type == "classification":
        prob = 1.0 / (1.0 + np.exp(-signal + np.median(signal)))
        target = (np.random.rand(n_rows) < prob).astype(int)
    else:
        target = np.round(signal * 1000 + 20000, 2)

    df = pd.DataFrame({
        "customer_id": np.arange(10001, 10001 + n_rows),
        "age": age,
        "income": income,
        "credit_score": credit_score,
        "txn_count": txn_count,
        "education": education,
        "city_tier": city_tier,
        "occupation": occupation,
        "target": target
    })
    return reduce_mem_usage(df)


# ======================================================================================
# 3. PREPROCESSING PIPELINE
# ======================================================================================
class WebDataPreprocessor:
    def __init__(self, numeric_cols: List[str], categorical_cols: List[str]):
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols
        self.numeric_imputes: Dict[str, float] = {}
        self.label_encoders: Dict[str, LabelEncoder] = {}
        self.category_mappings: Dict[str, Dict[str, int]] = {}

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        for col in self.numeric_cols:
            median_val = df[col].median()
            self.numeric_imputes[col] = float(median_val) if not pd.isna(median_val) else 0.0
            df[col] = df[col].fillna(self.numeric_imputes[col])

        for col in self.categorical_cols:
            df[col] = df[col].astype(str).fillna("MISSING")
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            self.label_encoders[col] = le
            # Store known classes
            self.category_mappings[col] = {val: idx for idx, val in enumerate(le.classes_)}

        return df

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        for col in self.numeric_cols:
            if col in df.columns:
                fill_val = self.numeric_imputes.get(col, 0.0)
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(fill_val)

        for col in self.categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).fillna("MISSING")
                mapping = self.category_mappings.get(col, {})
                # Map unseen categories to -1
                df[col] = df[col].map(lambda x: mapping.get(x, -1))

        return df


# ======================================================================================
# 4. MODEL TRAINING & CROSS-VALIDATION
# ======================================================================================
def train_model(
    df: pd.DataFrame,
    target_col: str,
    feature_cols: List[str],
    problem_type: str = "classification",
    model_name: str = "lightgbm",
    cv_folds: int = 5,
    sample_size: Optional[int] = None,
    progress_callback = None
) -> Tuple[Dict[str, Any], Dict[str, float], pd.DataFrame]:
    """
    Executes training and cross-validation across chosen GBDT algorithm or Ensemble.
    Returns: (pipeline_dict, metrics_dict, feature_importance_df)
    """
    # Optional sub-sampling for fast interactive experiments
    train_data = df.copy()
    if sample_size and len(train_data) > sample_size:
        train_data = train_data.sample(sample_size, random_state=42).reset_index(drop=True)

    y_raw = train_data[target_col].values
    X_raw = train_data[feature_cols].copy()

    # Determine numeric and categorical column sets
    numeric_cols = [c for c in feature_cols if pd.api.types.is_numeric_dtype(X_raw[c])]
    categorical_cols = [c for c in feature_cols if c not in numeric_cols]

    # Preprocess features
    preprocessor = WebDataPreprocessor(numeric_cols, categorical_cols)
    X = preprocessor.fit_transform(X_raw)

    # Encode target if classification with string labels
    target_encoder = None
    if problem_type == "classification":
        if not np.issubdtype(y_raw.dtype, np.number) or len(np.unique(y_raw)) > 2:
            target_encoder = LabelEncoder()
            y = target_encoder.fit_transform(y_raw.astype(str))
        else:
            y = y_raw.astype(int)
    else:
        y = y_raw.astype(float)

    n_samples = len(X)
    n_splits = max(2, min(cv_folds, 10))

    if problem_type == "classification":
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    else:
        cv = KFold(n_splits=n_splits, shuffle=True, random_state=42)

    trained_models = []
    oof_predictions = np.zeros(n_samples, dtype=np.float32)
    all_importances = []

    models_list = ["lightgbm", "xgboost", "catboost"] if model_name == "ensemble" else [model_name]
    total_steps = n_splits * len(models_list)
    current_step = 0

    ensemble_oof = np.zeros(n_samples, dtype=np.float32)

    for m_type in models_list:
        sub_oof = np.zeros(n_samples, dtype=np.float32)

        for fold, (train_idx, val_idx) in enumerate(cv.split(X, y), 1):
            X_tr, y_tr = X.iloc[train_idx], y[train_idx]
            X_va, y_va = X.iloc[val_idx], y[val_idx]

            # Model Instantiation
            if m_type == "lightgbm":
                if problem_type == "classification":
                    m = lgb.LGBMClassifier(n_estimators=300, learning_rate=0.05, num_leaves=31, random_state=42, n_jobs=-1, verbose=-1)
                else:
                    m = lgb.LGBMRegressor(n_estimators=300, learning_rate=0.05, num_leaves=31, random_state=42, n_jobs=-1, verbose=-1)
                m.fit(X_tr, y_tr)
                fi = m.feature_importances_

            elif m_type == "xgboost":
                if problem_type == "classification":
                    m = xgb.XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=5, tree_method="hist", random_state=42, n_jobs=-1)
                else:
                    m = xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, tree_method="hist", random_state=42, n_jobs=-1)
                m.fit(X_tr, y_tr)
                fi = m.feature_importances_

            elif m_type == "catboost":
                if problem_type == "classification":
                    m = CatBoostClassifier(iterations=300, learning_rate=0.05, depth=5, verbose=0, random_seed=42)
                else:
                    m = CatBoostRegressor(iterations=300, learning_rate=0.05, depth=5, verbose=0, random_seed=42)
                m.fit(X_tr, y_tr)
                fi = m.get_feature_importance()

            # Predict on fold
            if problem_type == "classification":
                val_pred = m.predict_proba(X_va)[:, 1] if hasattr(m, "predict_proba") else m.predict(X_va)
            else:
                val_pred = m.predict(X_va)

            sub_oof[val_idx] = val_pred
            trained_models.append((m_type, m))
            all_importances.append(fi)

            current_step += 1
            if progress_callback:
                progress_callback(current_step / total_steps, f"Trained {m_type.upper()} Fold {fold}/{n_splits}")

        ensemble_oof += sub_oof / len(models_list)

    oof_predictions = ensemble_oof

    # Calculate Evaluation Metrics
    metrics = {}
    if problem_type == "classification":
        pred_labels = (oof_predictions >= 0.5).astype(int)
        metrics["Accuracy"] = float(accuracy_score(y, pred_labels))
        metrics["F1-Score"] = float(f1_score(y, pred_labels, average="binary" if len(np.unique(y)) <= 2 else "macro"))
        try:
            metrics["ROC-AUC"] = float(roc_auc_score(y, oof_predictions))
        except Exception:
            metrics["ROC-AUC"] = 0.0
        try:
            metrics["Log Loss"] = float(log_loss(y, oof_predictions))
        except Exception:
            metrics["Log Loss"] = 0.0
    else:
        metrics["RMSE"] = float(mean_squared_error(y, oof_predictions, squared=False))
        metrics["MAE"] = float(mean_absolute_error(y, oof_predictions))
        metrics["R2-Score"] = float(r2_score(y, oof_predictions))

    # Feature Importance aggregation
    if len(all_importances) > 0:
        mean_fi = np.mean(all_importances, axis=0)
        # Normalize to percentage
        if np.sum(mean_fi) > 0:
            mean_fi = 100.0 * (mean_fi / np.sum(mean_fi))
        fi_df = pd.DataFrame({
            "Feature": feature_cols,
            "Importance (%)": np.round(mean_fi, 2)
        }).sort_values(by="Importance (%)", ascending=False).reset_index(drop=True)
    else:
        fi_df = pd.DataFrame({"Feature": feature_cols, "Importance (%)": [1.0] * len(feature_cols)})

    # Package pipeline artifact
    pipeline_artifact = {
        "models": trained_models,
        "model_name": model_name,
        "problem_type": problem_type,
        "feature_cols": feature_cols,
        "target_col": target_col,
        "preprocessor": preprocessor,
        "target_encoder": target_encoder,
        "metrics": metrics
    }

    return pipeline_artifact, metrics, fi_df


# ======================================================================================
# 5. INFERENCE / PREDICTION ENGINE
# ======================================================================================
def predict_batch(pipeline_artifact: Dict[str, Any], input_df: pd.DataFrame) -> np.ndarray:
    """Predicts target on new unseen batch data using the ensemble of trained fold models."""
    feature_cols = pipeline_artifact["feature_cols"]
    preprocessor = pipeline_artifact["preprocessor"]
    trained_models = pipeline_artifact["models"]
    problem_type = pipeline_artifact["problem_type"]
    target_encoder = pipeline_artifact.get("target_encoder")

    # Ensure all required features are present
    missing_cols = [c for c in feature_cols if c not in input_df.columns]
    if missing_cols:
        raise ValueError(f"Input data is missing expected feature columns: {missing_cols}")

    X_sub = input_df[feature_cols].copy()
    X_proc = preprocessor.transform(X_sub)

    # Accumulate predictions across all models and folds
    preds = np.zeros(len(input_df), dtype=np.float32)
    for _, model in trained_models:
        if problem_type == "classification":
            fold_pred = model.predict_proba(X_proc)[:, 1] if hasattr(model, "predict_proba") else model.predict(X_proc)
        else:
            fold_pred = model.predict(X_proc)
        preds += fold_pred / len(trained_models)

    return preds
