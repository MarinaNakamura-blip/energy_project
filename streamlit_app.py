# This file is the Streamlit user interface to visualize Eurostat energy data
# Reuses functions from src/data_functions.py and keep this file focused on UI only

import streamlit as st
from src.data_functions import (
    load_tidy_energy, 
    renewables_over_time, 
    renewables_share,
    renewables_boxplot, 
    renewables_vs_nonrenewables_bar, 
    top10_renewable_share, 
    top10_renewable_share_bar
)

TREND_ENERGY_OPTIONS = ["Bioenergy", "Hydropower", "Wind power", "Solar photovoltaic", "Solar thermal", "Heat pumps (renewable)", "Renewables (total)"]

st.set_page_config(page_title="Sweden Renewables Dashboard", layout="wide")

df = load_tidy_energy()

st.title("Welcome to EU Renewable Energy Dashboard!⚡️")
st.subheader("Explore how sustainable Sweden and other EU countries are, based on their renewable energy production")
st.write(
    """
    This app uses Eurostat energy data to explore renewable energy production across EU, with a focus on Sweden.
    
    The data covers electricity production by energy source over 30 years and allows comparison between Sweden, individual EU countries, and EU-wide averages.

    **In this dashboard, you can:**
    - 1. Explore long-term trends in renewable energy production for selected energy sources and countries.
    - 2. Examine how renewable energy contributes to total energy production, and how the renewable energy mix changes over time.
    - 3. Compare Sweden’s renewable energy production with the EU using a distribution chart that shows typical production levels, variation over time, and extreme years.
    - 4. See the top 10 countries by renewable energy share relative to total energy production in 2024.
    """
    )
st.markdown(
    "🔗 **Original data source:** "
    "[Eurostat – Electricity production by energy source and country]"
    "(https://ec.europa.eu/eurostat/databrowser/view/nrg_bal_peh__custom_19676230/default/table)" # External link to Eurostat data
)

# Page navigation using radio buttons to show 4 options for a better user experience. Simpler than a sidebar.
page = st.radio("Choose what you want to explore⚡️:",
                ["1, Trend over time", "2, Renewables mix overview", "3, Sweden vs EU: distribution", "4, Top 10 renewable share (2024)"], horizontal=True)
    
st.divider()

# ==================================================
# Page 1: Trend line chart
# ==================================================

if page == "1, Trend over time":
    st.header("1, Trend over time")
    st.write("Pick an energy source and add countries to compare the production over 30 years.")

    energy = st.selectbox("Energy source", TREND_ENERGY_OPTIONS) # User selects one renewable category to view as a trend
    countries = st.multiselect(  # User selects one or more countries to add the lines and compare
        "Countries",
        sorted(df["country"].unique()),
        default=["Sweden", "EU27 (average of EU)"] if "EU27 (average of EU)" in df["country"].unique() else ["Sweden"] # Set default focus on Sweden
    )

    filtered = df[(df["energy_source"] == energy) & (df["country"].isin(countries))] # Filter the dataset based on user input

    fig = renewables_over_time(filtered, energy) 
    st.pyplot(fig, clear_figure=True) 
    st.caption("Sweden’s total renewable energy production has increased steadily over time and remains consistently higher than the EU average.")
    
# ==================================================
# Page 2: Stacked bar and area charts
# ==================================================

elif page == "2, Renewables mix overview":
    st.header("2, Renewables mix overview")
    st.write(
        """
This section shows two diagrams for the selected country:
- Renewable vs non-renewable energy in total production
- Renewable energy mix (share %)

"""
    )
    # User selects one country (same selection used for both charts) and default to Sweden
    country = st.selectbox("Country", sorted(df["country"].unique()), index=sorted(df["country"].unique()).index("Sweden") if "Sweden" in df["country"].unique() else 0)

    # === Chart 1: Renewables vs non-renewables ===
    st.subheader("Renewables vs non-renewables (total production)")
    fig1 = renewables_vs_nonrenewables_bar(df, country)
    st.pyplot(fig1, clear_figure=True)
    st.caption("Total energy production remains relatively stable over time, while the share of renewable energy increases steadily.")
    
    st.divider()
    
    # === Chart 2: Renewable mix (share %) ===
    st.subheader("Renewable energy mix (share %)")
    fig2 = renewables_share(df, country)
    st.pyplot(fig2, clear_figure=True)
    st.caption("In general, the renewable energy mix has become more diversified over time, with growing contributions from wind, solar and bioenergy.")

# ==================================================
# Page 3: Box plot
# ==================================================

elif page == "3, Sweden vs EU: distribution":
    st.header("3, Sweden vs EU: distribution")
    st.write("Pick an energy source to show a Box plot showing the distribution over the years (median, variation, outliers).")

    energy = st.selectbox("Energy source", TREND_ENERGY_OPTIONS) # User choose which renewable category to compare (Sweden vs EU average)
    fig = renewables_boxplot(df, energy)
    st.pyplot(fig, clear_figure=True)
    st.caption("Sweden’s renewable energy production is consistently higher than the EU average, with both a higher typical level and greater variation over time.")

# ==================================================
# Page 4: Bar chart
# ==================================================

else:
    st.header("4, Top 10 countries by renewable energy share in 2024")
    st.write("This ranking shows the countries with the highest share of renewable energy relative to total energy production in 2024.")
    
    top10 = top10_renewable_share(df, year=2024) # Get top 10 data from the table
    fig = top10_renewable_share_bar(top10, year=2024) # Create the bar chart
    st.pyplot(fig, clear_figure=True)
    st.caption("In 2024, Sweden ranked as the 7th country in the EU for renewable energy share, with about 70% of its total energy production coming from renewable sources.")