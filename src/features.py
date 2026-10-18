"""Leakage-safe preprocessing and reproducible stratified hold-out split."""
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from .config import FEATURES, NUMERIC_FEATURES, CATEGORICAL_FEATURES, TARGET, TEST_SIZE, SEED


def build_preprocessor():
    numeric = Pipeline([('imputer', SimpleImputer(strategy='median'))])
    categorical = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore')),
    ])
    return ColumnTransformer([
        ('numeric', numeric, NUMERIC_FEATURES),
        ('categorical', categorical, CATEGORICAL_FEATURES),
    ])


def split_data(df):
    # Positive feature allowlist: no UDI, Product ID or failure-mode indicators.
    x = df.loc[:, FEATURES].copy()
    y = df[TARGET].astype(int).copy()
    if y.nunique() != 2:
        raise ValueError('Binary classification requires both target classes.')
    return train_test_split(x, y, test_size=TEST_SIZE, stratify=y, random_state=SEED)
