import json
import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Affordable Housing in Indian Cities",
    layout="wide",
)

GEO = "Exports/geospatial/"

# ── Header ────────────────────────────────────────────────────────────────────
st.title("Affordable Housing in Indian Cities and Market Impact - Case Study of Ahmedabad")
st.caption("Academic Project | Varun Phadke ")

# ── Acknowledgement ───────────────────────────────────────────────────────────
with st.expander("Acknowledgement"):
    st.write(
        """
        I would like to extend my sincerest gratitude to **Prof. Pennan Chinnasamy** and
        **Prof. Ashish Desai** for their unwavering support, guidance, and encouragement
        throughout this project.

        I would also like to thank my team members - Chintan Patel, Pawan Singh Ahirwar,  Sandeep Kadam
        """
    )

st.divider()

# ── Introduction ──────────────────────────────────────────────────────────────
st.header("Introduction")
st.write(
    """
Housing is identified as a basic human need, along with food and clothing. Housing is not merely
a shelter, but it comes with various amenities. These amenities are required to fulfill all kinds of
human needs at various levels. However, in the present scenario, the housing supply has failed to
fulfill the growing demand due to rapid urbanization. This **demand-supply mismatch has affected
all sections of society**, but the lowest section of the income pyramid bears the highest impact.

Therefore this study looks at the **PMAY-U** Scheme which provides affordable housing to the urban poor in India. The study aims to analyze the impact of affordable housing on local ward level property rates in Ahmedabad city, Gujarat. The study also looks at the overall impact of the PMAY-U scheme on the affordable housing segment in India.
    """
)

st.divider()

# ── Need Statement ────────────────────────────────────────────────────────────
st.header("Need Statement and Gaps")
col_a, col_b, col_c = st.columns(3)
col_a.warning(
    "**Population & Migration**\n\nRapid rural-to-urban migration intensifies demand "
    "for housing, causing overcrowding and inadequate living conditions."
)
col_b.warning(
    "**Infrastructure Strain**\n\nCities grapple with limited space, placing immense "
    "pressure on essential amenities like water and power."
)
col_c.warning(
    "**Affordability Gap**\n\nSoaring housing prices make homeownership elusive for "
    "low-income households — the dream of owning a home remains distant."
)

st.divider()

# ── Objectives ────────────────────────────────────────────────────────────────
st.header("Objectives")
st.markdown(
    """
    1. To study the **impact of the PMAY-U scheme** on the affordable housing segment.
    2. To provide **suggestions to the government** regarding future improvements in its
       policies relating to the affordable housing sector.
    3. Our main focus is on **Ahmedabad city** with granularity at the level of **wards**.
    """
)

st.divider()

# ── Study Area ────────────────────────────────────────────────────────────────
st.header("Study Area")
st.write(
    """
    This research project focuses on affordable housing in India, initially analyzing all Indian
    states using state-level data, then zooming into major Indian cities, and finally drilling
    down to **ward-level analysis in Ahmedabad**.
    """
)

sa1, sa2, sa3, sa4 = st.columns(4)
sa1.metric("States", "28")
sa2.metric("Cities (PMAY)", "9,500")
sa3.metric("Cities (Census)", "2,500")
sa4.metric("Cities (HPI)", "50")

st.divider()

# ── Methodology ───────────────────────────────────────────────────────────────
st.header("Methodology — Data Collection & Cleaning")
st.write(
    """
    A dataset of **2,646 cities** was compiled from Census Data 2011, and **8,868 data points**
    from the PMAY scheme database. Fuzzy matching identified **3,268 matching data points**;
    deduplication left **2,441 unique data points**.
    """
)

st.subheader("Data Cleaning Pipeline")
p1, _, p2, _, p3, _, p4 = st.columns([2, 1, 2, 1, 2, 1, 2])
p1.success("Census Datapoints\n\n**2,646**")
_.markdown("<div style='text-align:center;font-size:2rem;padding-top:1rem'>→</div>", unsafe_allow_html=True)
p2.info("PMAY Datapoints\n\n**8,868**")
_.markdown("")
p3.warning("After Fuzzy Matching\n\n**3,268**")
p4.success("After Deduplication\n\n**2,441**")

st.subheader("Data Sources")
data_table = pd.DataFrame(
    {
        "Explanatory Variable": [
            "Population in Slum Areas",
            "Number of Houses Sanctioned",
            "Housing Price Index",
            "Property Rates",
            "Ward-level Map of Ahmedabad",
        ],
        "Source": [
            "Census 2011",
            "PMAY-U Scheme Report",
            "Reserve Bank of India",
            "Online property listing websites (housing.com, MagicBricks)",
            "Ahmedabad Municipal Corporation (AMC)",
        ],
        "Challenges": [
            "Data time-interval was insufficient",
            "Data was not geolocated",
            "—",
            "Prices vary by society; average price per sq. ft. used",
            "Needed to add attributes from census",
        ],
    }
)
st.dataframe(data_table, width="stretch", hide_index=True)

st.divider()

# ── Analysis ──────────────────────────────────────────────────────────────────
st.header("Analysis")
st.write(
    """
    The assessment of affordable housing involves evaluating whether the existing supply meets
    demand. Slum prevalence provides a proxy for demand. At city level, ward-wise GIS mapping
    was done to identify slum pockets using a classification algorithm. Change in slum area was
    studied alongside current average property rates collected from property listing websites.
    """
)

s1, s2, s3 = st.columns(3)
s1.info("**Step 1 — Project Census 2011 Data**\n\nProject slum household data to 2021 using geometric projection and share-of-growth method.")
s2.info("**Step 2 — PMAY Supply Data**\n\nCapture housing units sanctioned under PMAY (target year 2022).")
s3.info("**Step 3 — Deficit / Surplus**\n\nCompare projected demand against PMAY supply to identify gaps.")

st.divider()

# ── AHDI ──────────────────────────────────────────────────────────────────────
st.header("Affordable Housing Deficit Index (AHDI) — City-Wise")
st.write("The city heat-map highlights deficit and surplus in affordable housing across 2,441 data points and reveals that **Tier 1 cities have not benefited from the scheme** to the extent enjoyed by Tier 2 and Tier 3 cities.")
st.latex(r"\text{AHDI} = \text{PMAY Sanctioned HH} - \text{Slum HH} \quad (\text{per location})")
st.info(
    "**Key Finding:** 24 states are experiencing deficits. "
    "**Maharashtra** exhibits the highest deficit, while **Gujarat** records the highest surplus "
    "among the 9 states in surplus."
)

st.divider()

# ── City-Wise Index ───────────────────────────────────────────────────────────
st.header("City-Wise Affordability Index")
st.write(
    """
    
    """
)
st.warning(
    "Note: PMAY scheme used demand generated by various States and UTs (validated by MoHUA) "
    "which remains short of actual housing shortage. The Ministry relied on States and urban "
    "local bodies to assess demand without imposing any ceiling."
)

# ── India PMAY Heatmap ────────────────────────────────────────────────────────
st.subheader("India PMAY — City-Level Housing Deficit Heatmap")
st.write(
    "Each of the **2,441 cities** is plotted by its Affordable Housing Deficit Index (AHDI). "
    "Heatmap intensity reflects the **magnitude of deficit** (cities where PMAY sanctioned "
    "housing falls short of slum households). Hover over circles for city-level details."
)

@st.cache_data
def load_pmay_cities():
    with open(GEO + "PMAY_Cities.geojson") as f:
        return json.load(f)

pmay_cities = load_pmay_cities()

india_map = folium.Map(location=[22.5, 80.5], zoom_start=5, tiles="CartoDB positron")

heat_points = [
    [
        f["properties"]["Latitude"],
        f["properties"]["Longitude"],
        min(1.0, max(0, -f["properties"]["Surplus"]) / 300000),
    ]
    for f in pmay_cities["features"]
    if f["properties"]["Surplus"] is not None
    and f["properties"]["Latitude"] is not None
    and f["properties"]["Surplus"] < 0
]
HeatMap(
    heat_points,
    name="Heatmap",
    radius=18,
    blur=22,
    min_opacity=0.3,
    gradient={0.2: "#ffffb2", 0.5: "#fd8d3c", 0.8: "#e31a1c", 1.0: "#67000d"},
).add_to(india_map)

deficit_fg = folium.FeatureGroup(name="Deficit cities", show=True)
surplus_fg = folium.FeatureGroup(name="Surplus cities", show=True)

for f in pmay_cities["features"]:
    p = f["properties"]
    if p["Latitude"] is None or p["Surplus"] is None:
        continue
    surplus = p["Surplus"]
    radius = max(3, min(14, abs(surplus) / 40000))
    color = "#d73027" if surplus < 0 else "#4575b4"
    tooltip_text = (
        f"<b>{p['City']}</b><br>"
        f"Slum HH: {p['Slum_HH']:,}<br>"
        f"PMAY HH: {p['PMAY.PMAY_HH']}<br>"
        f"{'Deficit' if surplus < 0 else 'Surplus'}: {abs(surplus):,}"
    )
    marker = folium.CircleMarker(
        location=[p["Latitude"], p["Longitude"]],
        radius=radius,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        weight=0.5,
        tooltip=folium.Tooltip(tooltip_text),
    )
    if surplus < 0:
        marker.add_to(deficit_fg)
    else:
        marker.add_to(surplus_fg)

deficit_fg.add_to(india_map)
surplus_fg.add_to(india_map)
folium.LayerControl(collapsed=False).add_to(india_map)

st_folium(india_map, width="100%", height=560, returned_objects=[])
st.caption(
    "Red circles = housing deficit (PMAY < slum HH) | "
    "Blue circles = surplus | Circle size ∝ magnitude | "
    "Heatmap intensity ∝ deficit depth"
)

st.divider()

# ── Property Appreciation ─────────────────────────────────────────────────────
st.header("Property Appreciation Index — Affordability")
st.write(
    """
    A linear regression analysis on RBI's House Price Index (HPI) against the Affordability
    Index shows a **positive correlation**: an increase in the presence of affordable housing
    is associated with increased prevalent market rates in the cities studied.
    """
)
st.info("Note: Tier-1 cities were excluded — market conditions there are exceptional.")

col_eq, col_stats = st.columns([1, 2])
with col_eq:
    st.subheader("Regression Equation")
    st.latex(r"Y = 322.45 \, X - 38047.19")
    st.markdown("**Y** — Appreciation in Property Value")
    st.markdown("**X** — Presence of Affordable Housing in the City")

with col_stats:
    st.subheader("Regression Statistics")
    reg_stats = pd.DataFrame(
        {
            "Statistic": [
                "Multiple R", "R Square", "Adjusted R Square",
                "Standard Error", "Observations", "F (ANOVA)", "Significance F",
            ],
            "Value": [
                "0.4139", "0.1713", "0.1406",
                "33,219.34", "29", "5.581", "0.0256",
            ],
        }
    )
    st.dataframe(reg_stats, width="stretch", hide_index=True)

st.divider()

# ── Scope City: Ahmedabad ─────────────────────────────────────────────────────
st.header("Scope City — Ahmedabad")
st.write(
    """
    The objective was to quantify changes in slum numbers ward-wise in Ahmedabad city and
    correlate them with market factors. GIS mapping covers all 48 wards — slum change
    over 10 years (2014–2024) and prevailing market rates.
    """
)

a1, a2, a3 = st.columns(3)
a1.metric("Wards mapped", "48", "AMC 2014 boundaries")
a2.metric("Slum HH reduced", "10,072", "2014 → 2024")
a3.metric("People affected", "45,112", "Slum population reduction")


# ── Ahmedabad Interactive Map ─────────────────────────────────────────────────
st.subheader("Ahmedabad — Wards, Slums 2014 & Slums 2024")
st.write(
    "Interactive map with three toggleable layers. Use the layer control (top-right) to "
    "show or hide each layer. Hover over any feature for details."
)

@st.cache_data
def load_wards():
    with open(GEO + "ahmedabad-wards.geojson") as f:
        return json.load(f)

@st.cache_data
def load_slums_2014():
    with open(GEO + "slums-2014-wgs84.geojson", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_slums_2024():
    with open(GEO + "slums-2024-wgs84.geojson", encoding="utf-8") as f:
        return json.load(f)

wards_geojson = load_wards()
slums_2014_geo = load_slums_2014()
slums_2024_geo = load_slums_2024()

ahd_map = folium.Map(location=[23.02, 72.57], zoom_start=11, tiles="CartoDB positron")

# Layer 1 — Ward boundaries choropleth (property rate)
ward_df = pd.DataFrame([
    {
        "Name": f["properties"]["Name"],
        "Market_Rate": f["properties"]["final_excel_property_rate_Market_Rate"],
        "Change10Y": f["properties"]["final_excel_property_rate_% Change in 10Y"],
        "Slum_HH_2014": f["properties"]["final_excel_property_rate_Wards_Slums_Dwelling_Units"],
        "Slum_HH_2024": f["properties"]["final_excel_property_rate_Wards_Slums_2024_Dwellling_Units"],
    }
    for f in wards_geojson["features"]
])
folium.Choropleth(
    geo_data=wards_geojson,
    data=ward_df,
    columns=["Name", "Market_Rate"],
    key_on="feature.properties.Name",
    fill_color="YlOrRd",
    fill_opacity=0.65,
    line_opacity=0.6,
    legend_name="Property Rate (Rs/sqft) — 2024",
    nan_fill_color="lightgrey",
    name="Wards — Property Rate",
).add_to(ahd_map)
folium.GeoJson(
    wards_geojson,
    name="Ward Labels",
    style_function=lambda _: {"fillOpacity": 0, "weight": 0},
    tooltip=folium.GeoJsonTooltip(
        fields=[
            "Name",
            "final_excel_property_rate_Market_Rate",
            "final_excel_property_rate_% Change in 10Y",
            "final_excel_property_rate_Wards_Slums_Dwelling_Units",
            "final_excel_property_rate_Wards_Slums_2024_Dwellling_Units",
        ],
        aliases=["Ward", "Rate (Rs/sqft)", "10Y Change", "Slum HH 2014", "Slum HH 2024"],
        localize=True,
    ),
    show=True,
).add_to(ahd_map)

# Layer 2 — Slums 2014 (dark red)
folium.GeoJson(
    slums_2014_geo,
    name="Slums 2014",
    style_function=lambda _: {
        "fillColor": "#d73027",
        "color": "#a50026",
        "fillOpacity": 0.7,
        "weight": 0.8,
    },
    tooltip=folium.GeoJsonTooltip(fields=["DN"], aliases=["Class ID"]),
    show=True,
).add_to(ahd_map)

# Layer 3 — Slums 2024 (orange, with detailed tooltip)
folium.GeoJson(
    slums_2024_geo,
    name="Slums 2024",
    style_function=lambda _: {
        "fillColor": "#fc8d59",
        "color": "#e34a33",
        "fillOpacity": 0.75,
        "weight": 0.8,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["slum_name", "ward_name", "total_Dvel", "final_popu"],
        aliases=["Slum Name", "Ward", "Dwellings", "Population"],
    ),
    show=True,
).add_to(ahd_map)

folium.LayerControl(collapsed=False).add_to(ahd_map)

st_folium(ahd_map, width="100%", height=580, returned_objects=[])
st.caption(
    "Dark red = Slums 2014 | Orange = Slums 2024 | "
    "Ward fill colour = property rate (Rs/sqft) | Use layer control (top-right) to toggle layers"
)

st.divider()

# ── Correlation Matrix ────────────────────────────────────────────────────────
st.subheader("Correlation Matrix — Ward-Level Variables")
corr_vars = [
    "Change_Area", "Wards_Slums_Dwelling_Units", "Wards_Slums_Population",
    "Wards_Slums_Area", "Wards_Slums_2024_Dwelling_Units",
    "Wards_Slums_2024_Population", "Wards_Slums_2024_Area",
    "Market_Rate_per_sqft", "% Change in 10Y", "Change in Household",
    "Change in Population",
]
corr_matrix = pd.DataFrame(
    [
        [1.00, 0.11, 0.12, 0.32, 0.02, 0.03, -0.13, 0.16, -0.01, 0.42, 0.42],
        [0.11, 1.00, 1.00, 0.78, 0.98, 0.98,  0.76, 0.25,  0.14, 0.14, 0.14],
        [0.12, 1.00, 1.00, 0.78, 0.97, 0.98,  0.75, 0.26,  0.15, 0.15, 0.15],
        [0.32, 0.78, 0.78, 1.00, 0.80, 0.79,  0.90, 0.07,  0.05,-0.04,-0.04],
        [0.02, 0.98, 0.97, 0.80, 1.00, 1.00,  0.82, 0.19,  0.10,-0.07,-0.07],
        [0.03, 0.98, 0.98, 0.79, 1.00, 1.00,  0.81, 0.20,  0.11,-0.08,-0.08],
        [-0.13,0.76, 0.75, 0.90, 0.82, 0.81,  1.00, 0.01,  0.05,-0.24,-0.24],
        [0.16, 0.25, 0.26, 0.07, 0.19, 0.20,  0.01, 1.00,  0.19, 0.28, 0.29],
        [-0.01,0.14, 0.15, 0.05, 0.10, 0.11,  0.05, 0.19,  1.00, 0.18, 0.19],
        [0.42, 0.14, 0.15,-0.04,-0.07,-0.08, -0.24, 0.28,  0.18, 1.00, 1.00],
        [0.42, 0.14, 0.15,-0.04,-0.07,-0.08, -0.24, 0.29,  0.19, 1.00, 1.00],
    ],
    index=corr_vars,
    columns=corr_vars,
)
short_labels = [
    "Change_Area", "Slum_DU_14", "Slum_Pop_14", "Slum_Area_14",
    "Slum_DU_24", "Slum_Pop_24", "Slum_Area_24",
    "Market_Rate", "Chg_10Y", "Chg_HH", "Chg_Pop",
]
label_map = dict(zip(corr_vars, short_labels))
corr_matrix.index = short_labels
corr_matrix.columns = short_labels
corr_long = (
    corr_matrix.reset_index()
    .melt(id_vars="index", var_name="Variable2", value_name="r")
    .rename(columns={"index": "Variable1"})
)
full_map = dict(zip(short_labels, corr_vars))
corr_long["Full1"] = corr_long["Variable1"].map(full_map)
corr_long["Full2"] = corr_long["Variable2"].map(full_map)

heat = alt.Chart(corr_long).mark_rect().encode(
    x=alt.X("Variable1:O", sort=short_labels, title=None, axis=alt.Axis(labelAngle=-40)),
    y=alt.Y("Variable2:O", sort=short_labels, title=None),
    color=alt.Color("r:Q", scale=alt.Scale(scheme="redyellowgreen", domain=[-1, 1]), legend=alt.Legend(title="r")),
    tooltip=[alt.Tooltip("Full1:N", title="Variable 1"), alt.Tooltip("Full2:N", title="Variable 2"), alt.Tooltip("r:Q", title="Correlation", format=".2f")],
)
labels = alt.Chart(corr_long).mark_text(fontSize=9).encode(
    x=alt.X("Variable1:O", sort=short_labels),
    y=alt.Y("Variable2:O", sort=short_labels),
    text=alt.Text("r:Q", format=".2f"),
    color=alt.condition("abs(datum.r) > 0.65", alt.value("white"), alt.value("black")),
)
st.altair_chart(alt.layer(heat, labels).properties(height=400), use_container_width=True)

st.divider()

# ── OLS Regression ────────────────────────────────────────────────────────────
st.subheader("OLS Regression — Slum Area Change vs Property Rate Change")
st.write(
    "**Dependent variable:** % Change in property rates (last 10Y)  \n"
    "**Independent variable:** Change in slum area (2014→2024)"
)

@st.cache_data
def load_property_rate():
    df = pd.read_csv("final_excel _property_rate.csv")
    df = df[["Name", "Change_Area", "% Change in 10Y"]].dropna()
    df["Pct_Change"] = df["% Change in 10Y"] * 100
    return df.reset_index(drop=True)

reg_df = load_property_rate()

q75 = reg_df["Change_Area"].quantile(0.75)
iqr = q75 - reg_df["Change_Area"].quantile(0.25)
fit_df = reg_df[reg_df["Change_Area"] <= q75 + 1.5 * iqr]
m_coef, b_coef = np.polyfit(fit_df["Change_Area"], fit_df["Pct_Change"], 1)
x_line = np.linspace(reg_df["Change_Area"].min(), reg_df["Change_Area"].max(), 200)
y_line = m_coef * x_line + b_coef

trend_df = pd.DataFrame({"Change_Area": x_line, "Pct_Change": y_line})

scatter = alt.Chart(reg_df).mark_circle(color="#4472C4", size=70, opacity=0.85).encode(
    x=alt.X("Change_Area:Q", title="Change in Slum Area (sq m)", axis=alt.Axis(format="~s")),
    y=alt.Y("Pct_Change:Q", title="% Change in Property Rate (10Y)"),
    tooltip=[
        alt.Tooltip("Name:N", title="Ward"),
        alt.Tooltip("Change_Area:Q", title="Slum Area Change (sq m)", format=",.0f"),
        alt.Tooltip("Pct_Change:Q", title="10Y Change (%)", format=".1f"),
    ],
)
trend_line = alt.Chart(trend_df).mark_line(color="#4472C4", strokeWidth=2).encode(
    x="Change_Area:Q",
    y="Pct_Change:Q",
)
st.altair_chart(
    (scatter + trend_line).properties(title="HPI to Affordable Housing Index (2021–2011)", height=420),
    use_container_width=True,
)

ols_c1, ols_c2 = st.columns(2)
with ols_c1:
    st.dataframe(
        pd.DataFrame(
            {
                "Term": ["Constant", "Change_Area"],
                "Coefficient": ["12.5935", "5.609e-05"],
                "Std. Error": ["1.64907", "2.169e-05"],
                "t-ratio": ["7.637", "2.589"],
                "p-value": ["2.03e-08 ***", "0.0149 **"],
            }
        ),
        width="stretch", hide_index=True,
    )
with ols_c2:
    st.dataframe(
        pd.DataFrame(
            {
                "Statistic": ["R-squared", "Adjusted R-squared", "F(1,29)", "P-value (F)", "S.E. of regression", "Observations"],
                "Value": ["0.1877", "0.1597", "6.701", "0.0149", "7.677", "31"],
            }
        ),
        width="stretch", hide_index=True,
    )

st.info(
    "**Interpretation:** R² = 18.77% — slum area change explains ~19% of variability in "
    "property rate change. P-value = 1.49% (< 5%) → null hypothesis accepted. "
    "**Slum rehabilitation increases property rates in the affected ward.**"
)

st.divider()

# ── Conclusion ────────────────────────────────────────────────────────────────
st.header("Conclusion")
st.write(
    """
    Slum deficit was calculated using Census 2011 slum population data against PMAY supply.
    **Ahmedabad showed a negative deficit** (affordable housing available in excess), possibly
    due to political stability, high average income, and targeted pro-poor programs.

    At ward level, supervised classification in QGIS identified slum pockets and their change
    over 10 years (2014–2024), correlated with average property prices per ward.

    OLS regression confirmed: **Reduction of slums increases the property value of the wards**
    (p = 1.49%, R² = 18.77%). Slum rehabilitation under schemes like RAY and PMAY does
    increase property rates in rehabilitated areas.
    """
)

st.divider()

# ── References ────────────────────────────────────────────────────────────────
st.header("References")
st.markdown(
    """
    1. Rao, P. K., & Biswas, A. (2023). *Housing affordability and housing demand assessment for urban poor in India using the hedonic model.* IJHMA. https://doi.org/10.1108/ijhma-09-2023-0124
    2. Abhijat, A., & Pathak, A. (2023). *Mobility and Choices in Urban Housing.* Environment and Urbanization ASIA, 14(1), 131–141. https://doi.org/10.1177/09754253231161022
    3. Kulkarni, R. (n.d.). *Property prices surge by 6% across top cities of India.* Housing.com.
    4. Knight Frank Research. *Rediscovering Affordability.*
    5. JLL Research. (2023, December). *Home Purchase Affordability Index.* jll.co.in.
    6. Shri Ajesh Palayi & Shri Nalin Priyaranjan. (2018, January). *Affordable Housing in India.* RBI Bulletin.
    7. Darshini Mahadevia, Bhatia, & Bhonsale. (2014). *Slum Rehabilitation Schemes (SRS) across Ahmedabad.* CUE Working Paper 27, CEPT University.
    8. Patel, B. N., Byahut, S., & Bhatha, B. (2017). *Building regulations are a barrier to affordable housing in Indian cities: the case of Ahmedabad.* https://doi.org/10.1007/s10901-017-9552-7
    9. Marnane, K., & Greenop, K. (2023). *Housing adequacy in an informal built environment: case studies from Ahmedabad.* https://doi.org/10.1007/s10901-023-10029-x
    10. Desai, & Sanghvi. (2018). *Mapping Evictions and Resettlement in Ahmedabad, 2000–17.* CUE Working Paper 39, CEPT University.
    11. Mahadevia, D., Bhatia, N., & Bhatt, B. (2018). *Private Sector in Affordable Housing? Case of Slum Rehabilitation Scheme in Ahmedabad.* https://doi.org/10.1177/0975425317748449
    """
)

st.divider()