import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import os
import plotly.express as px

st.set_page_config(page_title="Credit Risk Analytics", page_icon="🏦", layout="wide")

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
    conn_str = f"mssql+pymssql://{username}:{password}@{server}/{database}?charset=utf8"
    return create_engine(conn_str, pool_pre_ping=True, pool_recycle=300)

@st.cache_data(ttl=300)
def run_query(sql):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            return pd.read_sql(text(sql), conn)
    except Exception as e:
        st.error(f"Database error: {str(e)[:300]}")
        return pd.DataFrame()

st.sidebar.title("🏦 Credit Risk Platform")
st.sidebar.markdown("Real Lending Club Data · 100K Loans · Azure SQL")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["📊 Portfolio Overview","📈 Risk Analysis","🔍 Loan Explorer","⚙️ Pipeline Status"])

if page == "📊 Portfolio Overview":
    st.title("📊 Portfolio Overview")
    st.caption("Real Lending Club data · 100,000 loans · Azure SQL Database · ADLS Gen2")
    kpis = run_query("SELECT COUNT(*) as total_loans, ROUND(SUM(loan_amnt)/1000000.0,2) as exposure_mn, ROUND(AVG(int_rate),2) as avg_rate, ROUND(SUM(is_npa)*100.0/COUNT(*),2) as npa_pct, ROUND(AVG(pd_score)*100,2) as avg_pd_pct, ROUND(SUM(expected_loss)/1000000.0,2) as el_mn FROM fact_loans")
    if not kpis.empty:
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.metric("Total Loans", f"{int(kpis['total_loans'][0]):,}")
        c2.metric("Exposure", f"${kpis['exposure_mn'][0]}M")
        c3.metric("Avg Rate", f"{kpis['avg_rate'][0]}%")
        c4.metric("NPA Ratio", f"{kpis['npa_pct'][0]}%")
        c5.metric("Avg PD", f"{kpis['avg_pd_pct'][0]}%")
        c6.metric("Expected Loss", f"${kpis['el_mn'][0]}M")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("NPA Rate by Grade")
        df_grade = run_query("SELECT grade, COUNT(*) as loans, ROUND(SUM(is_npa)*100.0/COUNT(*),2) as npa_pct FROM fact_loans GROUP BY grade ORDER BY grade")
        if not df_grade.empty:
            fig = px.bar(df_grade, x='grade', y='npa_pct', color='npa_pct', color_continuous_scale='RdYlGn_r', text='npa_pct')
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Risk Band Distribution")
        df_risk = run_query("SELECT risk_band, COUNT(*) as loans FROM fact_loans GROUP BY risk_band")
        if not df_risk.empty:
            fig2 = px.pie(df_risk, values='loans', names='risk_band', hole=0.4)
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)
    st.subheader("Top Loan Purposes")
    df_p = run_query("SELECT TOP 8 purpose, COUNT(*) as loans, ROUND(SUM(is_npa)*100.0/COUNT(*),2) as npa_pct FROM fact_loans GROUP BY purpose ORDER BY loans DESC")
    if not df_p.empty:
        fig3 = px.bar(df_p, x='loans', y='purpose', orientation='h', color='npa_pct', color_continuous_scale='RdYlGn_r')
        fig3.update_layout(height=350)
        st.plotly_chart(fig3, use_container_width=True)

elif page == "📈 Risk Analysis":
    st.title("📈 Risk Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("PD Score by Grade")
        df_pd = run_query("SELECT grade, ROUND(AVG(pd_score),4) as avg_pd FROM fact_loans GROUP BY grade ORDER BY grade")
        if not df_pd.empty:
            fig = px.bar(df_pd, x='grade', y='avg_pd', color='avg_pd', color_continuous_scale='Reds')
            fig.update_layout(height=380)
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Expected Loss by Risk Band")
        df_el = run_query("SELECT risk_band, ROUND(SUM(expected_loss)/1000000.0,2) as el_mn FROM fact_loans GROUP BY risk_band")
        if not df_el.empty:
            fig2 = px.bar(df_el, x='risk_band', y='el_mn', color='risk_band', labels={'el_mn':'Expected Loss ($M)'})
            fig2.update_layout(height=380, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
    st.subheader("Interest Rate vs NPA Rate")
    df_s = run_query("SELECT grade, ROUND(AVG(int_rate),2) as avg_rate, ROUND(SUM(is_npa)*100.0/COUNT(*),2) as npa_pct, COUNT(*) as loans FROM fact_loans GROUP BY grade")
    if not df_s.empty:
        fig3 = px.scatter(df_s, x='avg_rate', y='npa_pct', size='loans', color='grade', text='grade')
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)

elif page == "🔍 Loan Explorer":
    st.title("🔍 Loan Explorer")
    col1, col2, col3 = st.columns(3)
    grades   = col1.multiselect("Grade", ['A','B','C','D','E','F','G'], default=['A','B','C'])
    purposes = col2.multiselect("Purpose", ['debt_consolidation','credit_card','home_improvement','other'], default=['debt_consolidation'])
    status   = col3.selectbox("Status", ['All','NPA Only','Performing'])
    if grades and purposes:
        gstr = ','.join([f"'{g}'" for g in grades])
        pstr = ','.join([f"'{p}'" for p in purposes])
        where = f"grade IN ({gstr}) AND purpose IN ({pstr})"
        if status == 'NPA Only': where += " AND is_npa=1"
        elif status == 'Performing': where += " AND is_npa=0"
        df_loans = run_query(f"SELECT TOP 500 loan_id,grade,loan_amnt,int_rate,purpose,loan_status,pd_score,expected_loss,risk_band FROM fact_loans WHERE {where} ORDER BY expected_loss DESC")
        if not df_loans.empty:
            st.dataframe(df_loans, use_container_width=True, height=400)
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(px.histogram(df_loans, x='loan_amnt', nbins=30, color='grade', title='Loan Amount Distribution'), use_container_width=True)
            with col2:
                st.plotly_chart(px.histogram(df_loans, x='pd_score', nbins=30, color='risk_band', title='PD Score Distribution'), use_container_width=True)

elif page == "⚙️ Pipeline Status":
    st.title("⚙️ Pipeline Status")
    st.subheader("Data Quality")
    df_dq = run_query("SELECT dq_flag, COUNT(*) as records, ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(),2) as pct FROM fact_loans GROUP BY dq_flag")
    if not df_dq.empty:
        col1, col2 = st.columns(2)
        with col1: st.dataframe(df_dq, use_container_width=True)
        with col2: st.plotly_chart(px.pie(df_dq, values='records', names='dq_flag'), use_container_width=True)
    st.subheader("Table Counts")
    counts = []
    for t in ['fact_loans','dim_customer','dim_date','dim_risk_band']:
        cnt = run_query(f"SELECT COUNT(*) as cnt FROM {t}")
        if not cnt.empty: counts.append({'table':t,'rows':int(cnt['cnt'][0])})
    if counts: st.dataframe(pd.DataFrame(counts), use_container_width=True)
    st.subheader("3-Tier Architecture")
    st.dataframe(pd.DataFrame({'Layer':['RAW','STAGING','GOLD'],'Location':['ADLS Gen2 raw/','ADLS Gen2 staging/','Azure SQL'],'Status':['✅','✅','✅']}), use_container_width=True)
    st.success("🔒 Credentials in Streamlit Secrets")
