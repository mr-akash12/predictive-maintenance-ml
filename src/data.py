"""Dataset loading, explicit validation and non-destructive cleaning."""
import argparse
import json
import pandas as pd
from .config import RAW_DATA, PROCESSED_DATA, EXPECTED_COLUMNS, FEATURES, TARGET, create_output_dirs


def inspect_quality(df: pd.DataFrame) -> dict:
    return {
        'rows': int(len(df)), 'columns': int(df.shape[1]),
        'missing_by_column': {c: int(v) for c, v in df.isna().sum().items()},
        'duplicate_rows': int(df.duplicated().sum()),
        'duplicate_udi': int(df['UDI'].duplicated().sum()),
        'dtypes': {c: str(t) for c, t in df.dtypes.items()},
        'target_counts': {str(k): int(v) for k, v in df[TARGET].value_counts().items()},
    }


def load_data(path=RAW_DATA) -> pd.DataFrame:
    path = __import__('pathlib').Path(path)
    if not path.is_file():
        raise FileNotFoundError(f'Dataset missing: {path}. Keep ai4i2020.csv in data/raw/.')
    df = pd.read_csv(path)
    missing = sorted(set(EXPECTED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f'Missing required dataset columns: {missing}')
    if df.columns.duplicated().any():
        raise ValueError('Duplicate column names are not supported.')
    if df[TARGET].isna().any() or not df[TARGET].isin([0, 1]).all():
        raise ValueError('Machine failure must contain only binary 0/1 values.')
    for c in FEATURES[1:]:
        if not pd.api.types.is_numeric_dtype(df[c]):
            raise ValueError(f'Expected numeric sensor column: {c}')
    if df['Type'].dropna().isin(['L', 'M', 'H']).all() is False:
        raise ValueError('Unexpected Type values; expected L, M or H.')
    if df['UDI'].isna().any() or df['UDI'].duplicated().any():
        raise ValueError('UDI must be non-null and unique.')
    return df


def prepare_clean_data(save=True) -> pd.DataFrame:
    df = load_data().copy()
    if df.duplicated().any():
        raise ValueError('Duplicate full rows found; review source before modelling.')
    # Keep missing sensor observations as missing: pipeline imputes from training only.
    if save:
        create_output_dirs()
        df.to_csv(PROCESSED_DATA, index=False)
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-save', action='store_true')
    args = parser.parse_args()
    print(json.dumps(inspect_quality(prepare_clean_data(save=not args.no_save)), indent=2))

if __name__ == '__main__':
    main()
