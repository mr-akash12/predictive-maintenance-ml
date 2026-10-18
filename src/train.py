"""Train a class-weighted Random Forest; optional XGBoost comparison on validation."""
import argparse
import json
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score
from .config import MODEL_PATH, ARTIFACTS, SEED, create_output_dirs
from .data import prepare_clean_data
from .features import split_data, build_preprocessor


def fit_baseline(x_train, y_train):
    model = Pipeline([
        ('preprocessor', build_preprocessor()),
        ('classifier', RandomForestClassifier(n_estimators=200, min_samples_leaf=2,
                                               class_weight='balanced_subsample',
                                               n_jobs=-1, random_state=SEED)),
    ])
    return model.fit(x_train, y_train)


def compare_optional_xgboost(x_train, y_train):
    try:
        from xgboost import XGBClassifier
    except ImportError:
        print('XGBoost is not installed; optional comparison skipped.')
        return
    x_fit, x_val, y_fit, y_val = train_test_split(
        x_train, y_train, test_size=0.25, stratify=y_train, random_state=SEED)
    ratio = (y_fit == 0).sum() / max(1, (y_fit == 1).sum())
    candidates = {
        'random_forest': fit_baseline(x_fit, y_fit),
        'xgboost': Pipeline([
            ('preprocessor', build_preprocessor()),
            ('classifier', XGBClassifier(n_estimators=200, max_depth=4, learning_rate=0.05,
                                         subsample=0.9, colsample_bytree=0.9,
                                         scale_pos_weight=ratio, eval_metric='logloss',
                                         n_jobs=2, random_state=SEED)),
        ]).fit(x_fit, y_fit),
    }
    results = {name: round(float(average_precision_score(y_val, model.predict_proba(x_val)[:, 1])), 5)
               for name, model in candidates.items()}
    (ARTIFACTS / 'optional_validation_comparison.json').write_text(
        json.dumps({'metric': 'validation_average_precision', 'results': results,
                    'note': 'Validation partition from training set only; test untouched. Baseline remains deployment model.'}, indent=2))
    print('Validation average precision:', results)


def main():
    parser = argparse.ArgumentParser(description='Train Random Forest predictive maintenance baseline.')
    parser.add_argument('--compare-xgboost', action='store_true')
    args = parser.parse_args()
    create_output_dirs()
    df = prepare_clean_data()
    x_train, _, y_train, _ = split_data(df)
    if args.compare_xgboost:
        compare_optional_xgboost(x_train, y_train)
    model = fit_baseline(x_train, y_train)
    joblib.dump(model, MODEL_PATH)
    print(f'Model saved: {MODEL_PATH} | training rows: {len(x_train)}')

if __name__ == '__main__':main()
