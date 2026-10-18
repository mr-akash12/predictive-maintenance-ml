"""Central project paths and modelling configuration."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / 'data' / 'raw' / 'ai4i2020.csv'
PROCESSED_DATA = ROOT / 'data' / 'processed' / 'ai4i2020_clean.csv'
ARTIFACTS = ROOT / 'artifacts'
FIGURES = ROOT / 'reports' / 'figures'
DATABASE = ROOT / 'data' / 'processed' / 'maintenance.db'
MODEL_PATH = ARTIFACTS / 'random_forest_pipeline.joblib'
METRICS_PATH = ARTIFACTS / 'evaluation_metrics.json'
SEED = 42
TEST_SIZE = 0.2
TARGET = 'Machine failure'
NUMERIC_FEATURES = ['Air temperature [K]', 'Process temperature [K]',
                    'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']
CATEGORICAL_FEATURES = ['Type']
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES
LEAKAGE_COLUMNS = ['TWF', 'HDF', 'PWF', 'OSF', 'RNF', 'Failure Type', 'UDI', 'Product ID']
EXPECTED_COLUMNS = ['UDI', 'Product ID', *FEATURES, TARGET, 'TWF', 'HDF', 'PWF', 'OSF', 'RNF']

def create_output_dirs():
    for folder in (PROCESSED_DATA.parent, ARTIFACTS, FIGURES):
        folder.mkdir(parents=True, exist_ok=True)
