# 🏦 Credit Risk Analytics Platform

> **End-to-end production-grade credit risk system** built on Azure Cloud — combining Data Engineering, Machine Learning, and Full Stack development on 100,000 real Lending Club loans.

[![Streamlit App](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://machinelearningprojects-cbac76bk4yuzxkafjtcbz4.streamlit.app/)
[![Azure](https://img.shields.io/badge/Azure-Cloud-0089D6?style=for-the-badge&logo=microsoft-azure)](https://portal.azure.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📌 Project Overview

This platform demonstrates three professional roles in a single end-to-end system:

| Role | What Was Built |
|---|---|
| **Data Engineer** | Azure ADLS Gen2 data lake, Azure Functions ETL pipeline, ADF orchestration |
| **Data Scientist** | EDA, feature engineering, 4 ML models, SMOTE, PD scoring on 100K loans |
| **Full Stack Developer** | 5-page Streamlit dashboard with live Azure SQL backend, ML scoring UI |

**Business Problem:** Banks need to predict which loans will default (NPA) to price risk correctly, allocate capital, and minimize losses. This platform automates the full workflow from raw data ingestion to live ML-powered risk scoring.

---

## 🏗️ Architecture

```
Lending Club Dataset (100K loans)
        │
        ▼
┌─────────────────────────────────────────────────────┐
│                  Azure Data Lake Gen2                │
│   raw/  ──►  staging/  ──►  (validation complete)   │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│           Azure Functions (Python 3.11)              │
│  ingest_raw → transform_staging → load_gold          │
│  [Timer + HTTP triggers — Flex Consumption Plan]     │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│         Azure Data Factory (ADF)                     │
│  pl_credit_risk_etl — daily scheduled pipeline       │
│  Web Activity chain with success dependencies        │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│              Azure SQL Database                      │
│  fact_loans · dim_customer · dim_date · dim_risk_band│
│  Star schema — 100,000 rows · DQ flags               │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│         ML Pipeline (Google Colab)                   │
│  EDA → Feature Engineering (24 features) → SMOTE    │
│  Logistic Regression | Random Forest                 │
│  Gradient Boosting   | XGBoost                       │
│  Best: Random Forest ROC-AUC = 0.688                 │
└─────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────┐
│         Streamlit Dashboard (5 pages)                │
│  Portfolio Overview · Risk Analysis · Loan Explorer  │
│  🤖 ML Scoring · Pipeline Status                     │
│  Live on Streamlit Cloud — Azure SQL backend         │
└─────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

### 📊 Phase 1 — Data Engineering
- **ADLS Gen2** data lake with 3-layer medallion architecture (raw → staging → gold)
- **3 Azure Functions** (Python) with both Timer and HTTP triggers
  - `ingest_raw` — downloads and lands raw loan data
  - `transform_staging` — applies data quality checks and transformations
  - `load_gold` — loads star schema into Azure SQL
- **Azure Data Factory** pipeline orchestrating all 3 functions in sequence with daily schedule
- **Star schema** in Azure SQL: `fact_loans`, `dim_customer`, `dim_date`, `dim_risk_band`
- Data quality flagging (`PASS`/`FAIL`) on every record

### 🤖 Phase 2 — Machine Learning
- **Exploratory Data Analysis** — default rate by grade (5.3% → 51.7%), purpose, interest rate distributions
- **24 engineered features** including interaction terms, bins, and binary flags:
  - `int_rate_x_grade` (top feature), `int_rate_x_dti`, `loan_per_open_acc`
  - Outlier capping (DTI > 60, revol_util > 100)
  - Binary flags: `has_pub_rec`, `high_util`, `long_term`, `high_dti`
- **SMOTE** oversampling to handle 18% class imbalance → balanced 131K training samples
- **4 models trained and compared:**

| Model | ROC-AUC | PR-AUC | Default Recall |
|---|---|---|---|
| **Random Forest** 🏆 | **0.6883** | **0.3039** | **82%** |
| Gradient Boosting | 0.6870 | 0.3032 | 79% |
| XGBoost | 0.6857 | 0.3031 | 80% |
| Logistic Regression | 0.6155 | 0.2561 | 62% |

- **PD scores** generated for all 100,000 loans with risk flags (LOW / MEDIUM / HIGH)
- Portfolio expected loss: ₹73.4M total, ₹64.3M concentrated in HIGH risk band

### 🖥️ Phase 3 — Full Stack Dashboard

**5 interactive pages:**

1. **Portfolio Overview** — KPI metrics, NPA by grade, risk band distribution, purpose analysis
2. **Risk Analysis** — PD score trends, expected loss breakdown, interest rate vs NPA scatter
3. **Loan Explorer** — filterable table (grade, purpose, status) with distribution charts
4. **🤖 ML Scoring** — 
   - Single loan PD scorer with real-time gauge chart and risk drivers
   - Per-model deep dive: feature importance, confusion matrix, classification report
   - Model leaderboard with ROC-AUC comparison
5. **Pipeline Status** — ADF pipeline status, table counts, data quality metrics

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Cloud Platform** | Microsoft Azure |
| **Data Lake** | Azure Data Lake Storage Gen2 |
| **ETL Functions** | Azure Functions (Python 3.11, Flex Consumption) |
| **Orchestration** | Azure Data Factory (Web Activity pipeline) |
| **Database** | Azure SQL Database (mssql+pymssql) |
| **ML Framework** | scikit-learn, XGBoost, imbalanced-learn |
| **Data Processing** | pandas, numpy, scipy |
| **Visualization** | plotly, matplotlib, seaborn |
| **Dashboard** | Streamlit (deployed on Streamlit Cloud) |
| **Notebook** | Google Colab |
| **Version Control** | GitHub |

---

## 📁 Repository Structure

```
Credit_Risk_Analytics_Platform/
│
├── credit_risk_app.py          # Streamlit dashboard (5 pages)
├── requirements.txt            # Python dependencies
├── packages.txt                # System packages
├── startup.sh                  # Streamlit startup config
├── README.md                   # This file
│
├── notebooks/
│   └── credit_risk_ml.ipynb    # Full ML pipeline (Colab)
│
└── etl_functions/              # Azure Functions code
    ├── ingest_raw/
    │   └── __init__.py
    ├── transform_staging/
    │   └── __init__.py
    └── load_gold/
        └── __init__.py
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Azure subscription (Functions + SQL + ADLS)
- Streamlit account (for deployment)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/RanadipM/Machine_Learning_Projects.git
cd Machine_Learning_Projects/Credit_Risk_Analytics_Platform

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SQL_SERVER="your-server.database.windows.net"
export SQL_DATABASE="your-database"
export SQL_USERNAME="your-username"
export SQL_PASSWORD="your-password"

# Run the dashboard
streamlit run credit_risk_app.py
```

### Streamlit Secrets (for cloud deployment)
Create `.streamlit/secrets.toml`:
```toml
SQL_SERVER   = "creditriskserver-ran.database.windows.net"
SQL_DATABASE = "creditriskdb"
SQL_USERNAME = "creditriskadmin"
SQL_PASSWORD = "your-password"
```

---

## 📊 Key Results

| Metric | Value |
|---|---|
| Dataset | 100,000 Lending Club loans |
| Default Rate | 18.11% |
| Best Model | Random Forest |
| Best ROC-AUC | 0.6883 |
| Default Recall | 82% (at threshold=0.3) |
| Features Engineered | 24 |
| Total Expected Loss | $73.4M |
| HIGH Risk Expected Loss | $64.3M (87% concentration) |
| Grade A Default Rate | 5.3% |
| Grade G Default Rate | 51.7% |
| ADF Pipeline | Daily scheduled, 3-step chain |
| Azure Functions | 6 live (3 timer + 3 HTTP) |

---

## 💡 Business Insights

1. **Grade is the strongest predictor** — Grade G loans default at 10x the rate of Grade A
2. **Interest rate × grade interaction** is the #1 ML feature — high-rate loans in lower grades are disproportionately risky
3. **60.7% of loans fall in HIGH risk** band, concentrating 87% of expected losses
4. **Small business loans** have the highest default rate by purpose (26%)
5. **60-month term loans** are significantly riskier than 36-month loans

---

## 🎓 About

Built by **Ranadip Manna** — Data Scientist & AI Automation Engineer

- 🎓 M.Sc. Mathematics, RKMVCC | PGPDS, Praxis Business School (2025)
- 💼 Expertise: Python, SQL, ML, Azure, n8n, Power BI
- 🔗 [GitHub](https://github.com/RanadipM) | [LinkedIn](https://linkedin.com/in/ranadip-manna)

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

*⭐ If you found this project useful, please give it a star!*
