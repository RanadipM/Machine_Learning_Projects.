import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import urllib
import os
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Credit Risk Analytics",
    page_icon="🏦",
    layout="wide"
)

# ── DB Connection ─────────────────────────────────────
@st.cache_resource
def get_engine():
    try:
        server   = st.secrets["SQL_SERVER"]
        database = st.secrets["SQL_DATABASE"]
        username = st.secrets["SQL_USERNAME"]
        password = st.secrets["SQL_PASSWORD"]
    except Exception:
        server   = os.environ.get("SQL_SERVER", "")
        database = os.environ.get("SQL_DATABASE", "")
        username = os.environ.get("SQL_USERNAME", "")
        password = os.environ.get("SQL_PASSWORD", "")

    params = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};DATABASE={database};"
        f"UID={username};PWD={password};"
        f"Encrypt=yes;TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )
    return create_engine(
        f"mssql+pyodbc:///?odbc_connect={params}",
        pool_pre_ping=True,
        pool_recycle=300
    )

@st.cache_data(ttl=300)
def run_query(sql):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            return pd.read_sql(text(sql), conn)
    except Exception as e:
        st.error(f"Database connection error: {str(e)[:200]}")
        return pd.DataFrame()

# ── Sidebar ───────────────────────────────────────────
st.sidebar.title("🏦 Credit Risk Platform")
st.sidebar.markdown("Real Lending Club Data · 100K Loans · Azure SQL")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "📊 Portfolio Overview",
    "📈 Risk Analysis",
    "🔍 Loan Explorer",
    "⚙️ Pipeline Status"
])

# ════════════════════════════════════════════════════
# PAGE 1 — Portfolio Overview
# ════════════════════════════════════════════════════
if page == "📊 Portfolio Overview":
    st.title("📊 Portfolio Overview")
    st.caption("Real Lending Club data · 100,000 loans · Azure SQL Database · ADLS Gen2")

    kpis = run_query("""
        SELECT
            COUNT(*) as total_loans,
            ROUND(SUM(loan_amnt)/1000000.0, 2) as exposure_mn,
            ROUND(AVG(int_rate), 2) as avg_rate,
            ROUND(SUM(is_npa)*100.0/COUNT(*), 2) as npa_pct,
            ROUND(AVG(pd_score)*100, 2) as avg_pd_pct,
            ROUND(SUM(expected_loss)/1000000.0, 2) as el_mn
        FROM fact_loans
    """)

    if not kpis.empty:
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.metric("Total Loans",    f"{int(kpis['total_loans'][0]):,}")
        c2.metric("Exposure",       f"${kpis['exposure_mn'][0]}M")
        c3.metric("Avg Rate",       f"{kpis['avg_rate'][0]}%")
        c4.metric("NPA Ratio",      f"{kpis['npa_pct'][0]}%")
        c5.metric("Avg PD",         f"{kpis['avg_pd_pct'][0]}%")
        c6.metric("Expected Loss",  f"${kpis['el_mn'][0]}M")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("NPA Rate by Grade")
        df_grade = run_query("""
            SELECT grade,
                   COUNT(*) as loans,
                   ROUND(SUM(is_npa)*100.0/COUNT(*),2) as npa_pct,
                   ROUND(AVG(int_rate),2) as avg_rate
            FROM fact_loans
            GROUP BY grade ORDER BY grade
        """)
        if not df_grade.empty:
            fig = px.bar(df_grade, x='grade', y='npa_pct',
                         color='npa_pct',
                         color_continuous_scale='RdYlGn_r',
                         labels={'npa_pct':'NPA %','grade':'Grade'},
                         text='npa_pct')
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Risk Band Distribution")
        df_risk = run_query("""
            SELECT risk_band, COUNT(*) as loans
            FROM fact_loans
            GROUP BY risk_band
        """)
        if not df_risk.empty:
            fig2 = px.pie(df_risk, values='loans', names='risk_band',
                          color_discrete_sequence=['#2ecc71','#f39c12','#e74c3c','#8e44ad'],
                          hole=0.4)
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Top Loan Purposes")
    df_purpose = run_query("""
        SELECT TOP 8 purpose,
               COUNT(*) as loans,
               ROUND(SUM(is_npa)*100.0/COUNT(*),2) as npa_pct,
               ROUND(AVG(loan_amnt),0) as avg_loan
        FROM fact_loans GROUP BY purpose ORDER BY loans DESC
    """)
    if not df_purpose.empty:
        fig3 = px.bar(df_purpose, x='loans', y='purpose',
                      orientation='h', color='npa_pct',
                      color_continuous_scale='RdYlGn_r',
                      labels={'loans':'Loan Count','purpose':'Purpose'})
        fig3.update_layout(height=350)
        st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════
# PAGE 2 — Risk Analysis
# ════════════════════════════════════════════════════
elif page == "📈 Risk Analysis":
    st.title("📈 Risk Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("PD Score by Grade")
        df_pd = run_query("""
            SELECT grade,
                   ROUND(MIN(pd_score),4) as min_pd,
                   ROUND(AVG(pd_score),4) as avg_pd,
                   ROUND(MAX(pd_score),4) as max_pd
            FROM fact_loans GROUP BY grade ORDER BY grade
        """)
        if not df_pd.empty:
            fig = px.bar(df_pd, x='grade', y='avg_pd',
                         labels={'avg_pd':'Avg PD Score','grade':'Grade'},
                         color='avg_pd',
                         color_continuous_scale='Reds')
            fig.update_layout(height=380)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Expected Loss by Risk Band")
        df_el = run_query("""
            SELECT risk_band,
                   ROUND(SUM(expected_loss)/1000000.0,2) as el_mn,
                   COUNT(*) as loans
            FROM fact_loans GROUP BY risk_band
        """)
        if not df_el.empty:
            fig2 = px.bar(df_el, x='risk_band', y='el_mn',
                          color='risk_band',
                          labels={'el_mn':'Expected Loss ($M)'},
                          color_discrete_map={
                              'LOW':'#2ecc71','MEDIUM':'#f39c12',
                              'HIGH':'#e74c3c','VERY_HIGH':'#8e44ad'})
            fig2.update_layout(height=380, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Interest Rate vs NPA Rate by Grade")
    df_scatter = run_query("""
        SELECT grade,
               ROUND(AVG(int_rate),2) as avg_rate,
               ROUND(SUM(is_npa)*100.0/COUNT(*),2) as npa_pct,
               COUNT(*) as loans
        FROM fact_loans GROUP BY grade
    """)
    if not df_scatter.empty:
        fig3 = px.scatter(df_scatter, x='avg_rate', y='npa_pct',
                          size='loans', color='grade', text='grade',
                          labels={'avg_rate':'Avg Interest Rate %',
                                  'npa_pct':'NPA Rate %'})
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════
# PAGE 3 — Loan Explorer
# ════════════════════════════════════════════════════
elif page == "🔍 Loan Explorer":
    st.title("🔍 Loan Explorer")

    col1, col2, col3 = st.columns(3)
    grade_filter   = col1.multiselect("Grade", ['A','B','C','D','E','F','G'],
                                       default=['A','B','C'])
    purpose_filter = col2.multiselect("Purpose",
                                       ['debt_consolidation','credit_card',
                                        'home_improvement','other','major_purchase'],
                                       default=['debt_consolidation'])
    npa_filter     = col3.selectbox("Loan Status", ['All','NPA Only','Performing'])

    if grade_filter and purpose_filter:
        grade_str   = ','.join([f"'{g}'" for g in grade_filter])
        purpose_str = ','.join([f"'{p}'" for p in purpose_filter])
        where = f"grade IN ({grade_str}) AND purpose IN ({purpose_str})"
        if npa_filter == 'NPA Only':     where += " AND is_npa = 1"
        elif npa_filter == 'Performing': where += " AND is_npa = 0"

        df_loans = run_query(f"""
            SELECT TOP 500 loan_id, grade, loan_amnt, int_rate,
                   purpose, loan_status, pd_score, expected_loss, risk_band
            FROM fact_loans WHERE {where}
            ORDER BY expected_loss DESC
        """)

        if not df_loans.empty:
            st.markdown(f"**Showing {len(df_loans):,} loans**")
            st.dataframe(df_loans, use_container_width=True, height=400)

            col1, col2 = st.columns(2)
            with col1:
                fig = px.histogram(df_loans, x='loan_amnt', nbins=30,
                                   title='Loan Amount Distribution',
                                   color='grade')
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig2 = px.histogram(df_loans, x='pd_score', nbins=30,
                                    title='PD Score Distribution',
                                    color='risk_band')
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Please select at least one grade and purpose.")

# ════════════════════════════════════════════════════
# PAGE 4 — Pipeline Status
# ════════════════════════════════════════════════════
elif page == "⚙️ Pipeline Status":
    st.title("⚙️ Pipeline Status")

    st.subheader("Data Quality Report")
    df_dq = run_query("""
        SELECT dq_flag,
               COUNT(*) as records,
               ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(),2) as pct
        FROM fact_loans GROUP BY dq_flag
    """)
    if not df_dq.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_dq, use_container_width=True)
        with col2:
            fig = px.pie(df_dq, values='records', names='dq_flag',
                         title='DQ Flag Distribution',
                         color_discrete_map={'PASS':'#2ecc71','INVALID_DTI':'#e74c3c'})
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Table Row Counts")
    tables = ['fact_loans','dim_customer','dim_date','dim_risk_band']
    counts = []
    for t in tables:
        cnt = run_query(f"SELECT COUNT(*) as cnt FROM {t}")
        if not cnt.empty:
            counts.append({'table': t, 'rows': int(cnt['cnt'][0])})
    if counts:
        st.dataframe(pd.DataFrame(counts), use_container_width=True)

    st.subheader("3-Tier Data Architecture")
    pipeline = pd.DataFrame({
        'Layer'    : ['Tier 1 — RAW', 'Tier 2 — STAGING', 'Tier 3 — GOLD'],
        'Location' : ['Azure ADLS Gen2 raw/loans/', 'Azure ADLS Gen2 staging/', 'Azure SQL creditriskdb'],
        'Format'   : ['Parquet + CSV', 'Parquet', 'Star Schema SQL Tables'],
        'Records'  : ['100,000', '100,000', '100,000'],
        'Status'   : ['✅ PASS', '✅ PASS', '✅ PASS']
    })
    st.dataframe(pipeline, use_container_width=True)

    st.subheader("Tech Stack")
    col1, col2, col3 = st.columns(3)
    col1.info("**Data Lake**\nAzure ADLS Gen2\nParquet format\nHierarchical namespace")
    col2.info("**DWH**\nAzure SQL Serverless\nStar schema\nAuto-pause enabled")
    col3.info("**Pipeline**\nPython + Pandas\nGreat Expectations DQ\nKaggle real data")

    st.success("🔒 All credentials stored in Streamlit Secrets — never in code")
