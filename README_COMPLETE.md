# Revenue Leakage Intelligence Platform for Hospitals

## 1. Executive Summary
This project is an end-to-end healthcare revenue intelligence platform that converts raw hospital claim data into actionable financial decisions.

It combines:
- KPI analytics for leakage visibility
- Machine learning for claim denial risk
- Time-series forecasting for future revenue
- Anomaly detection for suspicious billing patterns
- A Streamlit dashboard for role-based decision support

The goal is to help hospitals reduce revenue leakage, improve claim realization, and make finance operations proactive instead of reactive.

## 2. Storyline: From Claim Event to Financial Action
### The business story
A patient visit creates a claim. The claim passes through coding, billing, and payer validation. At each stage, small issues can cause financial leakage:
- under-coding
- documentation delays
- payer denial patterns
- mismatch between expected and realized revenue

When thousands of claims pass through this cycle, leakage compounds into a major financial problem.

### The platform story
This system follows the full lifecycle:
1. Ingest claim-level financial and operational data.
2. Engineer features that represent revenue risk and process quality.
3. Train and run predictive models to identify denial and anomaly risk.
4. Forecast near-term revenue trends for planning.
5. Surface insights in dashboards for different hospital stakeholders.

### Decision storyline by role
- Finance teams monitor leakage, AR behavior, and monthly revenue trend.
- Analysts investigate model outputs and segment risk by departments and payer groups.
- Department leaders track profitability and operational leakage indicators.
- Executives use aggregated KPIs to prioritize interventions.

## 3. Problem Statement
Hospitals often face hidden revenue loss due to:
- claim denials
- billing inconsistencies
- delayed documentation and collections
- inadequate forecasting of cash flow/revenue

Traditional static reporting identifies problems late. This platform introduces predictive and anomaly-aware monitoring to detect risk earlier.

## 4. Objectives
- Quantify revenue leakage using claim-level and aggregated KPIs.
- Predict claim denial probability and categorize risk levels.
- Forecast future revenue with statistical time-series modeling.
- Detect anomalous billing behavior for early audit triggers.
- Provide interactive dashboards for operational and leadership decisions.

## 5. Technical Architecture
### Layer 1: Data Layer
Input datasets are stored in `data/` and include claim-level records plus derived output tables.

Examples:
- `data/hospital_claims_60k_realistic_v2.csv`
- `data/feature_store.csv`
- `data/hospital_kpi_summary.csv`
- `data/revenue_forecast.csv`
- `data/anomaly_flags.csv`

### Layer 2: Data Preparation and Feature Engineering
Core tasks:
- Missing value handling
- Categorical encoding
- Date conversion
- Feature derivation for leakage and operational quality

Key script:
- `src/data_preprocessing.py`

### Layer 3: Analytics and ML Models
1. Revenue KPI and leakage analysis
- `src/revenue_kpi_analysis.py`
- `src/core_metrics.py`

2. Claim denial prediction (classification)
- `models/denial_prediction_model.py`
- Model family: Logistic Regression
- Metrics: Accuracy, Precision, Recall, F1, ROC-AUC

3. Revenue forecasting (time series)
- `src/revenue_forecasting_arima.py`
- Model family: ARIMA
- Metrics include MAPE and forecast output artifacts

4. Billing anomaly detection
- `src/anomaly_detection.py`
- Model family: Isolation Forest

### Layer 4: Insight and Visualization Layer
Dashboard views are separated by role in `src/dashboards/`:
- `admin_dashboard.py`
- `finance_dashboard.py`
- `analyst_dashboard.py`
- `department_dashboard.py`
- `doctor_dashboard.py`

### Layer 5: Access and Presentation Layer
- Main app entry: `src/dashboard.py`
- Authentication helpers: `src/auth/`
- Theme customization: `src/ui/theme.py`

## 6. Repository Structure
```text
revenue_leakage/
  data/                     # raw and generated analytics outputs
  models/                   # model training scripts and model artifacts
  src/
    auth/                   # login, user management, security utilities
    dashboards/             # role-specific Streamlit dashboards
    ui/                     # UI styling/theme utilities
    dashboard.py            # Streamlit application entry point
    data_preprocessing.py
    revenue_kpi_analysis.py
    revenue_forecasting_arima.py
    anomaly_detection.py
    core_metrics.py
  README.md
  README_COMPLETE.md
  requirements.txt
```

## 7. Data Products and Artifacts
Generated assets include:
- Feature store: `data/feature_store.csv`
- KPI summaries: `data/hospital_kpi_summary.csv`, `data/core_hospital_metrics.csv`
- Department performance: `data/department_profitability.csv`
- Denial model outputs: `models/denial_model_metrics.csv`, `models/denial_model_predictions.csv`
- Forecast outputs: `data/revenue_forecast.csv`, `data/forecast_model_metrics.csv`
- Anomaly outputs: `data/anomaly_flags.csv`, `data/anomaly_summary_metrics.csv`

## 8. Tech Stack
- Python
- pandas
- numpy
- scikit-learn
- statsmodels
- streamlit
- plotly
- joblib
- bcrypt
- sqlite3 (standard library for auth persistence)

## 9. Setup and Run
### Prerequisites
- Python 3.10+
- `pip`

### Installation
```bash
python -m venv v
source v/bin/activate
pip install -r requirements.txt
```

### Launch dashboard
```bash
streamlit run src/dashboard.py
```

### Typical script execution order
```bash
python src/data_preprocessing.py
python src/revenue_kpi_analysis.py
python models/denial_prediction_model.py
python src/revenue_forecasting_arima.py
python src/anomaly_detection.py
```

## 10. Key Business KPIs
Representative KPIs tracked across modules:
- Revenue leakage amount
- Leakage index
- Accounts receivable days
- Charge capture efficiency
- Denial risk distribution (low/medium/high)
- Revenue-at-risk indicators
- Forecast variance and trend consistency
- Anomaly prevalence by department/payer

## 11. Current Maturity
Implemented modules:
- Revenue leakage analytics
- Claim denial prediction
- Revenue forecasting
- Billing anomaly detection
- Multi-role dashboard integration

This establishes a complete baseline for predictive revenue integrity monitoring.

## 12. Roadmap
Potential next enhancements:
- MLOps pipeline for scheduled retraining and model monitoring
- Drift detection for denial/anomaly models
- Scenario planning and what-if simulation
- Real-time data ingestion from HIS/RCM systems
- Alerting workflows for high-risk claims and anomalies
- PostgreSQL or cloud data warehouse backend for production scale

## 13. Expected Outcomes
Operational impact targets:
- Reduced revenue leakage
- Better claim approval and reduced denial burden
- Improved visibility into department-level profitability
- More accurate short-term revenue planning
- Earlier detection of irregular billing behavior

## 14. Disclaimer
This repository appears to use realistic or synthetic hospital-like data for analytics and demonstration. Production deployment should include:
- strict access control
- PHI handling policies
- audit logging
- compliance review
