# Verification record

Validation completed in the execution environment (Python 3.13; Windows PowerShell environment was not available).

- Original raw dataset SHA-256 preserved byte-for-byte: verified against input ZIP.
- Data load, expected 14 columns, target validation, and 10,000-row ingestion: passed.
- Python module syntax compile and imports: passed.
- Stratified training of 8,000 records and held-out evaluation of 2,000: passed.
- Four EDA and three evaluation figures: generated.
- Notebook nbformat structural validation and six code cells executed: passed.
- SQLite schema, 10,000 inserted rows, 339 positives: passed.
- All four analysis SQL statements executed successfully.
- Power BI .pbix not built or tested; Desktop manual build remains required.
- Optional XGBoost comparison not executed; opt-in code provided.
- Windows PowerShell installation and VS Code run not tested here.

Metrics in `artifacts/evaluation_metrics.json` are outcomes of this specific synthetic train/test split, not field deployment claims.
