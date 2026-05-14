import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.optimize import minimize
from scipy.stats import norm, skew, kurtosis
from sklearn.covariance import LedoitWolf
from numpy.linalg import eigh
import warnings
warnings.filterwarnings('ignore')

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Portfolio Optimisation Dashboard",
    page_icon="📈",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'DM Serif Display', serif; }
.stApp { background: #0d1117; color: #e6edf3; }

section[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}

.metric-card {
    background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #58a6ff55; }
.metric-card .label { font-size: 11px; color: #7d8590; text-transform: uppercase; letter-spacing: 1.2px; }
.metric-card .value { font-size: 26px; font-weight: 600; color: #58a6ff; margin-top: 6px; }
.metric-card .sub   { font-size: 13px; color: #3fb950; margin-top: 4px; }

.section-header {
    background: linear-gradient(90deg, #1f6feb22, transparent);
    border-left: 3px solid #1f6feb;
    padding: 10px 16px;
    border-radius: 0 8px 8px 0;
    margin: 28px 0 16px 0;
    font-family: 'DM Serif Display', serif;
    font-size: 20px;
    color: #e6edf3;
}

.stDataFrame { border: 1px solid #30363d !important; border-radius: 8px; }

div[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px;
}
div[data-testid="stMetric"] label { color: #7d8590 !important; font-size: 12px !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #58a6ff !important; font-size: 22px !important; }
div[data-testid="stMetric"] div[data-testid="stMetricDelta"] { font-size: 13px !important; }

.stTabs [data-baseweb="tab-list"] { background: #161b22; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: #7d8590; border-radius: 8px; }
.stTabs [aria-selected="true"] { background: #1f6feb !important; color: white !important; }

.highlight-box {
    background: linear-gradient(135deg, #1f6feb15, #3fb95015);
    border: 1px solid #1f6feb44;
    border-radius: 12px;
    padding: 20px;
    margin: 12px 0;
}

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
}
.badge-green { background: #3fb95022; color: #3fb950; border: 1px solid #3fb95055; }
.badge-red   { background: #f8514922; color: #f85149; border: 1px solid #f8514955; }
.badge-blue  { background: #58a6ff22; color: #58a6ff; border: 1px solid #58a6ff55; }

.info-row {
    display: flex;
    gap: 12px;
    margin: 8px 0;
    flex-wrap: wrap;
}
</style>
""", unsafe_allow_html=True)

# ── Colour palette ────────────────────────────────────────────────────────────
DARK_BG  = "#0d1117"
CARD_BG  = "#161b22"
BORDER   = "#30363d"
BLUE     = "#58a6ff"
GREEN    = "#3fb950"
ORANGE   = "#d29922"
RED      = "#f85149"
PURPLE   = "#a371f7"
MUTED    = "#7d8590"
PALETTE  = [BLUE, GREEN, ORANGE, RED, PURPLE, "#ffa657", "#79c0ff", "#56d364",
            "#ff7b72", "#d2a8ff", "#f0883e", "#7ee787"]

plt.rcParams.update({
    "figure.facecolor":  DARK_BG,
    "axes.facecolor":    CARD_BG,
    "axes.edgecolor":    BORDER,
    "axes.labelcolor":   MUTED,
    "xtick.color":       MUTED,
    "ytick.color":       MUTED,
    "text.color":        "#e6edf3",
    "grid.color":        BORDER,
    "grid.linestyle":    "--",
    "grid.alpha":        0.4,
    "legend.facecolor":  CARD_BG,
    "legend.edgecolor":  BORDER,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

# ── Helper functions (aligned exactly with notebook) ──────────────────────────

def correlDist(corr):
    """Distance matrix based on correlation: 0 <= d[i,j] <= 1"""
    dist = ((1 - corr) / 2.) ** .5
    return dist

def getIVP(cov):
    """Inverse-Variance Portfolio weights"""
    ivp = 1. / np.diag(cov)
    ivp /= ivp.sum()
    return ivp

def getClusterVar(cov, cItems):
    """Compute variance per cluster"""
    cov_ = cov.loc[cItems, cItems]
    w_   = getIVP(cov_).reshape(-1, 1)
    return np.dot(np.dot(w_.T, cov_), w_)[0, 0]

def getQuasiDiag(link):
    """Sort clustered items by distance"""
    link = link.astype(int)
    sortIx = pd.Series([link[-1, 0], link[-1, 1]])
    numItems = link[-1, 3]
    while sortIx.max() >= numItems:
        sortIx.index = range(0, sortIx.shape[0] * 2, 2)
        df0 = sortIx[sortIx >= numItems]
        i = df0.index; j = df0.values - numItems
        sortIx[i] = link[j, 0]
        df0 = pd.Series(link[j, 1], index=i + 1)
        sortIx = pd.concat([sortIx, df0])
        sortIx = sortIx.sort_index()
        sortIx.index = range(sortIx.shape[0])
    return sortIx.tolist()

def getRecBipart(cov, sortIx):
    """Recursive bisection for HRP weights (FIXED for pandas compatibility)"""
    
    # ✅ Fix 1: use float instead of int
    w = pd.Series(1.0, index=sortIx)

    cItems = [sortIx]

    while len(cItems) > 0:
        cItems = [i[j:k] for i in cItems
                  for j, k in ((0, len(i)//2), (len(i)//2, len(i)))
                  if len(i) > 1]

        for i in range(0, len(cItems), 2):
            cVar0 = getClusterVar(cov, cItems[i])
            cVar1 = getClusterVar(cov, cItems[i+1])

            alpha = 1 - cVar0 / (cVar0 + cVar1)

            # ✅ Fix 2: replace inplace operation with .loc
            w.loc[cItems[i]]     = w.loc[cItems[i]] * alpha
            w.loc[cItems[i+1]]   = w.loc[cItems[i+1]] * (1 - alpha)

    return w

def getHRP(cov, corr):
    """Hierarchical Risk Parity — uses 'single' linkage (matches notebook)"""
    dist   = correlDist(corr)
    link   = sch.linkage(dist, 'single')   # NOTE: 'single' as in notebook
    sortIx = getQuasiDiag(link)
    sortIx = corr.index[sortIx].tolist()
    hrp    = getRecBipart(cov, sortIx)
    return hrp.sort_index()

def getMVP(cov):
    """
    Minimum Variance Portfolio via SLSQP (notebook Cell 45 — the final version).
    Long-only, fully invested.
    """
    n          = cov.shape[0]
    cov_matrix = cov.values

    def portfolio_variance(w):
        return w.T @ cov_matrix @ w

    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds      = tuple((0, 1) for _ in range(n))
    w0          = np.ones(n) / n
    result = minimize(
        portfolio_variance, w0, method='SLSQP',
        bounds=bounds, constraints=constraints,
        options={'ftol': 1e-12, 'maxiter': 1000}
    )
    weights = result.x
    return weights / weights.sum()

def getEigenPortfolio(cov):
    """Eigen Portfolio — dominant eigenvector, long-only (matches notebook Cell 44)"""
    eigenvalues, eigenvectors = eigh(cov.values)
    idx          = np.argsort(eigenvalues)[::-1]
    eigenvectors = eigenvectors[:, idx]
    vec          = eigenvectors[:, 0]
    weights      = np.abs(vec) / np.abs(vec).sum()
    return pd.Series(weights, index=cov.index)

def get_all_portfolios(returns):
    """Build all three portfolios from training returns (matches notebook Cell 45)"""
    cov, corr = returns.cov(), returns.corr()
    hrp   = getHRP(cov, corr)
    mvp   = pd.Series(getMVP(cov), index=cov.index)
    eigen = getEigenPortfolio(cov)
    return pd.DataFrame([mvp, hrp, eigen], index=['MVP', 'HRP', 'Eigen']).T

def jobson_korkie_test(r1, r2, rf=0.06):
    """Jobson-Korkie test for Sharpe ratio equality (matches notebook Cell 57)"""
    r1, r2 = r1 - rf / 252, r2 - rf / 252
    T       = len(r1)
    mean1, mean2 = np.mean(r1), np.mean(r2)
    std1,  std2  = np.std(r1),  np.std(r2)
    corr         = np.corrcoef(r1, r2)[0, 1]
    sr1, sr2     = mean1 / std1, mean2 / std2
    denom = np.sqrt((1 / T) * (2 * (1 - corr) + (sr1**2 + sr2**2 - 2 * sr1 * sr2 * corr)))
    z     = (sr1 - sr2) / denom
    return z, 2 * (1 - norm.cdf(abs(z)))

def ledoit_wolf_test(r1, r2, rf=0.06):
    """Ledoit-Wolf shrinkage Sharpe test (matches notebook Cell 61)"""
    r1, r2   = r1 - rf / 252, r2 - rf / 252
    T        = len(r1)
    combined = np.column_stack([r1, r2])
    lw       = LedoitWolf(); lw.fit(combined)
    lw_cov   = lw.covariance_
    mean1, mean2 = np.mean(r1), np.mean(r2)
    std1  = np.sqrt(lw_cov[0, 0]); std2  = np.sqrt(lw_cov[1, 1]); cov12 = lw_cov[0, 1]
    sr1, sr2 = mean1 / std1, mean2 / std2
    var_diff  = (1 / T) * ((std1**2 + std2**2 - 2 * cov12) / (std1**2 * std2**2))
    z         = (sr1 - sr2) / np.sqrt(var_diff)
    return z, 2 * (1 - norm.cdf(abs(z)))

def max_drawdown(returns_series):
    """Compute maximum drawdown from a return series"""
    cum        = (1 + returns_series).cumprod()
    roll_max   = cum.cummax()
    drawdown   = (cum - roll_max) / roll_max
    return drawdown.min()

def calmar_ratio(returns_series, ann_return):
    """Calmar = Ann.Return / |Max Drawdown|"""
    mdd = abs(max_drawdown(returns_series))
    return ann_return / mdd if mdd > 0 else np.nan

def sortino_ratio(returns_series, rf=0.06):
    """Sortino ratio using downside deviation"""
    excess     = returns_series - rf / 252
    downside   = excess[excess < 0].std() * np.sqrt(252)
    ann_excess = excess.mean() * 252
    return ann_excess / downside if downside > 0 else np.nan

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    uploaded = st.file_uploader("Upload Stock Prices CSV", type=["csv"])
    st.markdown("---")
    invested_amount = st.number_input(
        "💰 Investment Amount (₹)", min_value=10_000,
        max_value=10_00_00_000, value=10_00_000, step=10_000, format="%d"
    )
    years       = st.slider("📅 Horizon (Years)", 1, 20, 4)
    # Default 83 maps to 83% ≈ notebook's 83.35% — kept as slider
    train_split = st.slider("Train / Test Split (%)", 60, 90, 83, step=1)
    rf_rate     = st.number_input("📊 Risk-Free Rate (%)", min_value=0.0,
                                  max_value=15.0, value=6.0, step=0.5,
                                  help="Used in Sharpe / Sortino / stat tests") / 100
    st.markdown("---")
    st.markdown(f"**Invested:** ₹{invested_amount:,.0f}")
    st.markdown(f"**Horizon:** {years} yr  |  **RF:** {rf_rate*100:.1f}%")

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding: 30px 0 10px 0;'>
  <h1 style='font-size:42px; margin:0; background: linear-gradient(90deg, #58a6ff, #3fb950);
     -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
    Portfolio Optimisation Dashboard
  </h1>
  <p style='color:#7d8590; font-size:16px; margin-top:6px;'>
    MVP &nbsp;·&nbsp; HRP &nbsp;·&nbsp; Eigen Portfolio &nbsp;— Indian Equities
  </p>
</div>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, index_col=0, parse_dates=True)
    # Drop columns with >40% missing (matches notebook Cell 13)
    missing_fracs = df.isnull().mean().sort_values(ascending=False)
    drop_list = missing_fracs[missing_fracs > 0.4].index.tolist()
    if drop_list:
        df.drop(columns=drop_list, inplace=True)
    # Forward-fill (matches notebook Cell 15) — ffill() avoids deprecation warning
    df.ffill(inplace=True)
    return df

if uploaded is None:
    st.info("👈  Upload your **selected_stocks_prices.csv** in the sidebar to begin.", icon="📂")
    st.stop()

dataset   = load_data(uploaded)
row       = len(dataset)

# train_len: exact logic from notebook (int(row * 0.8335))
# When slider = 83, int(row * 0.83) — only differs by a few rows vs notebook default.
# We keep the slider for flexibility but compute consistently.
train_len = int(row * train_split / 100)

X_train         = dataset.iloc[:train_len]
X_test          = dataset.iloc[train_len:]
returns         = X_train.pct_change().dropna()    # matches notebook Cell 22
returns_test    = X_test.pct_change().dropna()

with st.spinner("Computing portfolios..."):
    portfolios          = get_all_portfolios(returns)   # matches notebook Cell 45

# Portfolio returns (matches notebook Cell 50 exactly)
Insample_Result    = pd.DataFrame(
    np.dot(returns,      np.array(portfolios)),
    columns=['MVP', 'HRP', 'Eigen'], index=returns.index)

OutOfSample_Result = pd.DataFrame(
    np.dot(returns_test, np.array(portfolios)),
    columns=['MVP', 'HRP', 'Eigen'], index=returns_test.index)

# Annualised metrics (matches notebook Cells 52-55)
ann_ret_in  = Insample_Result.mean()  * 252
ann_ret_oos = OutOfSample_Result.mean() * 252
sr_in       = (Insample_Result.mean()  * np.sqrt(252)) / Insample_Result.std()
sr_oos      = (OutOfSample_Result.mean() * np.sqrt(252)) / OutOfSample_Result.std()
vol_in      = Insample_Result.std()  * np.sqrt(252)
vol_oos     = OutOfSample_Result.std() * np.sqrt(252)

# Extra metrics
sortino_oos = {s: sortino_ratio(OutOfSample_Result[s], rf_rate) for s in ['MVP','HRP','Eigen']}
calmar_oos  = {s: calmar_ratio(OutOfSample_Result[s], ann_ret_oos[s]) for s in ['MVP','HRP','Eigen']}
mdd_oos     = {s: max_drawdown(OutOfSample_Result[s]) * 100 for s in ['MVP','HRP','Eigen']}

# ── SECTION 0: Dataset Overview ───────────────────────────────────────────────
with st.expander("🗂️ Dataset Overview", expanded=False):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Rows",     f"{row:,}")
    c2.metric("Stocks",         f"{len(dataset.columns)}")
    c3.metric("Training Rows",  f"{train_len:,}  ({train_split}%)")
    c4.metric("Testing Rows",   f"{row - train_len:,}  ({100-train_split}%)")
    st.dataframe(dataset.tail(5), use_container_width=True)

# ── SECTION 1: Investment Growth Calculator ───────────────────────────────────
st.markdown('<div class="section-header">💰 Investment Growth Calculator</div>', unsafe_allow_html=True)

best_strategy = ann_ret_oos.idxmax()
best_rate     = float(ann_ret_oos[best_strategy])

cols = st.columns(4)
for idx, strategy in enumerate(['MVP', 'HRP', 'Eigen']):
    rate   = float(ann_ret_oos[strategy])
    fv     = invested_amount * (1 + rate) ** years
    profit = fv - invested_amount
    with cols[idx]:
        st.markdown(f"""
        <div class="metric-card">
          <div class="label">{strategy} Portfolio</div>
          <div class="value">₹{fv:,.0f}</div>
          <div class="sub" style="color:{'#3fb950' if profit>=0 else '#f85149'}">
            {'▲' if profit>=0 else '▼'} ₹{abs(profit):,.0f} &nbsp;|&nbsp; {rate*100:.2f}% p.a.
          </div>
        </div>""", unsafe_allow_html=True)

with cols[3]:
    fv_best = invested_amount * (1 + best_rate) ** years
    st.markdown(f"""
    <div class="metric-card" style="border-color:#1f6feb88; background:linear-gradient(135deg,#1f6feb18,#161b22);">
      <div class="label">🏆 Best Strategy</div>
      <div class="value" style="color:#1f6feb;">{best_strategy}</div>
      <div class="sub">Highest OOS return · {best_rate*100:.2f}% p.a.</div>
      <div class="sub" style="color:#58a6ff;">₹{fv_best:,.0f} in {years} yr</div>
    </div>""", unsafe_allow_html=True)

# Growth chart with compound vs simple comparison
st.markdown(f"#### Projected Portfolio Growth — ₹{invested_amount:,.0f} over {years} years (compound)")
fig_growth, ax_growth = plt.subplots(figsize=(13, 4))
t = np.linspace(0, years, 300)
colors_growth = [BLUE, GREEN, ORANGE]
for i, strat in enumerate(['MVP', 'HRP', 'Eigen']):
    rate = float(ann_ret_oos[strat])
    fv_t = invested_amount * (1 + rate) ** t
    ax_growth.plot(t, fv_t, color=colors_growth[i], lw=2.5, label=strat)
    ax_growth.annotate(
        f"₹{invested_amount*(1+rate)**years:,.0f}",
        xy=(years, invested_amount*(1+rate)**years),
        fontsize=9, color=colors_growth[i], ha='right',
        xytext=(-6, 0), textcoords='offset points')
ax_growth.axhline(invested_amount, color=MUTED, linestyle='--', lw=1.2, alpha=0.6, label='Principal')
ax_growth.fill_between(t,
    invested_amount * (1 + float(ann_ret_oos.min())) ** t,
    invested_amount * (1 + float(ann_ret_oos.max())) ** t,
    alpha=0.06, color=GREEN, label='Strategy Range')
ax_growth.set_xlabel("Years"); ax_growth.set_ylabel("Portfolio Value (₹)")
ax_growth.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'₹{x/1e5:.1f}L'))
ax_growth.legend(loc='upper left'); ax_growth.grid(True)
fig_growth.tight_layout()
st.pyplot(fig_growth); plt.close(fig_growth)

# ── SECTION 2: Portfolio Weights ──────────────────────────────────────────────
st.markdown('<div class="section-header">🥧 Section 1 — Portfolio Weight Allocation</div>', unsafe_allow_html=True)

tab_pie, tab_bar, tab_treemap, tab_tbl = st.tabs(["  Pie Charts  ", "  Bar Chart  ", "  Treemap  ", "  Weights Table  "])

with tab_pie:
    fig_pie, axes = plt.subplots(1, 3, figsize=(18, 7))
    titles_colors = [("MVP", BLUE), ("HRP", GREEN), ("Eigen Portfolio", ORANGE)]
    for ax, (title, accent), col_idx in zip(axes, titles_colors, range(3)):
        weights = portfolios.iloc[:, col_idx].values
        labels  = [s.replace('.NS','') for s in portfolios.index.tolist()]
        # Only label slices > 2% to avoid clutter
        display_labels = [l if w > 0.02 else '' for l, w in zip(labels, weights)]
        wedges, texts, autotexts = ax.pie(
            weights, labels=display_labels, autopct=lambda p: f'{p:.1f}%' if p > 2 else '',
            startangle=140, explode=[0.04]*len(weights),
            colors=PALETTE[:len(weights)],
            wedgeprops=dict(edgecolor=DARK_BG, linewidth=1.5),
            textprops={'fontsize': 8, 'color': '#e6edf3'})
        for at in autotexts:
            at.set_color('white'); at.set_fontweight('bold'); at.set_fontsize(8)
        ax.set_title(title, fontsize=16, color=accent, pad=14)
    fig_pie.patch.set_facecolor(DARK_BG)
    fig_pie.tight_layout()
    st.pyplot(fig_pie); plt.close(fig_pie)

with tab_bar:
    fig_bar, ax_bar = plt.subplots(figsize=(15, 5))
    x = np.arange(len(portfolios.index)); w = 0.25
    for i, (strat, color) in enumerate(zip(['MVP','HRP','Eigen'], [BLUE, GREEN, ORANGE])):
        bars = ax_bar.bar(x + i*w, portfolios[strat].values * 100, w,
                          label=strat, color=color, alpha=0.88, edgecolor=DARK_BG)
        for bar in bars:
            h = bar.get_height()
            if h > 1.5:
                ax_bar.text(bar.get_x() + bar.get_width()/2, h + 0.2,
                            f'{h:.1f}%', ha='center', fontsize=7, color='#e6edf3')
    ax_bar.set_xticks(x + w)
    ax_bar.set_xticklabels([s.replace('.NS','') for s in portfolios.index],
                            rotation=38, ha='right', fontsize=9)
    ax_bar.set_ylabel("Weight (%)"); ax_bar.legend(); ax_bar.grid(axis='y')
    fig_bar.tight_layout(); st.pyplot(fig_bar); plt.close(fig_bar)

with tab_treemap:
    # Manual treemap using squarified rectangles approximation via bar patches
    fig_tm, axes_tm = plt.subplots(1, 3, figsize=(18, 5))
    for ax_t, (col_idx, strat, accent) in enumerate(zip(range(3), ['MVP','HRP','Eigen'], [BLUE, GREEN, ORANGE])):
        ax = axes_tm[ax_t]
        w  = portfolios.iloc[:, col_idx].sort_values(ascending=False)
        labels_tm = [s.replace('.NS','') for s in w.index]
        bars_tm   = ax.barh(range(len(w)), w.values * 100,
                            color=PALETTE[:len(w)], edgecolor=DARK_BG, height=0.8)
        for bar, lbl, val in zip(bars_tm, labels_tm, w.values):
            ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
                    f'{lbl}  {val*100:.1f}%', va='center', fontsize=8, color='#e6edf3')
        ax.set_yticks([]); ax.set_xlabel("Weight (%)")
        ax.set_title(strat, color=accent, fontsize=14)
        ax.set_xlim(0, w.values.max()*100 * 1.45)
        ax.grid(axis='x')
    fig_tm.patch.set_facecolor(DARK_BG)
    fig_tm.tight_layout(); st.pyplot(fig_tm); plt.close(fig_tm)

with tab_tbl:
    disp = portfolios.copy()
    disp.index = [s.replace('.NS','') for s in disp.index]
    # Show numeric and formatted side by side
    disp_pct = disp.applymap(lambda x: f"{x*100:.3f}%")
    st.dataframe(disp_pct, use_container_width=True)
    # Concentration metrics
    hhi = {s: (portfolios[s]**2).sum() for s in ['MVP','HRP','Eigen']}
    eff_n = {s: 1/hhi[s] for s in hhi}
    c1, c2, c3 = st.columns(3)
    for col, strat in zip([c1,c2,c3], ['MVP','HRP','Eigen']):
        col.metric(f"{strat} — Effective N", f"{eff_n[strat]:.1f}",
                   help="1/HHI — higher = more diversified")

# ── SECTION 3: Stock Price Trends ─────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Section 2 — Stock Price Trends</div>', unsafe_allow_html=True)

tab_norm, tab_raw = st.tabs(["  Normalised (Base=100)  ", "  Raw Prices  "])

with tab_norm:
    fig_prices, ax_prices = plt.subplots(figsize=(14, 5))
    for i, col in enumerate(dataset.columns):
        norm_prices = dataset[col] / dataset[col].iloc[0] * 100
        ax_prices.plot(norm_prices, lw=1.3, color=PALETTE[i % len(PALETTE)],
                       label=col.replace('.NS',''), alpha=0.85)
    ax_prices.axvline(dataset.index[train_len], color=RED, lw=1.8,
                      linestyle='--', label='Train/Test Split', alpha=0.9)
    ax_prices.fill_between(dataset.index[:train_len],
                           ax_prices.get_ylim()[0] if ax_prices.get_ylim()[0] < 0 else 0,
                           ax_prices.dataLim.y1,
                           alpha=0.03, color=BLUE)
    ax_prices.set_ylabel("Normalised Price (Base=100)")
    ax_prices.set_xlabel("Date")
    ax_prices.legend(fontsize=8, ncol=5, loc='upper left')
    ax_prices.grid(True)
    fig_prices.tight_layout(); st.pyplot(fig_prices); plt.close(fig_prices)

with tab_raw:
    selected_stock = st.selectbox("Select stock to view raw price:", dataset.columns.tolist())
    fig_raw, ax_raw = plt.subplots(figsize=(14, 4))
    ax_raw.plot(dataset.index, dataset[selected_stock],
                color=BLUE, lw=1.5, label=selected_stock.replace('.NS',''))
    ax_raw.axvline(dataset.index[train_len], color=RED, lw=1.5, linestyle='--', label='Split')
    ax_raw.set_ylabel("Price (₹)"); ax_raw.legend(); ax_raw.grid(True)
    fig_raw.tight_layout(); st.pyplot(fig_raw); plt.close(fig_raw)

# ── SECTION 4: Dendrogram ─────────────────────────────────────────────────────
st.markdown('<div class="section-header">🌲 Section 3 — Hierarchical Clustering Dendrogram</div>', unsafe_allow_html=True)

# Notebook Cell 29: linkage uses 'ward'; getHRP internally uses 'single' (different purposes)
dist_mat = correlDist(returns.corr())   # square distance matrix (matches notebook Cell 29)
link_mat  = linkage(dist_mat, 'ward')   # 'ward' for visualisation (matches notebook Cell 29)
fig_dend, ax_dend = plt.subplots(figsize=(14, 5))
dend_result = dendrogram(
    link_mat,
    labels=[s.replace('.NS','') for s in dataset.columns],
    leaf_font_size=11, ax=ax_dend,
    color_threshold=0.5 * max(link_mat[:, 2]),
    above_threshold_color=MUTED,
)
ax_dend.set_xlabel("Stocks"); ax_dend.set_ylabel("Distance (Ward)")
ax_dend.tick_params(axis='x', rotation=40)
ax_dend.grid(axis='y')
fig_dend.tight_layout(); st.pyplot(fig_dend); plt.close(fig_dend)

# ── SECTION 5: Correlation Heatmap ────────────────────────────────────────────
st.markdown('<div class="section-header">🔥 Section 4 — Correlation Heatmap</div>', unsafe_allow_html=True)

tab_heat_in, tab_heat_oos = st.tabs(["  In-Sample  ", "  Out-of-Sample  "])

for tab_heat, ret_df, label in [
        (tab_heat_in,  returns,      "In-Sample"),
        (tab_heat_oos, returns_test, "Out-of-Sample")]:
    with tab_heat:
        corr_mat = ret_df.corr()
        n_stocks = len(corr_mat)
        fig_sz   = max(8, n_stocks * 0.7)
        fig_heat, ax_heat = plt.subplots(figsize=(fig_sz, fig_sz * 0.7))
        cmap = mcolors.LinearSegmentedColormap.from_list("custom", [RED, CARD_BG, BLUE])
        im   = ax_heat.imshow(corr_mat.values, cmap=cmap, vmin=-1, vmax=1, aspect='auto')
        ticks = [s.replace('.NS','') for s in corr_mat.columns]
        ax_heat.set_xticks(range(len(ticks))); ax_heat.set_xticklabels(ticks, rotation=45, ha='right', fontsize=8)
        ax_heat.set_yticks(range(len(ticks))); ax_heat.set_yticklabels(ticks, fontsize=8)
        font_sz = max(5, 9 - n_stocks // 5)
        for i in range(len(ticks)):
            for j in range(len(ticks)):
                v = corr_mat.values[i, j]
                ax_heat.text(j, i, f"{v:.2f}", ha='center', va='center',
                             fontsize=font_sz,
                             color='white' if abs(v) > 0.5 else MUTED)
        plt.colorbar(im, ax=ax_heat, shrink=0.6, label="Correlation")
        ax_heat.set_title(f"Correlation Matrix — {label}", fontsize=13, pad=12)
        fig_heat.tight_layout(); st.pyplot(fig_heat); plt.close(fig_heat)

# ── SECTION 6: Cumulative Returns ─────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Section 5 — Cumulative Returns</div>', unsafe_allow_html=True)

col_in, col_oos = st.columns(2)
with col_in:
    st.markdown("#### 🏋️ In-Sample (Training Period)")
    fig_in, ax_in = plt.subplots(figsize=(7, 4))
    for strat, color in zip(['MVP','HRP','Eigen'], [BLUE, GREEN, ORANGE]):
        cum_ret = Insample_Result[strat].cumsum() * 100
        ax_in.plot(Insample_Result.index, cum_ret, color=color, lw=2, label=strat)
        ax_in.annotate(f"{cum_ret.iloc[-1]:.1f}%",
                       xy=(Insample_Result.index[-1], cum_ret.iloc[-1]),
                       xytext=(5, 0), textcoords='offset points',
                       fontsize=8, color=color)
    ax_in.axhline(0, color=MUTED, lw=0.8, linestyle='--')
    ax_in.set_ylabel("Cumulative Return (%)"); ax_in.legend(); ax_in.grid(True)
    fig_in.tight_layout(); st.pyplot(fig_in); plt.close(fig_in)

with col_oos:
    st.markdown("#### 🚀 Out-of-Sample (Testing Period)")
    fig_oos, ax_oos = plt.subplots(figsize=(7, 4))
    for strat, color in zip(['MVP','HRP','Eigen'], [BLUE, GREEN, ORANGE]):
        cum_ret = OutOfSample_Result[strat].cumsum() * 100
        ax_oos.plot(OutOfSample_Result.index, cum_ret, color=color, lw=2, label=strat)
        ax_oos.annotate(f"{cum_ret.iloc[-1]:.1f}%",
                        xy=(OutOfSample_Result.index[-1], cum_ret.iloc[-1]),
                        xytext=(5, 0), textcoords='offset points',
                        fontsize=8, color=color)
    ax_oos.axhline(0, color=MUTED, lw=0.8, linestyle='--')
    ax_oos.set_ylabel("Cumulative Return (%)"); ax_oos.legend(); ax_oos.grid(True)
    fig_oos.tight_layout(); st.pyplot(fig_oos); plt.close(fig_oos)

# ── SECTION 7: Risk–Return Metrics ────────────────────────────────────────────
st.markdown('<div class="section-header">📐 Section 6 — Risk–Return Metrics</div>', unsafe_allow_html=True)

m_cols = st.columns(3)
for idx, strat in enumerate(['MVP','HRP','Eigen']):
    colors_map = {'MVP': BLUE, 'HRP': GREEN, 'Eigen': ORANGE}
    color = colors_map[strat]
    with m_cols[idx]:
        st.markdown(f"<p style='color:{color}; font-weight:600; font-size:16px;'>{strat}</p>",
                    unsafe_allow_html=True)
        st.metric("Ann. Return (IS)",  f"{ann_ret_in[strat]*100:.2f}%",
                  delta=f"OOS: {ann_ret_oos[strat]*100:.2f}%")
        st.metric("Sharpe Ratio (IS)", f"{sr_in[strat]:.3f}",
                  delta=f"OOS: {sr_oos[strat]:.3f}")
        st.metric("Volatility (IS)",   f"{vol_in[strat]*100:.2f}%",
                  delta=f"OOS: {vol_oos[strat]*100:.2f}%")
        st.metric("Sortino (OOS)",     f"{sortino_oos[strat]:.3f}")
        st.metric("Max DD (OOS)",      f"{mdd_oos[strat]:.2f}%")
        st.metric("Calmar (OOS)",      f"{calmar_oos[strat]:.3f}")

# Comprehensive metric comparison chart
fig_rr, axes_rr = plt.subplots(2, 3, figsize=(16, 8))
metric_panels = {
    "Ann. Return OOS (%)":   ann_ret_oos * 100,
    "Sharpe OOS":            sr_oos,
    "Volatility OOS (%)":    vol_oos * 100,
    "Sortino OOS":           pd.Series(sortino_oos),
    "Max Drawdown OOS (%)":  pd.Series(mdd_oos),
    "Calmar OOS":            pd.Series(calmar_oos),
}
for ax_r, (metric_name, metric_vals) in zip(axes_rr.flatten(), metric_panels.items()):
    vals  = [metric_vals['MVP'], metric_vals['HRP'], metric_vals['Eigen']]
    bars  = ax_r.bar(['MVP','HRP','Eigen'], vals,
                     color=[BLUE, GREEN, ORANGE], edgecolor=DARK_BG, width=0.5)
    for bar, val in zip(bars, vals):
        ypos = bar.get_height() + (abs(bar.get_height()) * 0.03)
        ax_r.text(bar.get_x() + bar.get_width()/2, ypos,
                  f"{val:.2f}", ha='center', fontsize=10, color='#e6edf3')
    ax_r.set_title(metric_name, fontsize=11); ax_r.grid(axis='y')
    # Colour drawdown bars red since negative is bad
    if "Drawdown" in metric_name:
        for bar in bars: bar.set_color(RED)
fig_rr.patch.set_facecolor(DARK_BG)
fig_rr.tight_layout(); st.pyplot(fig_rr); plt.close(fig_rr)

# ── SECTION 8: Statistical Tests ─────────────────────────────────────────────
st.markdown('<div class="section-header">🧪 Section 7 — Statistical Significance Tests</div>', unsafe_allow_html=True)

pairs = [('MVP','HRP'), ('MVP','Eigen'), ('HRP','Eigen')]
rows  = []
for a, b in pairs:
    # Pass rf_rate from sidebar — matches notebook's rf=0.06 default but user-configurable
    jz, jp = jobson_korkie_test(OutOfSample_Result[a], OutOfSample_Result[b], rf=rf_rate)
    lz, lp = ledoit_wolf_test(OutOfSample_Result[a],   OutOfSample_Result[b], rf=rf_rate)
    rows.append({
        'Pair':           f'{a} vs {b}',
        'JK Z-Stat':      f"{jz:.4f}",
        'JK P-Value':     f"{jp:.4f}",
        'JK Significant': '✅ Yes' if jp < 0.05 else '❌ No',
        'LW Z-Stat':      f"{lz:.4f}",
        'LW P-Value':     f"{lp:.4f}",
        'LW Significant': '✅ Yes' if lp < 0.05 else '❌ No',
    })

test_df = pd.DataFrame(rows).set_index('Pair')
st.dataframe(test_df, use_container_width=True)
st.markdown("""
<div class='highlight-box' style='font-size:13px; color:#7d8590;'>
  <b style='color:#e6edf3;'>Interpretation:</b>&nbsp;
  Jobson-Korkie (JK) tests whether Sharpe ratio differences are statistically significant
  under the classical assumption. Ledoit-Wolf (LW) uses shrinkage covariance estimation for
  more robust inference. A p-value &lt; 0.05 indicates significance at the 95% level.
  Neither test finding significance means the strategies are statistically indistinguishable.
</div>
""", unsafe_allow_html=True)

# ── SECTION 9: Return Distribution & Drawdown ─────────────────────────────────
st.markdown('<div class="section-header">📉 Section 8 — Return Distribution & Drawdown</div>', unsafe_allow_html=True)

col_dist, col_dd = st.columns(2)

with col_dist:
    st.markdown("#### Daily Return Distribution (OOS)")
    fig_dist, ax_dist = plt.subplots(figsize=(7, 4))
    for strat, color in zip(['MVP','HRP','Eigen'], [BLUE, GREEN, ORANGE]):
        data_s = OutOfSample_Result[strat]
        ax_dist.hist(data_s, bins=40, alpha=0.5, color=color, label=strat, density=True)
        # Overlay KDE
        from scipy.stats import gaussian_kde
        kde = gaussian_kde(data_s)
        xs  = np.linspace(data_s.min(), data_s.max(), 200)
        ax_dist.plot(xs, kde(xs), color=color, lw=2)
    ax_dist.axvline(0, color=MUTED, lw=1, linestyle='--')
    ax_dist.set_xlabel("Daily Return"); ax_dist.set_ylabel("Density")
    ax_dist.legend(); ax_dist.grid(True)
    fig_dist.tight_layout(); st.pyplot(fig_dist); plt.close(fig_dist)

    # Distribution statistics table
    dist_stats = pd.DataFrame({
        strat: {
            'Mean (%)':     f"{OutOfSample_Result[strat].mean()*100:.4f}",
            'Std Dev (%)':  f"{OutOfSample_Result[strat].std()*100:.4f}",
            'Skewness':     f"{skew(OutOfSample_Result[strat]):.3f}",
            'Kurtosis':     f"{kurtosis(OutOfSample_Result[strat]):.3f}",
            'Min (%)':      f"{OutOfSample_Result[strat].min()*100:.3f}",
            'Max (%)':      f"{OutOfSample_Result[strat].max()*100:.3f}",
        }
        for strat in ['MVP','HRP','Eigen']
    })
    st.dataframe(dist_stats, use_container_width=True)

with col_dd:
    st.markdown("#### Maximum Drawdown (OOS)")
    fig_dd, ax_dd = plt.subplots(figsize=(7, 4))
    for strat, color in zip(['MVP','HRP','Eigen'], [BLUE, GREEN, ORANGE]):
        cum        = (1 + OutOfSample_Result[strat]).cumprod()
        roll_max   = cum.cummax()
        drawdown   = (cum - roll_max) / roll_max * 100
        ax_dd.fill_between(drawdown.index, drawdown, 0, alpha=0.35, color=color, label=strat)
        ax_dd.plot(drawdown.index, drawdown, color=color, lw=1.2)
        # Mark maximum drawdown point
        mdd_idx = drawdown.idxmin()
        ax_dd.scatter(mdd_idx, drawdown[mdd_idx], color=color, s=60, zorder=5)
        ax_dd.annotate(f"{drawdown[mdd_idx]:.1f}%", xy=(mdd_idx, drawdown[mdd_idx]),
                       xytext=(0, -14), textcoords='offset points',
                       fontsize=7, color=color, ha='center')
    ax_dd.axhline(0, color=MUTED, lw=0.8, linestyle='--')
    ax_dd.set_ylabel("Drawdown (%)"); ax_dd.legend(); ax_dd.grid(True)
    fig_dd.tight_layout(); st.pyplot(fig_dd); plt.close(fig_dd)

# ── SECTION 10: Rolling Metrics ───────────────────────────────────────────────
st.markdown('<div class="section-header">🔄 Section 9 — Rolling Metrics (OOS)</div>', unsafe_allow_html=True)

window = st.slider("Rolling Window (days)", 20, 120, 60, step=5)

tab_roll_sr, tab_roll_vol, tab_roll_ret = st.tabs([
    "  Rolling Sharpe  ", "  Rolling Volatility  ", "  Rolling Return  "])

with tab_roll_sr:
    fig_roll, ax_roll = plt.subplots(figsize=(14, 4))
    for strat, color in zip(['MVP','HRP','Eigen'], [BLUE, GREEN, ORANGE]):
        roll_sr = (OutOfSample_Result[strat].rolling(window).mean() * np.sqrt(252)) / \
                   OutOfSample_Result[strat].rolling(window).std()
        ax_roll.plot(roll_sr.index, roll_sr, color=color, lw=2, label=strat)
    ax_roll.axhline(0, color=MUTED, lw=1, linestyle='--')
    ax_roll.axhline(1, color=MUTED, lw=0.7, linestyle=':', alpha=0.5)
    ax_roll.set_ylabel(f"Rolling {window}-Day Sharpe"); ax_roll.legend(); ax_roll.grid(True)
    fig_roll.tight_layout(); st.pyplot(fig_roll); plt.close(fig_roll)

with tab_roll_vol:
    fig_rvol, ax_rvol = plt.subplots(figsize=(14, 4))
    for strat, color in zip(['MVP','HRP','Eigen'], [BLUE, GREEN, ORANGE]):
        rvol = OutOfSample_Result[strat].rolling(window).std() * np.sqrt(252) * 100
        ax_rvol.plot(rvol.index, rvol, color=color, lw=2, label=strat)
    ax_rvol.set_ylabel(f"Rolling {window}-Day Ann. Vol (%)"); ax_rvol.legend(); ax_rvol.grid(True)
    fig_rvol.tight_layout(); st.pyplot(fig_rvol); plt.close(fig_rvol)

with tab_roll_ret:
    fig_rret, ax_rret = plt.subplots(figsize=(14, 4))
    for strat, color in zip(['MVP','HRP','Eigen'], [BLUE, GREEN, ORANGE]):
        rret = OutOfSample_Result[strat].rolling(window).mean() * 252 * 100
        ax_rret.plot(rret.index, rret, color=color, lw=2, label=strat)
    ax_rret.axhline(0, color=MUTED, lw=1, linestyle='--')
    ax_rret.set_ylabel(f"Rolling {window}-Day Ann. Return (%)"); ax_rret.legend(); ax_rret.grid(True)
    fig_rret.tight_layout(); st.pyplot(fig_rret); plt.close(fig_rret)

# ── SECTION 11: Summary Scorecard ─────────────────────────────────────────────
st.markdown('<div class="section-header">🏆 Section 10 — Strategy Scorecard</div>', unsafe_allow_html=True)

scorecard = pd.DataFrame({
    'Ann. Return IS (%)':    (ann_ret_in  * 100).round(2),
    'Ann. Return OOS (%)':   (ann_ret_oos * 100).round(2),
    'Sharpe IS':             sr_in.round(3),
    'Sharpe OOS':            sr_oos.round(3),
    'Volatility IS (%)':     (vol_in  * 100).round(2),
    'Volatility OOS (%)':    (vol_oos * 100).round(2),
    'Sortino OOS':           pd.Series(sortino_oos).round(3),
    'Max DD OOS (%)':        pd.Series(mdd_oos).round(2),
    'Calmar OOS':            pd.Series(calmar_oos).round(3),
}).T
st.dataframe(scorecard.style.highlight_max(axis=1, color='#1f6feb33')
                            .highlight_min(axis=1, color='#f8514922'),
             use_container_width=True)

st.markdown("""
<div class='highlight-box' style='font-size:13px; color:#7d8590;'>
  <b style='color:#e6edf3;'>Legend:</b>&nbsp;
  <span class='badge badge-blue'>Blue highlight</span> = best value in row &nbsp;|&nbsp;
  <span class='badge badge-red'>Red highlight</span> = worst value in row. &nbsp;
  IS = In-Sample (training period) &nbsp;|&nbsp; OOS = Out-of-Sample (test period).
  All metrics computed from daily returns aligned with notebook calculations.
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border-color:#30363d; margin-top:48px;'>
<p style='text-align:center; color:#7d8590; font-size:12px;'>
  Portfolio Optimisation Dashboard &nbsp;·&nbsp; MVP &nbsp;·&nbsp; HRP &nbsp;·&nbsp; Eigen
  &nbsp;·&nbsp; Built with Streamlit
</p>
""", unsafe_allow_html=True)
