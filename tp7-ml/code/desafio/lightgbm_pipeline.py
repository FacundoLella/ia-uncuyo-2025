#!/usr/bin/env python3
"""Entrena un modelo LightGBM para el desafío de arbolado público."""

import argparse
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split

import lightgbm as lgb


CAT_COLS = ["especie", "seccion", "nombre_seccion"]
NUMERIC_COLS = [
    "altura",
    "circ_tronco_cm",
    "diametro_tronco",
    "long",
    "lat",
    "area_seccion",
    "mod_year",
    "mod_month",
    "mod_day",
    "mod_hour",
    "mod_wday",
    "densidad_tronco",
    "relacion_altura_circ",
    "altura_div_diametro",
    "long_lat_ratio",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline LightGBM para TP7.")
    parser.add_argument("--train", default="data/arbolado-mendoza-dataset-train.csv", help="CSV con etiquetas.")
    parser.add_argument("--test", default="data/arbolado-mza-dataset-test.csv", help="CSV de Kaggle sin etiquetas.")
    parser.add_argument("--output_dir", default="code/desafio/output", help="Directorio de salidas.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help=("Umbral para binarizar probabilidades. Si se omite, se ajusta automáticamente "),
    )
    parser.add_argument("--valid_size", type=float, default=0.2, help="Proporción para la partición de validación.")
    parser.add_argument("--seed", type=int, default=2025, help="Semilla para reproducibilidad.")
    return parser.parse_args()


def _clean_str_series(series: pd.Series) -> pd.Series:
    return (
        series.fillna("desconocido")
        .astype(str)
        .str.strip()
        .str.lower()
    )


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    dt = pd.to_datetime(df["ultima_modificacion"], format="%d/%m/%Y %H:%M", errors="coerce", dayfirst=True)
    df["mod_year"] = dt.dt.year
    df["mod_month"] = dt.dt.month
    df["mod_day"] = dt.dt.day
    df["mod_hour"] = dt.dt.hour
    df["mod_wday"] = dt.dt.dayofweek

    for col in ["altura", "circ_tronco_cm", "diametro_tronco", "long", "lat", "area_seccion"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["densidad_tronco"] = df["circ_tronco_cm"] / (df["diametro_tronco"] + 1)
    df["relacion_altura_circ"] = df["altura"] / (df["circ_tronco_cm"] + 1)
    df["altura_div_diametro"] = df["altura"] / (df["diametro_tronco"] + 1)
    df["long_lat_ratio"] = df["long"] / (df["lat"].abs() + 1e-3)

    return df


def encode_categories(
    df: pd.DataFrame, mappings: Dict[str, Dict[str, int]] = None
) -> Tuple[pd.DataFrame, Dict[str, Dict[str, int]]]:
    df = df.copy()
    if mappings is None:
        mappings = {}
        for col in CAT_COLS:
            cleaned = _clean_str_series(df[col])
            unique_vals = sorted(cleaned.unique())
            mappings[col] = {val: idx for idx, val in enumerate(unique_vals)}
            df[col] = cleaned.map(mappings[col]).astype("int32")
    else:
        for col in CAT_COLS:
            cleaned = _clean_str_series(df[col])
            default_idx = len(mappings[col])
            df[col] = cleaned.map(lambda x: mappings[col].get(x, default_idx)).astype("int32")
    return df, mappings


def prepare_datasets(train_path: str, test_path: str):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    train_ids = train_df["id"].copy()
    test_ids = test_df["id"].copy()

    train_df = add_engineered_features(train_df)
    test_df = add_engineered_features(test_df)

    numeric_medians = train_df[NUMERIC_COLS].median()
    train_df[NUMERIC_COLS] = train_df[NUMERIC_COLS].fillna(numeric_medians)
    test_df[NUMERIC_COLS] = test_df[NUMERIC_COLS].fillna(numeric_medians)

    train_df, cat_maps = encode_categories(train_df)
    test_df, _ = encode_categories(test_df, cat_maps)

    features = train_df[NUMERIC_COLS + CAT_COLS].copy()
    labels = train_df["inclinacion_peligrosa"].astype(int)
    test_features = test_df[NUMERIC_COLS + CAT_COLS].copy()
    return features, labels, test_features, train_ids, test_ids


def compute_metrics(y_true: np.ndarray, probas: np.ndarray, threshold: float) -> Dict[str, float]:
    preds = (probas >= threshold).astype(int)
    return {
        "auc": roc_auc_score(y_true, probas),
        "accuracy": accuracy_score(y_true, preds),
        "precision": precision_score(y_true, preds, zero_division=0),
        "recall": recall_score(y_true, preds, zero_division=0),
    }


def train_lightgbm(X: pd.DataFrame, y: pd.Series, valid_size: float, seed: int):
    X_train, X_valid, y_train, y_valid = train_test_split(
        X,
        y,
        test_size=valid_size,
        stratify=y,
        random_state=seed,
    )

    scale_pos_weight = (len(y_train) - y_train.sum()) / y_train.sum()
    params = dict(
        objective="binary",
        learning_rate=0.05,
        n_estimators=1200,
        max_depth=-1,
        num_leaves=48,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        n_jobs=-1,
        random_state=seed,
        scale_pos_weight=scale_pos_weight,
    )

    clf = lgb.LGBMClassifier(**params)
    clf.fit(
        X_train,
        y_train,
        eval_set=[(X_valid, y_valid)],
        eval_metric="auc",
        callbacks=[lgb.early_stopping(stopping_rounds=50)],
    )
    return clf, X_train, X_valid, y_train, y_valid


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    X, y, X_test, train_ids, test_ids = prepare_datasets(args.train, args.test)
    clf, X_train, X_valid, y_train, y_valid = train_lightgbm(
        X, y, args.valid_size, args.seed
    )

    val_probas = clf.predict_proba(X_valid)[:, 1]
    if args.threshold is None:
        target_rate = y.mean()
        adaptive_threshold = float(np.quantile(val_probas, 1 - target_rate))
    else:
        adaptive_threshold = args.threshold

    metrics = compute_metrics(y_valid, val_probas, adaptive_threshold)
    pd.DataFrame([metrics]).to_csv(output_dir / "validation_metrics.csv", index=False)

    val_preds = pd.DataFrame(
        {
            "id": train_ids.loc[X_valid.index].values,
            "probabilidad": val_probas,
            "prediccion": (val_probas >= adaptive_threshold).astype(int),
            "real": y_valid.values,
        }
    )
    val_preds.to_csv(output_dir / "validation_predictions.csv", index=False)

    best_n_estimators = clf.best_iteration_ or clf.n_estimators
    final_model = lgb.LGBMClassifier(
        **{k: v for k, v in clf.get_params().items() if k != "n_estimators"},
        n_estimators=best_n_estimators,
    )
    final_model.fit(X, y)

    test_probas = final_model.predict_proba(X_test)[:, 1]
    submission = pd.DataFrame(
        {"ID": test_ids, "inclinacion_peligrosa": (test_probas >= adaptive_threshold).astype(int)}
    )
    submission.to_csv(output_dir / "submission_inclinacion.csv", index=False)
    print(f"Validation AUC: {metrics['auc']:.4f}")
    print(f"Umbral utilizado: {adaptive_threshold:.4f}")
    print(f"Submission guardado en {output_dir / 'submission_inclinacion.csv'}")


if __name__ == "__main__":
    main()
