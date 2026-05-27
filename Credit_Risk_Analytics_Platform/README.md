# Credit Risk Analytics Platform

## Architecture
RAW (ADLS Gen2) → Staging (Python ELT) → Gold (Azure SQL) → Streamlit Dashboard

## Tech Stack
- Azure ADLS Gen2 — data lake storage
- Azure SQL Database — serverless star schema DWH
- Python / Pandas — ELT pipeline
- Streamlit — interactive dashboard
- Plotly — visualizations
- Real Lending Club data — 100,000 loans

## Dashboard Pages
1. Portfolio Overview — KPIs, NPA by grade, risk distribution
2. Risk Analysis — PD distribution, expected loss, scatter plots
3. Loan Explorer — filterable loan table with charts
4. Pipeline Status — DQ report, table counts, layer status

## Setup
1. Set environment variables (see .env.template)
2. pip install -r requirements.txt
3. streamlit run app.py
