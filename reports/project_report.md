# Project report — Predictive Maintenance

## 1. Business problem and scope
Illustrate how a maintenance analyst could rank synthetic records for investigation based on their recorded operating measurements. This is a machine-failure **classification** portfolio exercise, not an operational asset-monitoring system.

## 2. Data provenance and quality
Input: UCI AI4I 2020 synthetic dataset, preserved verbatim at `data/raw/ai4i2020.csv`. Inspection of the uploaded file: **10,000 rows × 14 columns**, with **339 positive labels** (3.39%), 9,661 negative labels and no missing values. The observations do not form a genuine chronological sequence. An identifier is not assumed to represent a unique real machine.

## 3. Method
Allowed inputs: product Type and five operating measurements. `UDI`, `Product ID` and failure-mode columns (`TWF`, `HDF`, `PWF`, `OSF`, `RNF`) are excluded to avoid identifier dependence and target leakage. A stratified random 80/20 split is produced using seed 42. A pipeline fits median imputation and one-hot encoding **only on training data**, then a Random Forest with imbalance-aware class weights. XGBoost is an opt-in inner-validation comparison, not an automatic deployment-model replacement.

## 4. Evaluation and findings
**Executed Random Forest hold-out (2,000 synthetic records, 68 positive):** precision **0.8462**, recall **0.6471**, F1 **0.7333**, ROC-AUC **0.9607**, average precision **0.7707**. Confusion matrix (rows actual 0/1, columns predicted 0/1): **[[1924, 8], [24, 44]]**. These values were produced by running `python -m src.evaluate` and are saved at `artifacts/evaluation_metrics.json`. Read `reports/figures/confusion_matrix.png`, `roc_curve.png`, and `precision_recall_curve.png` together with the scores; average precision is useful when failures are infrequent. Do not infer real-world sensitivity or economic return from synthetic hold-out measurements.

**Operational interpretation:** false negatives are failures that the classifier misses, potentially allowing avoidable investigation to be skipped; false positives trigger unnecessary inspection workload. Different maintenance settings imply different costs. A probability threshold of 0.50 is only an initial convention.

## 5. SQL and dashboard
The SQLite table represents dataset **observations**, with overall/type-level failure rates and sensor summaries. Power BI implementation is documented, not delivered as a `.pbix`. Source failure flags can support historical descriptive investigation but are not permitted as predictors.

## 6. Limitations and next steps
Synthetic generation; class imbalance; no time-order; no genuine equipment-level grouping; possible dependencies between rows; one hold-out partition; no external, prospective or temporal validation. No calibration, production drift or financial utility study. For a real deployment, collect time-stamped event histories, define failure horizon and machine identity, validate out of time and across assets, address label quality, tune thresholds on validation folds and establish operator oversight.
