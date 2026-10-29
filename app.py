"""
Food Order Prediction Using Data Mining
=======================================
A DWDM college project built with Streamlit, Pandas and Plotly.

Run from the project root with:
    streamlit run app.py

Expected project structure:
    app.py
    data/food_orders.csv
    output/order_prediction_model.pkl
    output/model_features.pkl
"""

import pickle
import time
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# 1. PAGE SETUP
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Food Order Prediction",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# 2. FILE PATHS (always relative to the folder that contains app.py)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "food_orders.csv"
MODEL_PATH = BASE_DIR / "output" / "order_prediction_model.pkl"
FEATURES_PATH = BASE_DIR / "output" / "model_features.pkl"

# ---------------------------------------------------------------------------
# 3. THEME COLOURS
# ---------------------------------------------------------------------------
ORANGE = "#FF7A18"
ORANGE_DARK = "#E85D04"
NAVY = "#0B1F3A"
NAVY_LIGHT = "#1B3A63"
CREAM = "#FFF6E9"
WHITE = "#FFFFFF"
# Colour sequence used by all charts
CHART_COLORS = [ORANGE, NAVY, "#FFB347", "#3C6E9F", "#F4A261", "#8FA9C7", "#D95D39", "#5C7A99"]

# Navigation labels (the emoji acts as the page icon)
PAGES = [
    "🏠 Home",
    "📈 Customer Insights",
    "🔮 Order Prediction",
    "🧮 Data Analysis",
    "ℹ️ About Project",
]

DISCLAIMER = (
    "⚠️ **Demo only:** the current prediction model was trained on **simulated data**. "
    "Its predictions are for demonstration and must not be treated as reliable real-world results."
)

# ---------------------------------------------------------------------------
# 4. CUSTOM CSS (gradient background, cards, buttons, sidebar)
# ---------------------------------------------------------------------------
CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Poppins', sans-serif;
}}

/* Page background: cream to soft orange gradient */
.stApp {{
    background: linear-gradient(135deg, {CREAM} 0%, #FFE8CC 55%, #FFD3A5 100%);
    color: {NAVY};
}}

/* Hide default Streamlit menu/footer for a cleaner demo */
#MainMenu, footer {{ visibility: hidden; }}

/* Make normal text navy so it is readable on the cream background */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp label,
.stApp span, .stApp li {{
    color: {NAVY};
}}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {NAVY} 0%, #12305A 100%);
}}
[data-testid="stSidebar"] * {{
    color: {CREAM} !important;
}}
.sidebar-brand {{
    text-align: center;
    padding: 10px 0 18px 0;
}}
.sidebar-brand .logo {{ font-size: 3rem; }}
.sidebar-brand .name {{ font-size: 1.15rem; font-weight: 700; color: {ORANGE} !important; }}
.sidebar-brand .tag {{ font-size: 0.8rem; opacity: 0.8; }}

/* Style the sidebar radio buttons like menu items */
[data-testid="stSidebar"] div[role="radiogroup"] > label {{
    background: rgba(255,255,255,0.06);
    padding: 12px 16px;
    border-radius: 14px;
    margin-bottom: 8px;
    transition: all 0.25s ease;
    cursor: pointer;
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
    background: rgba(255,122,24,0.35);
    transform: translateX(4px);
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {{
    background: linear-gradient(90deg, {ORANGE}, {ORANGE_DARK});
    box-shadow: 0 6px 16px rgba(255,122,24,0.4);
}}
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {{
    display: none;  /* hide the little radio circle */
}}

/* ---------- Hero banner ---------- */
.hero {{
    background: linear-gradient(120deg, {NAVY} 0%, {NAVY_LIGHT} 60%, {ORANGE_DARK} 140%);
    border-radius: 28px;
    padding: 48px 44px;
    box-shadow: 0 18px 40px rgba(11,31,58,0.28);
    margin-bottom: 26px;
}}
.hero h1 {{
    color: {WHITE} !important;
    font-size: 3rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    line-height: 1.15;
}}
.hero h1 span {{ color: {ORANGE} !important; }}
.hero p {{
    color: #E8EEF7 !important;
    font-size: 1.08rem;
    max-width: 760px;
    margin: 0;
}}

/* ---------- Page titles ---------- */
.page-title {{
    font-size: 2.2rem;
    font-weight: 800;
    color: {NAVY};
    margin-bottom: 0;
}}
.page-subtitle {{
    color: #4A5C75 !important;
    margin-bottom: 22px;
}}

/* ---------- KPI cards ---------- */
.kpi-card {{
    background: {WHITE};
    border-radius: 22px;
    padding: 22px 20px;
    box-shadow: 0 10px 26px rgba(11,31,58,0.10);
    border-left: 7px solid {ORANGE};
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}}
.kpi-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 16px 32px rgba(255,122,24,0.25);
}}
.kpi-icon {{ font-size: 2rem; }}
.kpi-label {{ font-size: 0.85rem; color: #5B6B82 !important; font-weight: 500; }}
.kpi-value {{ font-size: 1.9rem; font-weight: 800; color: {NAVY} !important; }}

/* ---------- Generic white info card ---------- */
.info-card {{
    background: {WHITE};
    border-radius: 22px;
    padding: 24px 26px;
    box-shadow: 0 10px 26px rgba(11,31,58,0.08);
    margin-bottom: 18px;
}}
.info-card h3 {{ margin-top: 0; }}

/* ---------- Warning banner ---------- */
.warn-box {{
    background: #FFF1D6;
    border: 1px solid {ORANGE};
    border-radius: 16px;
    padding: 14px 18px;
    margin: 10px 0 20px 0;
    color: {NAVY};
}}

/* ---------- Prediction result card ---------- */
.result-card {{
    border-radius: 26px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 18px 40px rgba(11,31,58,0.22);
    color: {WHITE};
}}
.result-yes {{ background: linear-gradient(135deg, #0B1F3A 0%, #1F6F54 130%); }}
.result-no  {{ background: linear-gradient(135deg, #0B1F3A 0%, #B5472B 130%); }}
.result-card .emoji {{ font-size: 3.2rem; }}
.result-card .headline {{ font-size: 1.7rem; font-weight: 800; color: {WHITE} !important; }}
.result-card .prob {{ font-size: 3.2rem; font-weight: 800; color: {ORANGE} !important; }}
.result-card .small {{ color: #D8E2F0 !important; font-size: 0.9rem; }}

/* ---------- Buttons ---------- */
.stButton > button, .stDownloadButton > button {{
    background: linear-gradient(90deg, {ORANGE}, {ORANGE_DARK});
    color: {WHITE} !important;
    border: none;
    border-radius: 999px;
    padding: 0.7rem 1.6rem;
    font-weight: 600;
    font-size: 1rem;
    box-shadow: 0 8px 18px rgba(255,122,24,0.35);
    transition: all 0.25s ease;
    width: 100%;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 12px 24px rgba(255,122,24,0.5);
    color: {WHITE} !important;
    border: none;
}}
.stButton > button p {{ color: {WHITE} !important; }}

/* ---------- Charts get rounded white cards ---------- */
div[data-testid="stPlotlyChart"] {{
    background: {WHITE};
    border-radius: 22px;
    padding: 10px;
    box-shadow: 0 10px 26px rgba(11,31,58,0.08);
}}

/* Dataframes with rounded corners */
div[data-testid="stDataFrame"] {{
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(11,31,58,0.08);
}}

/* Tabs */
.stTabs [data-baseweb="tab"] {{ font-weight: 600; }}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 5. HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def find_column(df, keywords):
    """Return the first column whose name contains any of the keywords
    (case-insensitive). Returns None if nothing matches.
    This lets the app work even if your column names are slightly different."""
    if df is None:
        return None
    for keyword in keywords:
        for col in df.columns:
            if keyword in str(col).lower().replace(" ", "_"):
                return col
    return None


@st.cache_data(show_spinner=False)
def load_data(path):
    """Load the CSV dataset. Returns (DataFrame or None, error message or None)."""
    if not Path(path).exists():
        return None, f"Dataset not found at `{path}`."
    try:
        return pd.read_csv(path), None
    except Exception as err:  # e.g. a corrupted file
        return None, f"Could not read the dataset: {err}"


@st.cache_resource(show_spinner=False)
def load_model_and_features(model_path, features_path):
    """Load the trained model and the list of feature names.
    Returns (model, features, error message)."""
    if not Path(model_path).exists():
        return None, None, f"Model file not found at `{model_path}`."
    if not Path(features_path).exists():
        return None, None, f"Feature file not found at `{features_path}`."
    try:
        # joblib is installed together with scikit-learn and reads most .pkl files
        try:
            import joblib
            model = joblib.load(model_path)
            features = joblib.load(features_path)
        except Exception:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
            with open(features_path, "rb") as f:
                features = pickle.load(f)
        if isinstance(features, str):
            features = [features]
        if features is None:
            raise ValueError("The saved model feature list is empty or invalid.")
        features = list(features)
        if not features:
            raise ValueError("The saved model feature list is empty.")
        return model, features, None
    except Exception as err:
        return None, None, f"Could not load the model files: {err}"


def prepare_data(df):
    """Clean the dataset and work out which column is which.
    Returns the cleaned DataFrame and a dictionary of detected columns."""
    df = df.copy()
    cols = {
        "order_id": find_column(df, ["order_id", "orderid", "order_no"]),
        "customer": find_column(df, ["customer_id", "customerid", "customer", "user"]),
        "amount": find_column(df, ["amount", "price", "total", "bill", "value", "spend"]),
        "status": find_column(df, ["status"]),
        "category": find_column(df, ["category", "cuisine", "food", "item"]),
        "payment": find_column(df, ["payment", "pay_"]),
        "date": find_column(df, ["order_date", "date", "time"]),
    }
    # Make the amount column numeric
    if cols["amount"]:
        df[cols["amount"]] = pd.to_numeric(df[cols["amount"]], errors="coerce")
    # Turn the date column into real dates (only if most values parse correctly)
    if cols["date"]:
        parsed = pd.to_datetime(df[cols["date"]], errors="coerce")
        if parsed.notna().mean() > 0.5:
            df[cols["date"]] = parsed
        else:
            cols["date"] = None
    return df, cols


def style_fig(fig, height=380):
    """Give every Plotly chart the same transparent, rounded, navy-text look."""
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins, sans-serif", color=NAVY),
        colorway=CHART_COLORS,
        margin=dict(l=20, r=20, t=60, b=20),
        title=dict(font=dict(size=17, color=NAVY)),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def kpi_card(icon, label, value):
    """Return the HTML for one summary card."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """


def page_header(title, subtitle):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)


def go_to(page_name):
    """Button callback: switch the sidebar page.
    Callbacks run before the page reloads, which is why changing the
    sidebar's state here is allowed."""
    st.session_state["page"] = page_name


def count_chart(df, column, title, kind="Bar"):
    """Make a bar or donut chart showing how many orders each value has."""
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "Orders"]
    if kind == "Donut":
        fig = px.pie(counts, names=column, values="Orders", hole=0.55, title=title,
                     color_discrete_sequence=CHART_COLORS)
        fig.update_traces(textposition="inside", textinfo="percent+label")
    else:
        fig = px.bar(counts, x=column, y="Orders", title=title, text="Orders",
                     color=column, color_discrete_sequence=CHART_COLORS)
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False)
    return style_fig(fig)


def map_feature_value(feature_name, previous_orders, avg_amount, days_since):
    """Match a model feature name to one of the three slider inputs.
    Returns None if the feature does not look like any of them."""
    name = feature_name.lower()
    if "day" in name or "since" in name or "recen" in name:
        return days_since
    if "amount" in name or "avg" in name or "average" in name or "price" in name:
        return avg_amount
    if "order" in name or "previous" in name or "count" in name or "freq" in name:
        return previous_orders
    return None


# ---------------------------------------------------------------------------
# 6. LOAD DATA + MODEL ONCE
# ---------------------------------------------------------------------------
raw_df, data_error = load_data(DATA_PATH)
model, model_features, model_error = load_model_and_features(MODEL_PATH, FEATURES_PATH)

if raw_df is not None:
    try:
        df, COLS = prepare_data(raw_df)
        if df.empty:
            data_error = "The dataset was loaded, but it contains no rows."
    except Exception as err:
        df, COLS = None, {}
        data_error = f"The dataset could not be prepared: {err}"
else:
    df, COLS = None, {}

# ---------------------------------------------------------------------------
# 7. SIDEBAR NAVIGATION
# ---------------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state["page"] = PAGES[0]

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="logo">🍔</div>
            <div class="name">FoodCast</div>
            <div class="tag">Food Order Prediction</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.radio("Navigate", PAGES, key="page", label_visibility="collapsed")
    st.markdown("---")
    # Small status indicators so you can see at a glance what loaded
    st.caption("System status")
    st.write("✅ Dataset loaded" if df is not None else "❌ Dataset missing")
    st.write("✅ Model loaded" if model is not None else "❌ Model missing")
    st.markdown("---")
    st.caption("DWDM College Project")

page = st.session_state["page"]


# ===========================================================================
# PAGE 1: HOME
# ===========================================================================
def show_home():
    st.markdown(
        """
        <div class="hero">
            <h1>Welcome to <span>Food Order Prediction</span> 🍕</h1>
            <p>Explore how customers order food, discover patterns in categories,
            payments and delivery status, and see how data mining can estimate
            whether a customer will place their next order.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Three navigation buttons
    b1, b2, b3 = st.columns(3)
    b1.button("🚀 Explore Dashboard", on_click=go_to, args=("📈 Customer Insights",))
    b2.button("🔮 Predict Next Order", on_click=go_to, args=("🔮 Order Prediction",))
    b3.button("📊 View Analytics", on_click=go_to, args=("🧮 Data Analysis",))

    st.write("")
    if df is None:
        st.error(f"{data_error} Place your CSV at `data/food_orders.csv` to see the summary cards.")
        st.markdown(f'<div class="warn-box">{DISCLAIMER}</div>', unsafe_allow_html=True)
        return

    # ---- Summary numbers ----
    total_orders = df[COLS["order_id"]].nunique() if COLS["order_id"] else len(df)
    customers = f"{df[COLS['customer']].nunique():,}" if COLS["customer"] else "N/A"
    avg_amount = f"₹{df[COLS['amount']].mean():,.2f}" if COLS["amount"] else "N/A"
    if COLS["status"]:
        delivered = int(df[COLS["status"]].astype(str).str.contains("deliver", case=False).sum())
        delivered = f"{delivered:,}"
    else:
        delivered = "N/A"

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi_card("🧾", "Total Orders", f"{total_orders:,}"), unsafe_allow_html=True)
    c2.markdown(kpi_card("👥", "Customers", customers), unsafe_allow_html=True)
    c3.markdown(kpi_card("💰", "Average Order Amount", avg_amount), unsafe_allow_html=True)
    c4.markdown(kpi_card("🛵", "Delivered Orders", delivered), unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown(
            """
            <div class="info-card">
                <h3>📌 What this project does</h3>
                <p>The app reads real food-order records, shows interactive charts about
                what people order and how they pay, and uses a trained classification model
                to estimate the chance of a repeat order from three simple inputs:
                previous orders, average order amount and days since the last order.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(f'<div class="warn-box">{DISCLAIMER}</div>', unsafe_allow_html=True)

    # Quick preview chart on the home page
    if COLS["category"]:
        st.plotly_chart(count_chart(df, COLS["category"], "Orders by Category"),
                        use_container_width=True)


# ===========================================================================
# PAGE 2: CUSTOMER INSIGHTS
# ===========================================================================
def reset_filters():
    """Callback for the 'Reset filters' button."""
    st.session_state["f_category"] = []
    st.session_state["f_status"] = []
    st.session_state["f_payment"] = []
    if "amt_range" in st.session_state:
        st.session_state["f_amount"] = st.session_state["amt_range"]


def show_insights():
    page_header("📈 Customer Insights", "Filter the real order data and explore ordering behaviour.")
    if df is None:
        st.error(f"{data_error}")
        return

    # ---- Filters ----
    st.markdown("##### 🎛️ Filters  _(leave a filter empty to include everything)_")
    f1, f2, f3 = st.columns(3)
    filtered = df.copy()

    if COLS["category"]:
        options = sorted(df[COLS["category"]].dropna().astype(str).unique())
        chosen = f1.multiselect("🍽️ Category", options, key="f_category")
        if chosen:
            filtered = filtered[filtered[COLS["category"]].astype(str).isin(chosen)]
    if COLS["status"]:
        options = sorted(df[COLS["status"]].dropna().astype(str).unique())
        chosen = f2.multiselect("📦 Order status", options, key="f_status")
        if chosen:
            filtered = filtered[filtered[COLS["status"]].astype(str).isin(chosen)]
    if COLS["payment"]:
        options = sorted(df[COLS["payment"]].dropna().astype(str).unique())
        chosen = f3.multiselect("💳 Payment method", options, key="f_payment")
        if chosen:
            filtered = filtered[filtered[COLS["payment"]].astype(str).isin(chosen)]

    if COLS["amount"] and df[COLS["amount"]].notna().any():
        lo, hi = float(df[COLS["amount"]].min()), float(df[COLS["amount"]].max())
        if lo < hi:
            st.session_state["amt_range"] = (lo, hi)
            amt = st.slider("💰 Order amount range", lo, hi, (lo, hi), key="f_amount")
            filtered = filtered[filtered[COLS["amount"]].between(amt[0], amt[1])]

    chart_style = st.radio("Chart style", ["Bar", "Donut"], horizontal=True)
    st.button("🔄 Reset filters", on_click=reset_filters)

    if filtered.empty:
        st.warning("No orders match these filters. Try removing a filter.")
        return

    st.success(f"Showing **{len(filtered):,}** of {len(df):,} orders.")

    # ---- Tabs for different views ----
    tab1, tab2, tab3 = st.tabs(["🍽️ Orders & Payments", "👥 Customer Patterns", "📅 Trends"])

    with tab1:
        c1, c2 = st.columns(2)
        if COLS["category"]:
            c1.plotly_chart(count_chart(filtered, COLS["category"], "Orders by Category", chart_style),
                            use_container_width=True)
        else:
            c1.info("No category column found in the dataset.")
        if COLS["status"]:
            c2.plotly_chart(count_chart(filtered, COLS["status"], "Order Status", chart_style),
                            use_container_width=True)
        else:
            c2.info("No status column found in the dataset.")

        c3, c4 = st.columns(2)
        if COLS["payment"]:
            c3.plotly_chart(count_chart(filtered, COLS["payment"], "Payment Methods", chart_style),
                            use_container_width=True)
        if COLS["amount"] and COLS["category"]:
            fig = px.box(filtered, x=COLS["category"], y=COLS["amount"],
                         title="Order Amount by Category", color=COLS["category"],
                         color_discrete_sequence=CHART_COLORS)
            fig.update_layout(showlegend=False)
            c4.plotly_chart(style_fig(fig), use_container_width=True)

    with tab2:
        if COLS["customer"]:
            per_customer = filtered.groupby(COLS["customer"]).agg(
                Orders=(COLS["customer"], "size"),
                **({"Total_Spent": (COLS["amount"], "sum")} if COLS["amount"] else {}),
            ).reset_index()

            c1, c2 = st.columns(2)
            fig = px.histogram(per_customer, x="Orders", title="How Many Orders Does Each Customer Place?",
                               color_discrete_sequence=[ORANGE])
            fig.update_layout(bargap=0.1, yaxis_title="Number of customers")
            c1.plotly_chart(style_fig(fig), use_container_width=True)

            if "Total_Spent" in per_customer.columns:
                fig = px.scatter(per_customer, x="Orders", y="Total_Spent", opacity=0.7,
                                 title="Orders vs Total Spend per Customer",
                                 color_discrete_sequence=[NAVY], hover_name=COLS["customer"])
                c2.plotly_chart(style_fig(fig), use_container_width=True)

            st.markdown("##### 🏆 Top 10 customers by number of orders")
            top10 = per_customer.sort_values("Orders", ascending=False).head(10)
            st.dataframe(top10, use_container_width=True, hide_index=True)
        else:
            st.info("No customer column found in the dataset, so customer patterns can't be shown.")

    with tab3:
        if COLS["date"]:
            dated = filtered.dropna(subset=[COLS["date"]]).copy()
            dated["Month"] = dated[COLS["date"]].dt.to_period("M").dt.to_timestamp()
            monthly = dated.groupby("Month").size().reset_index(name="Orders")
            fig = px.line(monthly, x="Month", y="Orders", markers=True, title="Orders per Month",
                          color_discrete_sequence=[ORANGE])
            st.plotly_chart(style_fig(fig), use_container_width=True)

            dated["Weekday"] = dated[COLS["date"]].dt.day_name()
            order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            weekday = dated["Weekday"].value_counts().reindex(order).reset_index()
            weekday.columns = ["Weekday", "Orders"]
            fig = px.bar(weekday, x="Weekday", y="Orders", title="Orders by Day of the Week",
                         color_discrete_sequence=[NAVY])
            st.plotly_chart(style_fig(fig), use_container_width=True)
        else:
            st.info("No usable date column was found, so trends can't be shown.")


# ===========================================================================
# PAGE 3: ORDER PREDICTION
# ===========================================================================
def show_prediction():
    page_header("🔮 Order Prediction", "Estimate whether a customer is likely to order again.")
    st.markdown(f'<div class="warn-box">{DISCLAIMER}</div>', unsafe_allow_html=True)

    if model is None:
        st.error(f"{model_error}")
        st.info("Save your trained model to `output/order_prediction_model.pkl` and the feature "
                "list to `output/model_features.pkl`, then refresh this page.")
        return

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown("##### 🧮 Customer details")
        previous_orders = st.slider("🧾 Number of previous orders", 0, 100, 10)
        avg_amount = st.number_input("💰 Average order amount (₹)", min_value=0.0,
                                     max_value=10000.0, value=350.0, step=10.0)
        days_since = st.slider("📅 Days since last order", 0, 365, 14)
        st.write("")
        predict_clicked = st.button("✨ Predict Now")

    with right:
        if not predict_clicked:
            st.markdown(
                """
                <div class="info-card" style="text-align:center;">
                    <div style="font-size:3rem;">🍜</div>
                    <h3>Your result will appear here</h3>
                    <p>Adjust the inputs on the left and press <b>Predict Now</b>.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        # Loading animation
        with st.spinner("🍳 Cooking up your prediction..."):
            time.sleep(1)

            # Build one row in exactly the order the model was trained on
            row, unmatched = {}, []
            for feature in model_features:
                value = map_feature_value(str(feature), previous_orders, avg_amount, days_since)
                if value is None:
                    # Unknown feature: use the dataset median if possible, otherwise 0
                    if df is not None and feature in df.columns and pd.api.types.is_numeric_dtype(df[feature]):
                        value = float(df[feature].median())
                    else:
                        value = 0
                    unmatched.append(str(feature))
                row[feature] = value
            input_df = pd.DataFrame([row], columns=model_features)

            try:
                prediction = model.predict(input_df)[0]
                probability = None
                if hasattr(model, "predict_proba"):
                    probabilities = model.predict_proba(input_df)[0]
                    classes = list(getattr(model, "classes_", range(len(probabilities))))
                    # Use the probability of the "positive" class (1 / True / Yes)
                    positive_index = len(classes) - 1
                    for i, cls in enumerate(classes):
                        if str(cls).lower() in ("1", "true", "yes", "will order"):
                            positive_index = i
                    probability = float(probabilities[positive_index])
            except Exception as err:
                st.error(f"The model could not make a prediction: {err}")
                st.caption(f"Features the model expects: {model_features}")
                return

        st.toast("Prediction ready!", icon="✅")

        # Decide on the wording of the result
        will_order = str(prediction).lower() in ("1", "true", "yes", "will order")
        css_class = "result-yes" if will_order else "result-no"
        emoji = "🎉" if will_order else "😴"
        headline = "Likely to order again" if will_order else "Unlikely to order soon"
        prob_text = f"{probability * 100:.1f}%" if probability is not None else "N/A"

        st.markdown(
            f"""
            <div class="result-card {css_class}">
                <div class="emoji">{emoji}</div>
                <div class="headline">{headline}</div>
                <div class="small">Estimated probability of a next order</div>
                <div class="prob">{prob_text}</div>
                <div class="small">Demo result from a model trained on simulated data</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Gauge chart for the probability
        if probability is not None:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=probability * 100,
                number={"suffix": "%", "font": {"color": NAVY}},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": ORANGE},
                    "steps": [
                        {"range": [0, 40], "color": "#FFE0CC"},
                        {"range": [40, 70], "color": "#FFD1A1"},
                        {"range": [70, 100], "color": "#CFE8DC"},
                    ],
                },
            ))
            st.plotly_chart(style_fig(gauge, height=260), use_container_width=True)

        if unmatched:
            st.caption("ℹ️ These model features are not one of the three inputs, so default values "
                       f"were used: {', '.join(unmatched)}")


# ===========================================================================
# PAGE 4: DATA ANALYSIS
# ===========================================================================
def show_analysis():
    page_header("🧮 Data Analysis", "Look inside the dataset and build your own charts.")
    if df is None:
        st.error(f"{data_error}")
        return

    tab1, tab2, tab3 = st.tabs(["📋 Data Explorer", "📊 Statistics", "🎨 Chart Builder"])

    with tab1:
        search = st.text_input("🔎 Search any text in the data", placeholder="e.g. Pizza, UPI, Delivered")
        view = df
        if search:
            mask = df.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
            view = df[mask]
        rows = st.slider("Rows to show", 5, 200, 25)
        st.caption(f"{len(view):,} matching rows")
        st.dataframe(view.head(rows), use_container_width=True)
        st.download_button("⬇️ Download data as CSV", view.to_csv(index=False).encode("utf-8"),
                           file_name="food_orders_filtered.csv", mime="text/csv")

    with tab2:
        c1, c2, c3 = st.columns(3)
        c1.markdown(kpi_card("📏", "Rows", f"{len(df):,}"), unsafe_allow_html=True)
        c2.markdown(kpi_card("🧱", "Columns", f"{df.shape[1]}"), unsafe_allow_html=True)
        c3.markdown(kpi_card("🕳️", "Missing values", f"{int(df.isna().sum().sum()):,}"),
                    unsafe_allow_html=True)
        st.write("")
        st.markdown("##### Summary statistics (numeric columns)")
        st.dataframe(df.describe().T, use_container_width=True)

        numeric = df.select_dtypes(include="number")
        if numeric.shape[1] >= 2:
            fig = px.imshow(numeric.corr(), text_auto=".2f", aspect="auto",
                            color_continuous_scale=["#0B1F3A", "#FFF6E9", "#FF7A18"],
                            title="Correlation Heatmap")
            st.plotly_chart(style_fig(fig, 460), use_container_width=True)

    with tab3:
        all_cols = list(df.columns)
        numeric_cols = list(df.select_dtypes(include="number").columns)
        c1, c2, c3 = st.columns(3)
        kind = c1.selectbox("Chart type", ["Histogram", "Bar (count)", "Box", "Scatter"])
        x_col = c2.selectbox("X column", all_cols)
        y_col = c3.selectbox("Y column (Box / Scatter)", numeric_cols if numeric_cols else all_cols)

        try:
            if kind == "Histogram":
                fig = px.histogram(df, x=x_col, color_discrete_sequence=[ORANGE])
            elif kind == "Bar (count)":
                counts = df[x_col].value_counts().head(20).reset_index()
                counts.columns = [x_col, "Count"]
                fig = px.bar(counts, x=x_col, y="Count", color_discrete_sequence=[NAVY])
            elif kind == "Box":
                fig = px.box(df, x=x_col, y=y_col, color_discrete_sequence=[ORANGE])
            else:
                fig = px.scatter(df, x=x_col, y=y_col, opacity=0.7, color_discrete_sequence=[NAVY])
            fig.update_layout(title=f"{kind}: {x_col}")
            st.plotly_chart(style_fig(fig, 460), use_container_width=True)
        except Exception as err:
            st.warning(f"That combination can't be plotted: {err}")


# ===========================================================================
# PAGE 5: ABOUT PROJECT
# ===========================================================================
def show_about():
    page_header("ℹ️ About Project", "Food Order Prediction Using Data Mining (DWDM)")

    st.markdown(
        """
        <div class="info-card">
            <h3>🎯 Objective</h3>
            <p>Use data warehousing and data mining techniques to understand customer food-ordering
            behaviour and to estimate whether a customer will place another order.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="info-card">
                <h3>🛠️ Technology</h3>
                <p>🐍 Python<br>🎈 Streamlit (web interface)<br>🐼 Pandas (data handling)<br>
                📊 Plotly (interactive charts)<br>🤖 Scikit-learn model (saved as .pkl)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="info-card">
                <h3>🔄 Workflow</h3>
                <p>1️⃣ Load and clean the order dataset<br>2️⃣ Explore patterns with charts<br>
                3️⃣ Train a prediction model<br>4️⃣ Serve predictions through this app</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("##### 🧠 Model information")
    if model is not None:
        st.write(f"**Model type:** `{type(model).__name__}`")
        st.write("**Features (in order):** " + ", ".join(f"`{f}`" for f in model_features))
    else:
        st.warning(model_error)

    st.markdown(
        f"""
        <div class="warn-box">
        <b>Important note on the model</b><br>
        {DISCLAIMER}<br>
        The charts on the Customer Insights and Data Analysis pages use the actual dataset
        in <code>data/food_orders.csv</code>.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# 8. SHOW THE SELECTED PAGE
# ---------------------------------------------------------------------------
if page == "🏠 Home":
    show_home()
elif page == "📈 Customer Insights":
    show_insights()
elif page == "🔮 Order Prediction":
    show_prediction()
elif page == "🧮 Data Analysis":
    show_analysis()
else:
    show_about()