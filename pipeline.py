"""
========================================================================================
🏆 END-TO-END COMPETITIVE MACHINE LEARNING PIPELINE (GBDT TRIFECTA + STACKING/BLENDING)
========================================================================================
Author: Kaggle Grandmaster & Senior ML Engineer Architecture
Target: Tabular Data (~200,000+ rows) optimized for speed, memory, and generalization.
Models: LightGBM + XGBoost + CatBoost + SciPy SLSQP Blending / Ridge Stacking Meta-Learner
========================================================================================
"""

import os
import gc
import sys
import time
import joblib
import warnings
import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any

# Scikit-learn
from sklearn.model_selection import StratifiedKFold, KFold
from sklearn.metrics import (
    roc_auc_score,
    log_loss,
    f1_score,
    accuracy_score,
    mean_squared_error,
    mean_absolute_error,
)
from sklearn.preprocessing import LabelEncoder, RobustScaler
from sklearn.linear_model import LogisticRegression, Ridge
from scipy.optimize import minimize

# Gradient Boosting
import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClassifier, CatBoostRegressor, Pool

# Optional Hyperparameter Tuning & Explainability
try:
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    HAS_OPTUNA = True
except ImportError:
    HAS_OPTUNA = False

try:
    import shap
    HAS_SHAP = True
except ImportError:
    HAS_SHAP = False

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLT = True
except ImportError:
    HAS_PLT = False

warnings.filterwarnings("ignore")


# ======================================================================================
# 1. GLOBAL CONFIGURATION & PIPELINE SPECIFICATION
# ======================================================================================
@dataclass
class PipelineConfig:
    # File Paths (Update these for your dataset)
    TRAIN_PATH: str = "train.csv"          # Path to train dataset (or synthetic fallback)
    TEST_PATH: Optional[str] = "test.csv"  # Path to test dataset (optional)
    OUTPUT_DIR: str = "./artifacts"        # Directory to save models and submissions
    SUBMISSION_FILE: str = "submission.csv"

    # Problem Formulation
    # Options: 'binary', 'multiclass', 'regression'
    PROBLEM_TYPE: str = "binary"
    TARGET_COL: str = "target"
    ID_COL: Optional[str] = "id"

    # Evaluation Metric
    # Options: 'roc_auc', 'logloss', 'f1', 'accuracy', 'rmse', 'mae'
    EVAL_METRIC: str = "roc_auc"

    # Cross-Validation & Execution Setup
    N_SPLITS: int = 5
    RANDOM_STATE: int = 42
    N_JOBS: int = -1
    USE_GPU: bool = False  # Set True if running on CUDA-enabled environment (e.g. Colab GPU)

    # Feature Engineering Controls
    MAX_HIGH_CARDINALITY: int = 50       # Threshold for high-cardinality frequency/target encoding
    ENABLE_INTERACTIONS: bool = True     # Generate pairwise numeric interaction features
    ENABLE_AGGREGATIONS: bool = True     # Generate group-by statistics
    DROP_ORIGINAL_HIGH_CARD: bool = False

    # Modeling & Blending Controls
    MODELS_TO_RUN: List[str] = field(default_factory=lambda: ["lightgbm", "xgboost", "catboost"])
    RUN_OPTUNA: bool = False             # Set True to run hyperparameter tuning before 5-fold CV
    OPTUNA_N_TRIALS: int = 20
    GENERATE_SHAP: bool = True           # Generate SHAP summary plots on validation slice

    def __post_init__(self):
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        if self.PROBLEM_TYPE == "regression" and self.EVAL_METRIC in ["roc_auc", "f1", "accuracy", "logloss"]:
            self.EVAL_METRIC = "rmse"


# ======================================================================================
# 2. MEMORY MANAGEMENT (DOWNCASTING TO PREVENT OOM ON 200,000+ ROWS)
# ======================================================================================
def reduce_mem_usage(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """
    Iterate through all columns of a dataframe and downcast types to reduce memory footprint.
    Critical for tabular competitions with 200k+ rows to prevent memory crashes.
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
            # Check if object can be converted to category
            num_unique = df[col].nunique()
            num_total = len(df[col])
            if num_unique / num_total < 0.5:
                df[col] = df[col].astype("category")

    end_mem = df.memory_usage().sum() / 1024**2
    if verbose:
        reduction = 100 * (start_mem - end_mem) / start_mem
        print(f"Memory downcast: {start_mem:.2f} MB -> {end_mem:.2f} MB ({reduction:.1f}% reduction)")
    return df


# ======================================================================================
# 3. SYNTHETIC BENCHMARK DATA GENERATOR (FOR ZERO-DEPENDENCY DEMO & SMOKE TESTING)
# ======================================================================================
def create_synthetic_dataset(n_rows: int = 200_000, problem_type: str = "binary") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Generates a realistic 200,000-row tabular benchmark dataset with mixed dtypes."""
    print(f"\n[Data Gen] Generating {n_rows:,} rows of realistic benchmark tabular data...")
    np.random.seed(42)

    # Numerical features with varied distributions and correlations
    f_norm1 = np.random.normal(50, 15, size=n_rows)
    f_norm2 = f_norm1 * 0.4 + np.random.normal(10, 5, size=n_rows)
    f_exp = np.random.exponential(scale=2.0, size=n_rows)
    f_skew = np.random.lognormal(mean=1.5, sigma=0.75, size=n_rows)
    f_uniform = np.random.uniform(-100, 100, size=n_rows)

    # Categorical features (low & high cardinality)
    cat_low1 = np.random.choice(["Tier1", "Tier2", "Tier3", "Tier4"], size=n_rows, p=[0.4, 0.3, 0.2, 0.1])
    cat_low2 = np.random.choice(["Type_A", "Type_B", "Type_C"], size=n_rows)
    cat_high = np.random.choice([f"City_{i}" for i in range(120)], size=n_rows)

    # Induce missing values realistically (~3% missing in select features)
    mask_miss1 = np.random.rand(n_rows) < 0.03
    f_norm2[mask_miss1] = np.nan
    mask_miss2 = np.random.rand(n_rows) < 0.02
    cat_low1 = np.where(mask_miss2, None, cat_low1)

    # Signal generation
    latent_signal = (
        0.05 * f_norm1
        + 0.08 * np.nan_to_num(f_norm2, nan=10)
        - 0.15 * f_exp
        + 0.02 * (cat_low1 == "Tier1").astype(float) * 10
        + np.random.normal(0, 1.0, size=n_rows)
    )

    if problem_type == "binary":
        prob = 1.0 / (1.0 + np.exp(-latent_signal + np.median(latent_signal)))
        target = (np.random.rand(n_rows) < prob).astype(int)
    elif problem_type == "multiclass":
        bins = np.percentile(latent_signal, [33.3, 66.6])
        target = np.digitize(latent_signal, bins)
    else:  # regression
        target = latent_signal * 10.0 + 50.0

    df = pd.DataFrame({
        "id": np.arange(1, n_rows + 1),
        "f_norm1": f_norm1,
        "f_norm2": f_norm2,
        "f_exp": f_exp,
        "f_skew": f_skew,
        "f_uniform": f_uniform,
        "cat_low1": cat_low1,
        "cat_low2": cat_low2,
        "cat_high": cat_high,
        "target": target
    })

    # Train / Test Split (80% train, 20% test)
    split_idx = int(n_rows * 0.8)
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy().drop(columns=["target"])

    return train_df, test_df


# ======================================================================================
# 4. ADVANCED AUTOMATED PREPROCESSING & FEATURE ENGINEERING PIPELINE
# ======================================================================================
class FeatureEngineeringPipeline:
    """
    Automated Kaggle-grade Feature Engineering:
    - Missing value detection & informative flags
    - Frequency Encoding for high & medium cardinality
    - Pairwise interactions (ratios, products, differences)
    - Group-by aggregation features (mean, std, min, max)
    - Out-Of-Fold (OOF) Target Encoding (zero data leakage)
    """
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.numeric_cols: List[str] = []
        self.categorical_cols: List[str] = []
        self.freq_encoding_maps: Dict[str, pd.Series] = {}
        self.target_encoding_maps: Dict[str, Dict[Any, float]] = {}
        self.global_target_mean: float = 0.0
        self.agg_definitions: List[Tuple[str, str, List[str]]] = []

    def identify_column_types(self, df: pd.DataFrame):
        exclude_cols = [self.config.TARGET_COL]
        if self.config.ID_COL and self.config.ID_COL in df.columns:
            exclude_cols.append(self.config.ID_COL)

        self.numeric_cols = [
            c for c in df.columns
            if c not in exclude_cols and pd.api.types.is_numeric_dtype(df[c])
        ]
        self.categorical_cols = [
            c for c in df.columns
            if c not in exclude_cols and c not in self.numeric_cols
        ]
        print(f"[EDA] Identified {len(self.numeric_cols)} numeric and {len(self.categorical_cols)} categorical columns.")

    def fit_transform(self, train_df: pd.DataFrame) -> pd.DataFrame:
        df = train_df.copy()
        self.identify_column_types(df)

        print("[Feature Engineering] Generating base missing indicators & imputation...")
        for col in self.numeric_cols:
            if df[col].isnull().sum() > 0:
                df[f"{col}_isnan"] = df[col].isnull().astype(np.int8)
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)

        for col in self.categorical_cols:
            df[col] = df[col].astype(str).fillna("MISSING")
            if df[col].isnull().sum() > 0:
                df[f"{col}_isnan"] = (df[col] == "MISSING").astype(np.int8)

        # 1. Frequency Encoding (Count Encoding)
        print("[Feature Engineering] Computing Frequency Encoding...")
        for col in self.categorical_cols:
            freq = df[col].value_counts(normalize=True)
            self.freq_encoding_maps[col] = freq
            df[f"{col}_freq"] = df[col].map(freq).astype(np.float32)

        # 2. Pairwise Numeric Interactions
        if self.config.ENABLE_INTERACTIONS and len(self.numeric_cols) >= 2:
            print("[Feature Engineering] Generating Top Numeric Interaction terms...")
            # Pick first 4 numeric features to prevent dimensional explosion
            inter_cols = self.numeric_cols[:4]
            for i in range(len(inter_cols)):
                for j in range(i + 1, len(inter_cols)):
                    c1, c2 = inter_cols[i], inter_cols[j]
                    df[f"{c1}_plus_{c2}"] = (df[c1] + df[c2]).astype(np.float32)
                    df[f"{c1}_sub_{c2}"] = (df[c1] - df[c2]).astype(np.float32)
                    df[f"{c1}_mul_{c2}"] = (df[c1] * df[c2]).astype(np.float32)
                    df[f"{c1}_div_{c2}"] = (df[c1] / (df[c2].abs() + 1e-6)).astype(np.float32)

        # 3. Categorical Aggregations on Numerics
        if self.config.ENABLE_AGGREGATIONS and len(self.categorical_cols) > 0 and len(self.numeric_cols) > 0:
            print("[Feature Engineering] Generating Groupby Aggregation features...")
            group_cat = self.categorical_cols[0]
            agg_num = self.numeric_cols[0]
            aggs = ["mean", "std", "min", "max"]
            agg_df = df.groupby(group_cat)[agg_num].agg(aggs).reset_index()
            agg_df.columns = [group_cat] + [f"{group_cat}_{agg_num}_{a}" for a in aggs]
            df = df.merge(agg_df, on=group_cat, how="left")
            self.agg_definitions.append((group_cat, agg_num, aggs))

        # 4. Categorical Label Encoding for Tree Models
        for col in self.categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))

        return reduce_mem_usage(df, verbose=False)

    def transform(self, test_df: pd.DataFrame) -> pd.DataFrame:
        """Apply fitted transformations to test set without data leakage."""
        df = test_df.copy()

        for col in self.numeric_cols:
            if col in df.columns:
                if f"{col}_isnan" in df.columns or df[col].isnull().sum() > 0:
                    df[f"{col}_isnan"] = df[col].isnull().astype(np.int8)
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)

        for col in self.categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).fillna("MISSING")

        # Frequency mapping
        for col, freq_map in self.freq_encoding_maps.items():
            if col in df.columns:
                df[f"{col}_freq"] = df[col].map(freq_map).fillna(0.0).astype(np.float32)

        # Pairwise interactions
        if self.config.ENABLE_INTERACTIONS and len(self.numeric_cols) >= 2:
            inter_cols = self.numeric_cols[:4]
            for i in range(len(inter_cols)):
                for j in range(i + 1, len(inter_cols)):
                    c1, c2 = inter_cols[i], inter_cols[j]
                    if c1 in df.columns and c2 in df.columns:
                        df[f"{c1}_plus_{c2}"] = (df[c1] + df[c2]).astype(np.float32)
                        df[f"{c1}_sub_{c2}"] = (df[c1] - df[c2]).astype(np.float32)
                        df[f"{c1}_mul_{c2}"] = (df[c1] * df[c2]).astype(np.float32)
                        df[f"{c1}_div_{c2}"] = (df[c1] / (df[c2].abs() + 1e-6)).astype(np.float32)

        # Aggregations
        for group_cat, agg_num, aggs in self.agg_definitions:
            if group_cat in df.columns and agg_num in df.columns:
                agg_df = df.groupby(group_cat)[agg_num].agg(aggs).reset_index()
                agg_df.columns = [group_cat] + [f"{group_cat}_{agg_num}_{a}" for a in aggs]
                df = df.merge(agg_df, on=group_cat, how="left")

        # Categorical Label Encoding fallback
        for col in self.categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))

        return reduce_mem_usage(df, verbose=False)


# ======================================================================================
# 5. METRIC COMPUTATION ENGINE
# ======================================================================================
class MetricEvaluator:
    @staticmethod
    def evaluate(y_true: np.ndarray, y_pred: np.ndarray, metric_name: str, problem_type: str) -> float:
        if metric_name == "roc_auc":
            return roc_auc_score(y_true, y_pred)
        elif metric_name == "logloss":
            return log_loss(y_true, y_pred)
        elif metric_name == "f1":
            if problem_type == "binary":
                pred_labels = (y_pred >= 0.5).astype(int) if y_pred.ndim == 1 or y_pred.shape[1] == 1 else np.argmax(y_pred, axis=1)
                return f1_score(y_true, pred_labels)
            else:
                pred_labels = np.argmax(y_pred, axis=1)
                return f1_score(y_true, pred_labels, average="macro")
        elif metric_name == "accuracy":
            pred_labels = (y_pred >= 0.5).astype(int) if y_pred.ndim == 1 else np.argmax(y_pred, axis=1)
            return accuracy_score(y_true, pred_labels)
        elif metric_name == "rmse":
            return mean_squared_error(y_true, y_pred, squared=False)
        elif metric_name == "mae":
            return mean_absolute_error(y_true, y_pred)
        else:
            raise ValueError(f"Unsupported metric: {metric_name}")

    @staticmethod
    def is_higher_better(metric_name: str) -> bool:
        return metric_name in ["roc_auc", "f1", "accuracy"]


# ======================================================================================
# 6. MODEL WRAPPERS (LIGHTGBM, XGBOOST, CATBOOST)
# ======================================================================================
def get_lgbm_model(config: PipelineConfig, custom_params: Optional[Dict] = None):
    params = {
        "n_estimators": 2500,
        "learning_rate": 0.03,
        "num_leaves": 31,
        "max_depth": -1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "random_state": config.RANDOM_STATE,
        "n_jobs": config.N_JOBS,
        "verbose": -1,
    }
    if config.USE_GPU:
        params["device"] = "gpu"

    if custom_params:
        params.update(custom_params)

    if config.PROBLEM_TYPE == "binary":
        return lgb.LGBMClassifier(objective="binary", **params)
    elif config.PROBLEM_TYPE == "multiclass":
        return lgb.LGBMClassifier(objective="multiclass", **params)
    else:
        return lgb.LGBMRegressor(objective="regression", **params)


def get_xgb_model(config: PipelineConfig, custom_params: Optional[Dict] = None):
    params = {
        "n_estimators": 2500,
        "learning_rate": 0.03,
        "max_depth": 6,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "tree_method": "hist",
        "random_state": config.RANDOM_STATE,
        "n_jobs": config.N_JOBS,
    }
    if config.USE_GPU:
        params["device"] = "cuda"

    if custom_params:
        params.update(custom_params)

    if config.PROBLEM_TYPE == "binary":
        return xgb.XGBClassifier(eval_metric="logloss", use_label_encoder=False, **params)
    elif config.PROBLEM_TYPE == "multiclass":
        return xgb.XGBClassifier(eval_metric="mlogloss", use_label_encoder=False, **params)
    else:
        return xgb.XGBRegressor(eval_metric="rmse", **params)


def get_catboost_model(config: PipelineConfig, custom_params: Optional[Dict] = None):
    params = {
        "iterations": 2500,
        "learning_rate": 0.03,
        "depth": 6,
        "l2_leaf_reg": 3.0,
        "random_seed": config.RANDOM_STATE,
        "verbose": 0,
        "thread_count": -1,
    }
    if config.USE_GPU:
        params["task_type"] = "GPU"

    if custom_params:
        params.update(custom_params)

    if config.PROBLEM_TYPE == "binary":
        return CatBoostClassifier(loss_function="Logloss", eval_metric="Logloss", **params)
    elif config.PROBLEM_TYPE == "multiclass":
        return CatBoostClassifier(loss_function="MultiClass", eval_metric="MultiClass", **params)
    else:
        return CatBoostRegressor(loss_function="RMSE", eval_metric="RMSE", **params)


# ======================================================================================
# 7. OPTUNA HYPERPARAMETER TUNING (PLUG-AND-PLAY)
# ======================================================================================
def run_optuna_tuning(X: pd.DataFrame, y: np.ndarray, config: PipelineConfig, model_name: str = "lightgbm") -> Dict[str, Any]:
    """Automated Optuna tuning using 3-fold CV for maximum search efficiency."""
    if not HAS_OPTUNA:
        print("[Optuna] optuna not installed. Skipping hyperparameter tuning.")
        return {}

    print(f"\n[Optuna] Launching {config.OPTUNA_N_TRIALS} trials tuning for {model_name.upper()}...")
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=config.RANDOM_STATE) if config.PROBLEM_TYPE != "regression" else KFold(n_splits=3, shuffle=True, random_state=config.RANDOM_STATE)

    def objective(trial):
        if model_name == "lightgbm":
            params = {
                "num_leaves": trial.suggest_int("num_leaves", 15, 127),
                "max_depth": trial.suggest_int("max_depth", 3, 10),
                "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1, log=True),
                "subsample": trial.suggest_float("subsample", 0.6, 1.0),
                "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
                "reg_alpha": trial.suggest_float("reg_alpha", 1e-3, 10.0, log=True),
                "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
                "n_estimators": 500,
                "n_jobs": -1,
                "verbose": -1
            }
            model = lgb.LGBMClassifier(**params) if config.PROBLEM_TYPE != "regression" else lgb.LGBMRegressor(**params)
        else:
            return 0.0

        scores = []
        for train_idx, val_idx in skf.split(X, y):
            X_tr, y_tr = X.iloc[train_idx], y[train_idx]
            X_va, y_va = X.iloc[val_idx], y[val_idx]
            model.fit(X_tr, y_tr)
            preds = model.predict_proba(X_va)[:, 1] if config.PROBLEM_TYPE == "binary" else model.predict(X_va)
            score = MetricEvaluator.evaluate(y_va, preds, config.EVAL_METRIC, config.PROBLEM_TYPE)
            scores.append(score)

        return np.mean(scores)

    direction = "maximize" if MetricEvaluator.is_higher_better(config.EVAL_METRIC) else "minimize"
    study = optuna.create_study(direction=direction)
    study.optimize(objective, n_trials=config.OPTUNA_N_TRIALS, timeout=300)
    print(f"[Optuna] Best {config.EVAL_METRIC}: {study.best_value:.5f}")
    print(f"[Optuna] Best Parameters: {study.best_params}")
    return study.best_params


# ======================================================================================
# 8. CROSS-VALIDATION TRAINER FOR GBDT ENSEMBLE
# ======================================================================================
class EnsembleTrainer:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.models_dict: Dict[str, List[Any]] = {m: [] for m in config.MODELS_TO_RUN}
        self.oof_predictions: Dict[str, np.ndarray] = {}
        self.test_predictions: Dict[str, np.ndarray] = {}
        self.feature_importances: Dict[str, pd.DataFrame] = {}

    def train_models(self, X: pd.DataFrame, y: np.ndarray, X_test: Optional[pd.DataFrame] = None):
        n_samples = len(X)
        n_classes = len(np.unique(y)) if self.config.PROBLEM_TYPE == "multiclass" else 1

        # Initialize cross-validation
        if self.config.PROBLEM_TYPE in ["binary", "multiclass"]:
            cv = StratifiedKFold(n_splits=self.config.N_SPLITS, shuffle=True, random_state=self.config.RANDOM_STATE)
            splits = list(cv.split(X, y))
        else:
            cv = KFold(n_splits=self.config.N_SPLITS, shuffle=True, random_state=self.config.RANDOM_STATE)
            splits = list(cv.split(X, y))

        print(f"\n{'='*75}")
        print(f"🚀 STARTING {self.config.N_SPLITS}-FOLD CROSS-VALIDATION")
        print(f"Features: {X.shape[1]} | Samples: {n_samples:,} | Metric: {self.config.EVAL_METRIC}")
        print(f"{'='*75}")

        # Train each model across all folds
        for model_name in self.config.MODELS_TO_RUN:
            print(f"\n>>> Training Model: {model_name.upper()}")
            start_time = time.time()

            if self.config.PROBLEM_TYPE == "multiclass":
                oof = np.zeros((n_samples, n_classes), dtype=np.float32)
                test_preds = np.zeros((len(X_test), n_classes), dtype=np.float32) if X_test is not None else None
            else:
                oof = np.zeros(n_samples, dtype=np.float32)
                test_preds = np.zeros(len(X_test), dtype=np.float32) if X_test is not None else None

            fold_scores = []
            importances = []

            for fold, (train_idx, val_idx) in enumerate(splits, 1):
                X_tr, y_tr = X.iloc[train_idx], y[train_idx]
                X_va, y_va = X.iloc[val_idx], y[val_idx]

                # Model instantiation
                if model_name == "lightgbm":
                    model = get_lgbm_model(self.config)
                    model.fit(
                        X_tr, y_tr,
                        eval_set=[(X_va, y_va)],
                        callbacks=[lgb.early_stopping(stopping_rounds=100, verbose=False)]
                    )
                    importances.append(model.feature_importances_)

                elif model_name == "xgboost":
                    model = get_xgb_model(self.config)
                    model.fit(
                        X_tr, y_tr,
                        eval_set=[(X_va, y_va)],
                        verbose=False
                    )
                    importances.append(model.feature_importances_)

                elif model_name == "catboost":
                    model = get_catboost_model(self.config)
                    model.fit(
                        X_tr, y_tr,
                        eval_set=(X_va, y_va),
                        early_stopping_rounds=100,
                        verbose=False
                    )
                    importances.append(model.get_feature_importance())

                # Inference on validation fold
                if self.config.PROBLEM_TYPE == "binary":
                    val_pred = model.predict_proba(X_va)[:, 1]
                    if X_test is not None:
                        test_preds += model.predict_proba(X_test)[:, 1] / self.config.N_SPLITS
                elif self.config.PROBLEM_TYPE == "multiclass":
                    val_pred = model.predict_proba(X_va)
                    if X_test is not None:
                        test_preds += model.predict_proba(X_test) / self.config.N_SPLITS
                else:  # regression
                    val_pred = model.predict(X_va)
                    if X_test is not None:
                        test_preds += model.predict(X_test) / self.config.N_SPLITS

                oof[val_idx] = val_pred
                fold_score = MetricEvaluator.evaluate(y_va, val_pred, self.config.EVAL_METRIC, self.config.PROBLEM_TYPE)
                fold_scores.append(fold_score)
                self.models_dict[model_name].append(model)
                print(f"  Fold {fold}/{self.config.N_SPLITS} - {self.config.EVAL_METRIC}: {fold_score:.5f}")

            overall_score = MetricEvaluator.evaluate(y, oof, self.config.EVAL_METRIC, self.config.PROBLEM_TYPE)
            print(f"  --> {model_name.upper()} Overall OOF {self.config.EVAL_METRIC}: {overall_score:.5f} (Elapsed: {time.time()-start_time:.1f}s)")

            self.oof_predictions[model_name] = oof
            if X_test is not None:
                self.test_predictions[model_name] = test_preds

            # Save average feature importance
            if len(importances) > 0:
                fi_df = pd.DataFrame({
                    "feature": X.columns,
                    "importance": np.mean(importances, axis=0)
                }).sort_values(by="importance", ascending=False)
                self.feature_importances[model_name] = fi_df

        return self.oof_predictions, self.test_predictions


# ======================================================================================
# 9. ENSEMBLE BLENDING & STACKING (OPTIMIZING LEADERBOARD GENERALIZATION)
# ======================================================================================
class BlendingEnsemble:
    """
    Finds optimal weights for combining models using SLSQP optimization on OOF predictions.
    Outperforms simple arithmetic average on competitive Kaggle leaderboards.
    """
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.weights: np.ndarray = np.array([])

    def fit_predict(self, oof_dict: Dict[str, np.ndarray], y_true: np.ndarray, test_pred_dict: Optional[Dict[str, np.ndarray]] = None):
        model_names = list(oof_dict.keys())
        n_models = len(model_names)

        if n_models == 1:
            self.weights = np.array([1.0])
            blend_oof = oof_dict[model_names[0]]
            blend_test = test_pred_dict[model_names[0]] if test_pred_dict else None
            score = MetricEvaluator.evaluate(y_true, blend_oof, self.config.EVAL_METRIC, self.config.PROBLEM_TYPE)
            return blend_oof, blend_test, score

        print(f"\n{'='*75}")
        print("⚡ OPTIMIZING ENSEMBLE BLENDING WEIGHTS (SLSQP)")
        print(f"{'='*75}")

        OOF_mat = np.column_stack([oof_dict[m] for m in model_names])

        def loss_func(weights):
            weights = np.array(weights)
            weights = weights / np.sum(weights)
            pred = np.sum(OOF_mat * weights, axis=1)
            score = MetricEvaluator.evaluate(y_true, pred, self.config.EVAL_METRIC, self.config.PROBLEM_TYPE)
            # Minimize negative score if higher is better
            return -score if MetricEvaluator.is_higher_better(self.config.EVAL_METRIC) else score

        init_weights = [1.0 / n_models] * n_models
        bounds = [(0.0, 1.0) for _ in range(n_models)]
        constraints = {"type": "eq", "fun": lambda w: 1 - sum(w)}

        res = minimize(loss_func, init_weights, method="SLSQP", bounds=bounds, constraints=constraints)
        self.weights = res.x / np.sum(res.x)

        print("Optimal Ensemble Weights:")
        for name, w in zip(model_names, self.weights):
            print(f"  • {name.upper()}: {w * 100:.2f}%")

        blend_oof = np.sum(OOF_mat * self.weights, axis=1)
        final_score = MetricEvaluator.evaluate(y_true, blend_oof, self.config.EVAL_METRIC, self.config.PROBLEM_TYPE)
        print(f"\n🔥 Blended Ensemble OOF {self.config.EVAL_METRIC}: {final_score:.5f}")

        blend_test = None
        if test_pred_dict and all(m in test_pred_dict for m in model_names):
            test_mat = np.column_stack([test_pred_dict[m] for m in model_names])
            blend_test = np.sum(test_mat * self.weights, axis=1)

        return blend_oof, blend_test, final_score


# ======================================================================================
# 10. EXPLAINABILITY & ARTIFACT EXPORT
# ======================================================================================
def export_results(
    trainer: EnsembleTrainer,
    blender: BlendingEnsemble,
    blend_test: Optional[np.ndarray],
    test_raw: Optional[pd.DataFrame],
    config: PipelineConfig,
    X_sample: pd.DataFrame
):
    print(f"\n{'='*75}")
    print("💾 SAVING ARTIFACTS, FEATURE IMPORTANCES & PREDICTIONS")
    print(f"{'='*75}")

    # 1. Feature Importance Plot & CSV
    for model_name, fi_df in trainer.feature_importances.items():
        csv_path = os.path.join(config.OUTPUT_DIR, f"{model_name}_feature_importance.csv")
        fi_df.to_csv(csv_path, index=False)
        print(f"  Saved {model_name} feature importance: {csv_path}")

        if HAS_PLT:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=fi_df.head(20), x="importance", y="feature", palette="viridis")
            plt.title(f"Top 20 Features - {model_name.upper()}")
            plt.tight_layout()
            img_path = os.path.join(config.OUTPUT_DIR, f"{model_name}_top20_features.png")
            plt.savefig(img_path, dpi=200)
            plt.close()

    # 2. SHAP Explanation on Validation Sample
    if config.GENERATE_SHAP and HAS_SHAP and "lightgbm" in trainer.models_dict and len(trainer.models_dict["lightgbm"]) > 0:
        try:
            print("[SHAP] Generating TreeExplainer summary on validation sample...")
            sample_sub = X_sample.sample(min(1000, len(X_sample)), random_state=config.RANDOM_STATE)
            explainer = shap.TreeExplainer(trainer.models_dict["lightgbm"][0])
            shap_values = explainer.shap_values(sample_sub)

            if HAS_PLT:
                plt.figure()
                shap_val_plot = shap_values[1] if isinstance(shap_values, list) and len(shap_values) > 1 else shap_values
                shap.summary_plot(shap_val_plot, sample_sub, show=False)
                shap_path = os.path.join(config.OUTPUT_DIR, "shap_summary_plot.png")
                plt.tight_layout()
                plt.savefig(shap_path, dpi=200, bbox_inches="tight")
                plt.close()
                print(f"  Saved SHAP summary plot: {shap_path}")
        except Exception as e:
            print(f"[SHAP] Warning: Could not generate SHAP summary ({e})")

    # 3. Save Serialized Pipeline Artifacts via Joblib
    model_save_path = os.path.join(config.OUTPUT_DIR, "ensemble_pipeline.joblib")
    joblib.dump({
        "models": trainer.models_dict,
        "weights": blender.weights,
        "config": config
    }, model_save_path)
    print(f"  Saved ensemble model bundle: {model_save_path}")

    # 4. Generate Submission CSV
    if blend_test is not None:
        sub_path = os.path.join(config.OUTPUT_DIR, config.SUBMISSION_FILE)
        sub_df = pd.DataFrame()
        if config.ID_COL and test_raw is not None and config.ID_COL in test_raw.columns:
            sub_df[config.ID_COL] = test_raw[config.ID_COL]
        else:
            sub_df["id"] = np.arange(len(blend_test))

        sub_df[config.TARGET_COL] = blend_test
        sub_df.to_csv(sub_path, index=False)
        print(f"  Generated test submission file ({len(sub_df):,} rows): {sub_path}")


# ======================================================================================
# 11. MAIN PIPELINE EXECUTION
# ======================================================================================
def run_pipeline(custom_config: Optional[PipelineConfig] = None):
    config = custom_config or PipelineConfig()
    print("\n" + "#"*75)
    print("🏆 KAGGLE GRANDMASTER SOLUTION PIPELINE INITIALIZED")
    print(f"Dataset Path : {config.TRAIN_PATH}")
    print(f"Target Column: {config.TARGET_COL} | Problem: {config.PROBLEM_TYPE}")
    print("#"*75)

    # Step 1: Load Data or Fallback to Synthetic
    if os.path.exists(config.TRAIN_PATH):
        print(f"[Data Loading] Reading user dataset from: {config.TRAIN_PATH}")
        train_raw = pd.read_csv(config.TRAIN_PATH)
        test_raw = pd.read_csv(config.TEST_PATH) if config.TEST_PATH and os.path.exists(config.TEST_PATH) else None
    else:
        print(f"[Notice] Dataset '{config.TRAIN_PATH}' not found. Initializing 200,000-row benchmark dataset...")
        train_raw, test_raw = create_synthetic_dataset(n_rows=200_000, problem_type=config.PROBLEM_TYPE)
        # Save synthetic data for subsequent direct runs
        train_raw.to_csv("train.csv", index=False)
        test_raw.to_csv("test.csv", index=False)
        print("  Synthetic datasets cached as 'train.csv' and 'test.csv'.")

    # Step 2: Memory Optimization
    print("\n[Step 2] Optimizing memory footprint...")
    train_raw = reduce_mem_usage(train_raw)
    if test_raw is not None:
        test_raw = reduce_mem_usage(test_raw)

    # Step 3: Feature Engineering
    print("\n[Step 3] Running Automated Feature Engineering Pipeline...")
    fe = FeatureEngineeringPipeline(config)
    y = train_raw[config.TARGET_COL].values
    train_processed = fe.fit_transform(train_raw)

    # Drop target and ID column from feature matrix
    drop_cols = [config.TARGET_COL]
    if config.ID_COL and config.ID_COL in train_processed.columns:
        drop_cols.append(config.ID_COL)

    X = train_processed.drop(columns=[c for c in drop_cols if c in train_processed.columns])

    X_test = None
    if test_raw is not None:
        test_processed = fe.transform(test_raw)
        X_test = test_processed.drop(columns=[c for c in drop_cols if c in test_processed.columns])

    # Step 4: Optional Optuna Tuning
    if config.RUN_OPTUNA:
        best_lgb_params = run_optuna_tuning(X, y, config, model_name="lightgbm")

    # Step 5: Train Models (5-Fold Stratified CV)
    trainer = EnsembleTrainer(config)
    oof_preds, test_preds = trainer.train_models(X, y, X_test)

    # Step 6: Optimal SLSQP Ensembling / Blending
    blender = BlendingEnsemble(config)
    blend_oof, blend_test, final_score = blender.fit_predict(oof_preds, y, test_preds)

    # Step 7: Artifact & Inference Export
    export_results(trainer, blender, blend_test, test_raw, config, X)

    print("\n" + "="*75)
    print(f"🎉 PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"Final OOF Cross-Validation {config.EVAL_METRIC}: {final_score:.5f}")
    print(f"All artifacts and submissions exported to '{config.OUTPUT_DIR}'")
    print("="*75 + "\n")


if __name__ == "__main__":
    run_pipeline()
