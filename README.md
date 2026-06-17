# Affordable Housing in Indian Cities — Market Impact Analysis

**Live App → [pmay-analysis-ahmedabad.streamlit.app](https://pmay-analysis-ahmedabad.streamlit.app/)**

---

## About

This is an interactive data report built for an academic research project at **IIT Bombay (TD-642, Group 2)**. It examines the **Pradhan Mantri Awas Yojana – Urban (PMAY-U)** scheme and its effect on local property markets, with a deep-dive into **Ahmedabad, Gujarat** at ward level.

The research asks a simple but consequential question: *does slum rehabilitation under PMAY-U have an effect on property prices in the surrounding area?* OLS regression at ward level (R² = 18.77%, p = 1.49%) confirms that it does.

---

## Data Sources

| Data | Source |
|---|---|
| Slum population (2011) | Census of India 2011 |
| PMAY-U sanctioned units | Ministry of Housing & Urban Affairs (MoHUA) |
| Housing Price Index (HPI) | Reserve Bank of India |
| Ward-level property rates | housing.com, MagicBricks (scraped April 2024) |
| Ahmedabad ward boundaries | Ahmedabad Municipal Corporation (AMC) |
| Slum boundaries 2014 | Centre for Environment and Planning, Gujarat (CEPT) |
| Slum boundaries 2024 | AMC / field classification (QGIS supervised classification) |

---

## Tech Stack

- **[Streamlit](https://streamlit.io/)** — app framework
- **[Folium](https://python-visualization.github.io/folium/)** + **[streamlit-folium](https://github.com/randyzwitch/streamlit-folium)** — interactive maps
- **[Altair](https://altair-viz.github.io/)** — correlation heatmap and regression scatter plot
- **Pandas / NumPy** — data wrangling and OLS regression
- GeoJSON (WGS84) for all geospatial layers

---

## Authors

**Varun Phadke** — analysis, GIS mapping, app development

Team: Chintan Patel, Pawan Singh Ahirwar, Sandeep Kadam

Guided by **Prof. Pennan Chinnasamy** and **Prof. Ashish Desai**, IIT Bombay
