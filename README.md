# Predictive Maintenance: Machine Failure Prediction and Operational Insights

An end-to-end, **portfolio-only** machine-failure binary classifier and operational analytics project, based on the **synthetic** UCI AI4I 2020 dataset. It demonstrates exploratory analysis, leakage-aware modelling, held-out evaluation, SQLite/SQL analysis, and a Power BI build guide. **It does not establish real factory performance, forecast failure time, or support a deployable maintenance decision without additional validation.**

## Dataset and label
- Source: UCI Machine Learning Repository, *AI4I 2020 Predictive Maintenance Dataset* (the original CSV is preserved under `data/raw/`).
- 10,000 records; target: `Machine failure` (0 or 1). Dataset includes product type and five operational measurements.
- Inputs are strictly: `Type`, `Air temperature [K]`, `Process temperature [K]`, `Rotational speed [rpm]`, `Torque [Nm]`, `Tool wear [min]`.
- Excluded from the input pipeline: `UDI`, `Product ID`, `TWF`, `HDF`, `PWF`, `OSF`, `RNF`, and `Failure Type` (if present). Failure flags leak target information. No genuine timestamps or machine-specific longitudinal sensor histories exist.
- A random stratified split tests generalisation to held-out **synthetic rows**, not future factory events.

## Layout
```text
predictive_maintenance_ml/
├── data/raw/ai4i2020.csv             # original, unchanged
├── data/processed/                  # derived CSV / local SQLite
├── notebooks/01_eda.ipynb
├── src/{config,data,features,eda,train,evaluate,database}.py
├── sql/{schema,analysis_queries}.sql
├── powerbi/{dashboard_guide.md,measures.dax}
├── artifacts/                        # model + metric outputs
├── reports/{project_report.md,figures/}
├── requirements.txt
└── .gitignore
```

## Windows / VS Code quick start
Install Python **3.11** and VS Code with the Python and Jupyter extensions. Extract the ZIP, open the **`predictive_maintenance_ml` folder** in VS Code (**File → Open Folder**) and launch **Terminal → New Terminal** (PowerShell).

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
If PowerShell blocks activation, use `.venv\Scripts\python.exe` instead of `python` in subsequent commands or adjust execution policy according to your organisation's security policy. VS Code: **Python: Select Interpreter** → `.venv\Scripts\python.exe`.

### Commands to run (in order, from project root)
```powershell
python -m src.data
python -m src.eda
python -m src.train
python -m src.evaluate
python -m src.database --init
python -m src.database --summary
```
Optional comparison (install dependency and re-train):
```powershell
python -m pip install "xgboost>=2,<4"
python -m src.train --compare-xgboost
python -m src.evaluate
```
XGBoost is evaluated on an **inner validation partition of training data**; the saved deployable baseline remains Random Forest and the test partition is not used for comparison. For a fair model-selection study, use nested CV and a pre-declared threshold/cost framework.

### Notebook and reports
Open `notebooks/01_eda.ipynb`, select your `.venv` kernel, and **Run All**. The notebook resolves the project root from either the notebook folder or project root. EDA plots appear in `reports/figures/`; fitted pipeline: `artifacts/random_forest_pipeline.joblib`; evaluated test scores: `artifacts/evaluation_metrics.json`. `.joblib` files must be loaded **only from trusted sources**. Generated files are optional outputs and are ignored by Git.

### SQLite and SQL
`python -m src.database --init` creates `data/processed/maintenance.db` with a single `machine_observations` table. Rerunning init **replaces rows in this derived database** (not the raw CSV). `--summary` validates descriptive totals by product type. Open SQLite using a local GUI or CLI and execute `sql/analysis_queries.sql`; the queries require the database schema from `sql/schema.sql`.

### Power BI
See `powerbi/dashboard_guide.md` for CSV / optional SQLite ODBC loading, exact field mappings, suggested visuals, and measures. Create the `.pbix` report manually in Power BI Desktop; this archive provides specifications, **not** a completed Power BI binary file.

## Methodology and interpretation
A class-weighted Random Forest (200 trees) follows imputation and one-hot encoding fitted **only to training rows**. Hold-out evaluation reports precision, recall, F1, ROC-AUC, average precision and confusion matrix. A **false negative** means a missed labelled failure; a **false positive** means a potentially unnecessary maintenance investigation. The 0.50 threshold is a baseline, **not a cost-optimised alert threshold**. The low failure prevalence makes raw accuracy a poor decision metric. No causal or forecasting claims are warranted.

## Constraints and possible extensions
Synthetic data, no timestamps, no entity-level separation, one random split, and no real maintenance costs, drift testing, calibration or external validation. Future work: genuine timestamped histories, group/time splits, operator-reviewed decision costs, threshold optimisation using training-only validation, calibration and drift monitoring. See `reports/project_report.md`.
