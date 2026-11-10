
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EconoCausal | Energy Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

RESULTS = Path(__file__).resolve().parent.parent / "results"

# =========================================================
# DATA
# =========================================================

@st.cache_data
def load_data(filename):
    path = RESULTS / filename
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

def number(value, digits=3):
    if pd.isna(value):
        return "N/A"
    return f"{value:,.{digits}f}"

def chart_style(fig, height=390):
    selected_theme = st.session_state.get(
        "eco_plot_template", "plotly_dark"
    )
    fig.update_layout(
        template=selected_theme,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=20, r=20, t=55, b=25),
        legend=dict(orientation="h", y=-0.2)
    )
    return fig

# =========================================================
# THEME
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

.stApp {
    background: #080f1c;
    color: #eaf2ff;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: #101827;
    border-right: 1px solid #26364d;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: #f2f7ff;
}

.hero {
    background: linear-gradient(115deg,#142c46,#173d53,#17243e);
    border: 1px solid #28516b;
    padding: 28px 32px;
    border-radius: 18px;
    margin: 4px 0 25px 0;
}

.eyebrow {
    color: #43d9ec;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 700;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    color: #f5f9ff;
    font-size: 36px;
    font-weight: 700;
    margin: 8px 0;
}

.hero-subtitle {
    color: #b8cadd;
    font-size: 14px;
}

.metric-card {
    background: linear-gradient(145deg,#172a40,#101d30);
    border: 1px solid #2a4059;
    border-radius: 15px;
    padding: 18px;
    min-height: 125px;
}

.metric-label {
    color: #9eb3ca;
    font-size: 11px;
    letter-spacing: 1px;
}

.metric-value {
    color: #f3f8ff;
    font-size: 27px;
    font-weight: 700;
    margin-top: 9px;
}

.metric-note {
    color: #48d9c0;
    font-size: 11px;
    margin-top: 5px;
}

.panel {
    background: #111e30;
    border: 1px solid #293e57;
    border-radius: 14px;
    padding: 18px;
}

.alert-card {
    background: #19263a;
    border: 1px solid #34445b;
    border-left: 4px solid #e7aa55;
    border-radius: 9px;
    padding: 13px;
    margin-bottom: 10px;
}

.recommendation-card {
    background: #142b32;
    border: 1px solid #285148;
    border-left: 4px solid #43d8b6;
    border-radius: 9px;
    padding: 13px;
    margin-bottom: 10px;
}

.small-muted {
    color: #93a9c1;
    font-size: 12px;
}

div[data-testid="stMetric"] {
    background: #15263b;
    border: 1px solid #293d56;
    border-radius: 12px;
    padding: 14px;
}

.stTabs [data-baseweb="tab"] {
    color: #b9c9dc;
}

.stTabs [aria-selected="true"] {
    color: #43d9ec;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD RESEARCH RESULTS
# =========================================================

comparison = load_data("phase1_phase2_comparison.csv")
phase1_models = load_data("phase1_final_model_comparison.csv")
hourly = load_data("phase1_hourly_consumption_summary.csv")
daily = load_data("phase1_daily_treatment_difference.csv")
signals = load_data("phase1_signal_type_summary.csv")
phase2_model = load_data("phase2_full_fe_regression.csv")
phase2_daily = load_data("phase2_daily_regression.csv")
regions = load_data("phase2_region_assignment_counts.csv")
robustness = load_data("phase2_robustness_temperature.csv")
validation = load_data("phase2_signal_schedule_validation.csv")
region_test = load_data("phase2_region_randomisation_test.csv")
survey_region = load_data("phase2_survey_coverage_by_region.csv")
survey_group = load_data("phase2_survey_coverage_by_assignment.csv")
randomisation = load_data("phase1_randomisation_test.csv")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    "<div style='font-size:27px;font-weight:700;color:#43d9ec;'>⚡ ECONOCAUSAL</div>",
    unsafe_allow_html=True
)
st.sidebar.caption("ENERGY INTELLIGENCE PLATFORM")
st.sidebar.divider()

pages = [
    "01 · Command Center",
    "02 · Consumption Intelligence",
    "03 · Causal Impact Lab",
    "04 · Regional Intelligence",
    "05 · Experiment Explorer"
]

page = st.sidebar.radio("NAVIGATION", pages, index=0)


# ECONOCAUSAL_THEME_SELECTOR
st.sidebar.divider()
st.sidebar.markdown("**APPEARANCE STUDIO**")
st.sidebar.markdown("🏙️ Metropolitan Dynamics")
st.sidebar.caption("Neutral charcoal · Warm grey · Elegant gold")

theme = {
    "bg": "#e9e7e3",
    "sidebar": "#d8d5d0",
    "surface": "#fbfaf7",
    "surface2": "#efede8",
    "text": "#292b2d",
    "muted": "#77746e",
    "accent": "#a58a4c",
    "accent2": "#c1ad79",
    "border": "#d0ccc2",
    "plot": "plotly_white"
}

st.session_state["eco_plot_template"] = theme["plot"]

st.markdown(f"""
<style>
:root {{
    --eco-bg: {theme['bg']};
    --eco-sidebar: {theme['sidebar']};
    --eco-surface: {theme['surface']};
    --eco-surface2: {theme['surface2']};
    --eco-text: {theme['text']};
    --eco-muted: {theme['muted']};
    --eco-accent: {theme['accent']};
    --eco-accent2: {theme['accent2']};
    --eco-border: {theme['border']};
}}

.stApp {{
    background: var(--eco-bg) !important;
    color: var(--eco-text) !important;
}}

[data-testid="stHeader"] {{
    background: var(--eco-bg) !important;
}}

[data-testid="stSidebar"] {{
    background: var(--eco-sidebar) !important;
    border-right: 1px solid var(--eco-border) !important;
}}

[data-testid="stSidebar"] * {{
    color: var(--eco-text);
}}

.stApp h1, .stApp h2, .stApp h3,
.stApp p, .stApp label,
.stApp [data-testid="stMarkdownContainer"] {{
    color: var(--eco-text);
}}

.hero {{
    background: linear-gradient(115deg,#fbfaf7,#e5e0d5) !important;
    border: 1px solid var(--eco-border) !important;
}}

.hero-title {{
    color: var(--eco-text) !important;
}}

.hero-subtitle {{
    color: var(--eco-muted) !important;
}}

.metric-card {{
    background: var(--eco-surface) !important;
    border: 1px solid var(--eco-border) !important;
}}

.metric-label {{
    color: var(--eco-muted) !important;
}}

.metric-value {{
    color: var(--eco-text) !important;
}}

.metric-note {{
    color: var(--eco-accent) !important;
}}

.alert-card, .recommendation-card, .panel {{
    background: var(--eco-surface) !important;
    border-color: var(--eco-border) !important;
}}

div[data-testid="stMetric"] {{
    background: var(--eco-surface) !important;
    border-color: var(--eco-border) !important;
}}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
    color: var(--eco-text) !important;
}}

.stButton button, .stDownloadButton button {{
    background: var(--eco-accent) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 8px !important;
}}

[data-baseweb="select"] > div {{
    background: var(--eco-surface) !important;
    border-color: var(--eco-border) !important;
}}

hr {{
    border-color: var(--eco-border) !important;
}}
</style>
""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("**RESEARCH ENVIRONMENT**")
st.sidebar.caption("iFlex Experimental Electricity Pricing")
st.sidebar.caption("Norway · 2020–2021")
st.sidebar.markdown(
    "<span style='color:#43d9ec;'>●</span> Research results connected",
    unsafe_allow_html=True
)
st.sidebar.divider()
st.sidebar.caption("ECONOCAUSAL RESEARCH PLATFORM")

# =========================================================
# COMMON HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <div class="eyebrow">IFLEX · EXPERIMENTAL ELECTRICITY PRICING</div>
    <div class="hero-title">EconoCausal</div>
    <div class="hero-subtitle">
        Electricity Price Impact Analyzer · Explore household consumption,
        experimental assignment and causal treatment effects.
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# PAGE 1 — COMMAND CENTER
# =========================================================

if page == "01 · Command Center":

    st.title("Energy Command Center")
    st.caption("A unified overview of the iFlex electricity pricing experiment.")

    p1_effect = 0.079155
    p1_pvalue = 0.481823
    p2_effect = -0.077289
    p2_pvalue = 0.164463

    if not comparison.empty:
        row1 = comparison[comparison["Phase"] == "Phase1"]
        row2 = comparison[comparison["Phase"] == "Phase2"]
        if not row1.empty:
            p1_effect = float(row1.iloc[0]["Treatment_Effect"])
            p1_pvalue = float(row1.iloc[0]["P_Value"])
        if not row2.empty:
            p2_effect = float(row2.iloc[0]["Treatment_Effect"])
            p2_pvalue = float(row2.iloc[0]["P_Value"])

    cards = [
        ("EXPERIMENTAL HOUSEHOLDS", "4,429", "Across both phases"),
        ("HOURLY OBSERVATIONS", "13.52M", "Household-hour records"),
        ("PHASE 1 EFFECT", f"{p1_effect:+.4f}", "kWh per hour"),
        ("PHASE 2 EFFECT", f"{p2_effect:+.4f}", "kWh per hour")
    ]

    cols = st.columns(4)
    for col, (label, value, note) in zip(cols, cards):
        with col:
            st.markdown(
                f"<div class='metric-card'><div class='metric-label'>{label}</div>"
                f"<div class='metric-value'>{value}</div>"
                f"<div class='metric-note'>{note}</div></div>",
                unsafe_allow_html=True
            )

    st.write("")
    left, right = st.columns([1.65, 1])

    with left:
        st.subheader("Treatment Effect Overview")

        if not comparison.empty:
            fig = px.bar(
                comparison,
                x="Phase",
                y="Treatment_Effect",
                color="Phase",
                text_auto=".4f",
                color_discrete_sequence=["#43d9ec", "#9b83ff"],
                title="Primary estimated treatment effects"
            )
            fig.add_hline(y=0, line_dash="dash", line_color="#e7aa55")
            fig.update_layout(showlegend=False, yaxis_title="Effect (kWh/hour)")
            st.plotly_chart(chart_style(fig), use_container_width=True)
        else:
            st.warning("Phase comparison file not found.")

    with right:
        st.subheader("Research Alerts")

        st.markdown(
            "<div class='alert-card'><b>Inference alert</b><br>"
            "Neither primary treatment estimate is statistically significant "
            "at the 5% level.</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div class='alert-card'><b>Regional assignment</b><br>"
            "Phase 2 assignment proportions differ across regions. "
            "Interpret regional comparisons carefully.</div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div class='alert-card'><b>Survey coverage</b><br>"
            "Phase 2 survey responses are limited and vary substantially "
            "by region.</div>",
            unsafe_allow_html=True
        )

    st.subheader("Consumption at a Glance")

    if not hourly.empty:
        selected = st.multiselect(
            "Choose Phase 1 household groups",
            sorted(hourly["Group_Phase1"].dropna().unique()),
            default=sorted(hourly["Group_Phase1"].dropna().unique()),
            key="command_groups"
        )
        view = hourly[hourly["Group_Phase1"].isin(selected)]
        fig = px.line(
            view, x="Hour", y="Demand_kWh",
            color="Group_Phase1", markers=True,
            color_discrete_sequence=["#43d9ec", "#9b83ff", "#48d9b5"],
            title="Average hourly electricity consumption"
        )
        fig.update_layout(xaxis_title="Hour of day", yaxis_title="Demand (kWh)")
        st.plotly_chart(chart_style(fig), use_container_width=True)

    st.subheader("Research Recommendations")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            "<div class='recommendation-card'><b>Compare phases</b><br>"
            "Investigate differences in treatment-effect estimates across "
            "the two experimental periods.</div>",
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            "<div class='recommendation-card'><b>Explore regions</b><br>"
            "Review regional assignment distributions and consumption "
            "patterns.</div>",
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            "<div class='recommendation-card'><b>Protect inference</b><br>"
            "Keep descriptive comparisons separate from causal estimates.</div>",
            unsafe_allow_html=True
        )

# =========================================================
# PAGE 2 — CONSUMPTION INTELLIGENCE
# =========================================================

elif page == "02 · Consumption Intelligence":

    st.title("Consumption Intelligence")
    st.caption("Explore observed household electricity consumption.")

    phase = st.selectbox("Experimental phase", ["Phase 1", "Phase 2"])

    if phase == "Phase 1":

        if not hourly.empty:
            groups = sorted(hourly["Group_Phase1"].dropna().unique())
            selected = st.multiselect(
                "Household groups",
                groups,
                default=groups
            )
            filtered = hourly[hourly["Group_Phase1"].isin(selected)]

            fig = px.line(
                filtered,
                x="Hour",
                y="Demand_kWh",
                color="Group_Phase1",
                markers=True,
                title="Average hourly consumption by group",
                color_discrete_sequence=["#43d9ec", "#9b83ff", "#48d9b5"]
            )
            st.plotly_chart(chart_style(fig), use_container_width=True)

            st.download_button(
                "Download hourly summary CSV",
                filtered.to_csv(index=False),
                "phase1_hourly_consumption.csv",
                "text/csv"
            )

        if not daily.empty:
            st.subheader("Daily Treatment-Control Difference")
            daily_view = daily.copy()
            daily_view["Date"] = pd.to_datetime(daily_view["Date"])
            fig = px.line(
                daily_view,
                x="Date",
                y="Difference",
                markers=True,
                title="Treatment minus control daily consumption",
                color_discrete_sequence=["#43d9ec"]
            )
            fig.add_hline(y=0, line_dash="dash", line_color="#e7aa55")
            st.plotly_chart(chart_style(fig), use_container_width=True)

            st.dataframe(daily_view, use_container_width=True, hide_index=True)

        if not signals.empty:
            st.subheader("Consumption by Price-Signal Type")
            fig = px.bar(
                signals,
                x="Price_signal",
                y="mean",
                color="Price_signal",
                hover_data=["count", "std", "median"],
                title="Observed average consumption by signal type"
            )
            st.plotly_chart(chart_style(fig), use_container_width=True)

    else:
        st.info(
            "Phase 2 hourly profile summaries have not yet been exported. "
            "The main Phase 2 causal results and daily model are available "
            "in the Causal Impact Lab. We will add an aggregated Phase 2 "
            "consumption profile without loading the full 12.18-million-row "
            "dataset into the dashboard."
        )

        if not phase2_daily.empty:
            st.subheader("Phase 2 Daily Regression Results")
            st.dataframe(phase2_daily, use_container_width=True, hide_index=True)

# =========================================================
# PAGE 3 — CAUSAL IMPACT LAB
# =========================================================

elif page == "03 · Causal Impact Lab":

    st.title("Causal Impact & Bootstrap Lab")
    st.caption("Inspect treatment estimates, uncertainty and model evidence.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Phase 1 Models",
        "Phase 2 Models",
        "Robustness",
        "Inference Diagnostics"
    ])

    with tab1:
        st.subheader("Phase 1 · Double Machine Learning")

        if not phase1_models.empty:
            st.dataframe(phase1_models, use_container_width=True, hide_index=True)

            model_choice = st.selectbox(
                "Choose a Phase 1 model",
                phase1_models["Model"].tolist()
            )
            row = phase1_models[phase1_models["Model"] == model_choice].iloc[0]

            st.metric(
                "Treatment effect",
                f"{row['Treatment_Effect']:+.5f} kWh/hour",
                f"p-value {row['P_Value']:.4f}"
            )

            fig = px.bar(
                phase1_models,
                x="Model",
                y="Treatment_Effect",
                color="Model",
                text_auto=".4f",
                title="Phase 1 model comparison"
            )
            fig.add_hline(y=0, line_dash="dash", line_color="#e7aa55")
            fig.update_layout(showlegend=False)
            st.plotly_chart(chart_style(fig), use_container_width=True)
        else:
            st.warning("Phase 1 model results are unavailable.")

    with tab2:
        st.subheader("Phase 2 · Full Fixed-Effects Regression")

        if not phase2_model.empty:
            st.dataframe(phase2_model, use_container_width=True, hide_index=True)

            treatment = phase2_model[
                phase2_model["Variable"] == "Treatment_Assigned"
            ]

            if not treatment.empty:
                row = treatment.iloc[0]
                st.metric(
                    "Hourly treatment effect",
                    f"{row['Coefficient']:+.5f} kWh/hour",
                    f"p-value {row['P_Value']:.4f}"
                )

        st.subheader("Secondary Daily Model")
        if not phase2_daily.empty:
            st.dataframe(phase2_daily, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Temperature Robustness")

        if not robustness.empty:
            st.dataframe(robustness, use_container_width=True, hide_index=True)

            if "Treatment_Coefficient" in robustness.columns:
                fig = px.bar(
                    robustness,
                    x="Model",
                    y="Treatment_Coefficient",
                    color="Model",
                    text_auto=".5f",
                    title="Treatment estimate across specifications"
                )
                fig.add_hline(y=0, line_dash="dash", line_color="#e7aa55")
                fig.update_layout(showlegend=False)
                st.plotly_chart(chart_style(fig), use_container_width=True)

            st.info(
                "The saved temperature robustness results show virtually "
                "identical treatment coefficients. Interpret this as the "
                "reported model comparison, not as independent confirmation."
            )

    with tab4:
        st.subheader("Randomization and Inference Diagnostics")

        if not randomisation.empty:
            st.markdown("**Phase 1 randomization inference**")
            st.dataframe(randomisation, use_container_width=True, hide_index=True)
        else:
            st.info("Phase 1 randomization-inference summary not found.")

        if not region_test.empty:
            st.markdown("**Phase 2 regional assignment test**")
            st.dataframe(region_test, use_container_width=True, hide_index=True)

        st.warning(
            "A non-significant estimate does not prove that the treatment "
            "had no effect. Confidence intervals and study design matter."
        )

    st.markdown("---")
    st.subheader("Bootstrap Lab · Current status")
    st.info(
        "The reference design includes an interactive bootstrap simulator. "
        "The saved primary model outputs do not contain bootstrap draws. "
        "We will add a genuine household-level bootstrap using the prepared "
        "Phase 1 analysis data, rather than displaying fabricated bootstrap "
        "distributions."
    )

# =========================================================
# PAGE 4 — REGIONAL INTELLIGENCE
# =========================================================


elif page == "04 · Regional Intelligence":

    st.title("Regional Intelligence")
    st.caption(
        "Geographic exploration of experimental household assignment "
        "across six Norwegian regions."
    )

    regions = load_data("phase2_region_assignment_counts.csv")

    if regions.empty:
        st.error("Regional assignment data could not be loaded.")
        st.stop()

    # Geographic coordinates of the six study-region cities.
    coordinates = {
        "Bergen": (60.3913, 5.3221),
        "Bodø": (67.2804, 14.4049),
        "Oslo": (59.9139, 10.7522),
        "Stavanger": (58.9700, 5.7331),
        "Tromsø": (69.6492, 18.9553),
        "Trondheim": (63.4305, 10.3951)
    }

    region_data = regions.copy()

    region_data["Total"] = (
        region_data["Control group"] +
        region_data["Price group"]
    )

    region_data["Price Share (%)"] = (
        region_data["Price group"] /
        region_data["Total"] * 100
    )

    region_data["Control Share (%)"] = (
        region_data["Control group"] /
        region_data["Total"] * 100
    )

    region_data["Latitude"] = region_data["Region"].map(
        lambda x: coordinates.get(x, (None, None))[0]
    )

    region_data["Longitude"] = region_data["Region"].map(
        lambda x: coordinates.get(x, (None, None))[1]
    )

    # -----------------------------------------------------
    # SEARCH AND FILTER
    # -----------------------------------------------------

    st.subheader("Explore Norwegian regions")

    search_col, filter_col = st.columns([1.5, 1])

    with search_col:
        search = st.text_input(
            "⌕ Search region",
            placeholder="Search Oslo, Bergen, Tromsø..."
        )

    with filter_col:
        sort_choice = st.selectbox(
            "Rank regions by",
            [
                "Price-group share",
                "Total households",
                "Price-group households"
            ]
        )

    filtered = region_data.copy()

    if search.strip():
        filtered = filtered[
            filtered["Region"].str.contains(
                search.strip(),
                case=False,
                na=False
            )
        ]

    if sort_choice == "Price-group share":
        filtered = filtered.sort_values(
            "Price Share (%)", ascending=False
        )
    elif sort_choice == "Total households":
        filtered = filtered.sort_values(
            "Total", ascending=False
        )
    else:
        filtered = filtered.sort_values(
            "Price group", ascending=False
        )

    if filtered.empty:
        st.warning("No matching region found. Try another search.")
        st.stop()

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    total_households = int(filtered["Total"].sum())
    total_price = int(filtered["Price group"].sum())
    total_control = int(filtered["Control group"].sum())

    overall_share = (
        total_price / total_households * 100
        if total_households else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("REGIONS", len(filtered))
    c2.metric("HOUSEHOLDS", f"{total_households:,}")
    c3.metric("PRICE GROUP", f"{total_price:,}")
    c4.metric("PRICE-GROUP SHARE", f"{overall_share:.1f}%")

    st.divider()

    # -----------------------------------------------------
    # GEOGRAPHIC MAP AND REGION PANEL
    # -----------------------------------------------------

    map_col, detail_col = st.columns([1.8, 1])

    with map_col:

        st.subheader("Norway · Regional assignment map")

        map_data = filtered.dropna(
            subset=["Latitude", "Longitude"]
        )

        if not map_data.empty:

            fig_map = px.scatter_geo(
                map_data,
                lat="Latitude",
                lon="Longitude",
                size="Total",
                color="Price Share (%)",
                text="Region",
                hover_name="Region",
                hover_data={
                    "Control group": True,
                    "Price group": True,
                    "Total": True,
                    "Price Share (%)": ":.1f",
                    "Latitude": False,
                    "Longitude": False
                },
                color_continuous_scale=[
                    "#243b55",
                    "#7466c9",
                    "#43d9ec"
                ],
                size_max=35,
                projection="mercator",
                title="Household assignment by study region"
            )

            fig_map.update_geos(
                scope="europe",
                center=dict(lat=64, lon=12),
                lataxis_range=[56, 72],
                lonaxis_range=[3, 32],
                showland=True,
                landcolor="#17283b",
                showocean=True,
                oceancolor="#0b1727",
                showcountries=True,
                countrycolor="#52647a",
                showcoastlines=True,
                coastlinecolor="#60758b",
                showframe=False,
                bgcolor="rgba(0,0,0,0)"
            )

            fig_map.update_traces(
                marker=dict(
                    line=dict(
                        color="#e5f5ff",
                        width=1
                    ),
                    opacity=0.9
                ),
                textposition="top center"
            )

            fig_map.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=560,
                margin=dict(l=0, r=0, t=45, b=0),
                font=dict(color="#e6f1ff"),
                coloraxis_colorbar=dict(
                    title="Price share (%)"
                )
            )

            st.plotly_chart(
                fig_map,
                use_container_width=True,
                config={"scrollZoom": True}
            )

            st.download_button(
                "⬇ Export interactive map (HTML)",
                data=fig_map.to_html(
                    include_plotlyjs="cdn"
                ),
                file_name="econocausal_norway_regional_map.html",
                mime="text/html"
            )

        else:
            st.warning("No geographic coordinates available for these results.")

    with detail_col:

        st.subheader("Regional explorer")

        selected_region = st.selectbox(
            "Select a region",
            filtered["Region"].tolist()
        )

        selected = filtered[
            filtered["Region"] == selected_region
        ].iloc[0]

        st.markdown(
            f"""
            <div style="
                background:#14263b;
                border:1px solid #344b66;
                border-radius:14px;
                padding:18px;
                margin-bottom:12px;
            ">
                <div style="color:#43d9ec;font-size:12px;">
                    SELECTED REGION
                </div>
                <div style="font-size:27px;font-weight:700;margin:8px 0;">
                    {selected_region}
                </div>
                <div style="color:#a9bdd1;font-size:12px;">
                    Phase 2 household assignment
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.metric(
            "Total households",
            f"{int(selected['Total']):,}"
        )

        st.metric(
            "Price-group households",
            f"{int(selected['Price group']):,}"
        )

        st.metric(
            "Control-group households",
            f"{int(selected['Control group']):,}"
        )

        st.metric(
            "Price-group share",
            f"{selected['Price Share (%)']:.1f}%"
        )

        st.progress(
            float(selected["Price Share (%)"]) / 100
        )

        st.caption(
            "The progress bar shows the proportion assigned "
            "to the experimental price group."
        )

    # -----------------------------------------------------
    # REGIONAL RANKINGS
    # -----------------------------------------------------

    st.divider()
    st.subheader("Regional comparison and rankings")

    rank_col, share_col = st.columns(2)

    with rank_col:

        ranking = filtered.sort_values(
            "Price Share (%)",
            ascending=False
        )

        fig_rank = px.bar(
            ranking,
            x="Price Share (%)",
            y="Region",
            orientation="h",
            text_auto=".1f",
            color="Price Share (%)",
            color_continuous_scale=[
                "#243b55",
                "#7466c9",
                "#43d9ec"
            ],
            title="Price-group share by region"
        )

        fig_rank.update_layout(
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False
        )

        st.plotly_chart(
            chart_style(fig_rank),
            use_container_width=True
        )

    with share_col:

        fig_groups = px.bar(
            filtered,
            x="Region",
            y=["Control group", "Price group"],
            barmode="group",
            title="Experimental group distribution",
            color_discrete_sequence=[
                "#9b83ff",
                "#43d9ec"
            ]
        )

        st.plotly_chart(
            chart_style(fig_groups),
            use_container_width=True
        )

    # -----------------------------------------------------
    # REGION LEADERBOARD
    # -----------------------------------------------------

    st.subheader("Regional leaderboard")

    highest = region_data.loc[
        region_data["Price Share (%)"].idxmax()
    ]

    lowest = region_data.loc[
        region_data["Price Share (%)"].idxmin()
    ]

    a, b = st.columns(2)

    with a:
        st.success(
            f"Highest price-group share: {highest['Region']} "
            f"({highest['Price Share (%)']:.1f}%)"
        )

    with b:
        st.info(
            f"Lowest price-group share: {lowest['Region']} "
            f"({lowest['Price Share (%)']:.1f}%)"
        )

    st.dataframe(
        filtered[
            [
                "Region",
                "Control group",
                "Price group",
                "Total",
                "Price Share (%)",
                "Control Share (%)"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇ Download regional data CSV",
        data=filtered.to_csv(index=False),
        file_name="econocausal_regional_intelligence.csv",
        mime="text/csv"
    )

    st.caption(
        "Research note: marker size represents household count; "
        "marker colour represents price-group assignment share. "
        "These are assignment statistics, not regional energy "
        "performance or consumption measurements."
    )



    # PAGE 5 — EXPERIMENT EXPLORER
# =========================================================

elif page == "05 · Experiment Explorer":

    st.title("Experiment & Research Explorer")
    st.caption("Explore the iFlex experiment, price signals and validation.")

    phase = st.radio(
        "Select experimental phase",
        ["Phase 1", "Phase 2"],
        horizontal=True
    )

    if phase == "Phase 1":
        start = "6 January 2020"
        end = "20 March 2020"
        note = "Phase 1 ended early because of COVID-19."
    else:
        start = "1 December 2020"
        end = "26 March 2021"
        note = "Phase 2 ran during winter 2020–2021."

    st.subheader("Experiment Timeline")

    timeline = pd.DataFrame({
        "Milestone": [
            "Experiment period begins",
            "Experimental price signals",
            "Experiment period ends"
        ],
        "Description": [
            start,
            "Scheduled price-group signal days",
            end
        ],
        "Stage": ["Start", "Treatment", "End"]
    })

    st.dataframe(timeline, use_container_width=True, hide_index=True)
    st.info(note)

    st.subheader("How the iFlex Experiment Worked")

    with st.expander("01 · Household assignment", expanded=True):
        st.write(
            "Participating households were assigned to experimental "
            "price groups or control groups. The official assignment "
            "variables are used for the main intention-to-treat analysis."
        )

    with st.expander("02 · Experimental price signals"):
        st.write(
            "Price-group households could receive experimental price "
            "signals on scheduled dates. Control households remained "
            "under normal, non-experimental pricing."
        )

    with st.expander("03 · Scheduling and notifications"):
        st.write(
            "Experiment days were selected approximately one week ahead "
            "using weather forecasts. Participants were notified one day "
            "before the scheduled experiment."
        )

    with st.expander("04 · Causal research method"):
        st.write(
            "The main causal analysis uses official group assignment "
            "rather than observed signal receipt. This estimates the "
            "intention-to-treat effect."
        )

    if phase == "Phase 1" and not signals.empty:
        st.subheader("Phase 1 Price-Signal Explorer")

        signal_names = sorted(signals["Price_signal"].dropna().unique())
        selected_signal = st.selectbox("Choose price signal", signal_names)

        signal_row = signals[
            signals["Price_signal"] == selected_signal
        ].iloc[0]

        x, y, z = st.columns(3)
        x.metric("Signal", selected_signal)
        y.metric("Observed records", f"{signal_row['count']:,.0f}")
        z.metric("Mean demand", f"{signal_row['mean']:.3f} kWh")

        st.dataframe(signals, use_container_width=True, hide_index=True)

    if phase == "Phase 2" and not validation.empty:
        st.subheader("Phase 2 Signal-Schedule Validation")
        st.dataframe(validation, use_container_width=True, hide_index=True)

    st.subheader("Research Files & Exports")

    export_files = [
        "phase1_phase2_comparison.csv",
        "phase1_final_model_comparison.csv",
        "phase2_full_fe_regression.csv",
        "phase2_daily_regression.csv",
        "phase2_region_assignment_counts.csv",
        "phase2_signal_schedule_validation.csv"
    ]

    for filename in export_files:
        path = RESULTS / filename
        if path.exists():
            with st.expander(filename):
                data = load_data(filename)
                st.dataframe(data, use_container_width=True, hide_index=True)
                st.download_button(
                    f"Download {filename}",
                    data=path.read_bytes(),
                    file_name=filename,
                    key=f"download_{filename}"
                )

# =========================================================
# FOOTER
# =========================================================

st.divider()
st.markdown(
    "<div style='text-align:center;color:#8195ad;font-size:12px;'>"
    "⚡ ECONOCAUSAL · ELECTRICITY PRICE IMPACT ANALYZER"
    "<br>iFlex Experimental Research · Norway · 2020–2021"
    "</div>",
    unsafe_allow_html=True
)
