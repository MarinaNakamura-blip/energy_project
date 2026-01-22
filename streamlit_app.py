import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide") # Full browser width
sns.set_theme(style="darkgrid")
st.title("Swedish Energy Production Dashboard")

@st.cache_data # Only read this file once unless it changes
def load_tidy():
    return pd.read_csv("data/tidy_energy.csv") 

df_long = load_tidy() # Calls the function and stores the tidy dataset in a DataFrame

countries = sorted(df_long["country"].unique()) # Extracts all available countries and energy sources for dropdowns
sources = sorted(df_long["energy_source"].unique())

stack_sources = ["Bioenergy", "Hydropower", "Wind power", "Solar photovoltaic", "Solar thermal", "Heat pumps (renewable)"]

def stacked_pivot(df):

source = st.sidebar.selectbox("Energy source", sources) # Adds a dropdown in the sidebar
compare = st.sidebar.selectbox("Compare Sweden with", [c for c in countries if c not in ["Sweden", "EU27 (average of EU)"]], index=0) # Sweden and EU average is excluded because it’s always included by default
st.sidebar.caption(f"Showing: Sweden + EU27 (average of EU) + {compare}")

# ================================ 
# Tab 1: Trend over time 
# ================================
with tab1:
    filtered = df_long[(df_long["energy_source"] == source) & (df_long["country"].isin(["Sweden", "EU27 (average of EU)", compare]))] # Creates a filtered DataFrame

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=filtered, x="year", y="electricity_ktoe", hue="country", marker="o", ax=ax, legend=False) # Line chart of electricity production over time
    for country, df_c in filtered.groupby("country"):
        last = df_c.sort_values("year").iloc[-1]
        ax.text(last["year"] + 0.2,last["electricity_ktoe"], f" {country}", va="center", fontsize=9)
    st.pyplot(fig) # Renders the Matplotlib figure inside the Streamlit app

# ================================ 
# Tab 2: Renewables mix (stacked)
# ================================
with tab2:
    st.subheader("Sweden: energy mix (latest 15 years)")

    stack_sources = [   # Define what to stack
        "Bioenergy",
        "Hydropower",
        "Wind power",
        "Solar photovoltaic",
        "Solar thermal",
        "Heat pumps (renewable)"
    ]
    
    swe = df_long[df_long["country"] == "Sweden"].copy()
    swe = swe.dropna(subset=["electricity_ktoe"])

    last_year = int(swe["year"].max())
    first_year = last_year - 14
    swe_15 = swe[swe["year"].between(first_year, last_year)]
    
    swe_stack = swe_15[swe_15["energy_source"].isin(stack_sources)].pivot_table(   
        index="year",
        columns="energy_source",
        values="electricity_ktoe",
        aggfunc="sum",
        fill_value=0
    )
    
    swe_total = swe_15[swe_15["energy_source"] == "All energy sources"].groupby("year")["electricity_ktoe"].sum() # overlay TOTAL as a line
    
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    swe_stack.plot(kind="bar", stacked=True, ax=ax1)

    if len(swe_total) > 0:
        ax1.plot(range(len(swe_total.index)), swe_total.values, marker="o")
        ax1.set_xticks(range(len(swe_total.index)))
        ax1.set_xticklabels(swe_total.index, rotation=0)

    ax1.set_title("Sweden: Energy production by source (stacked) — latest 15 years")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Electricity (ktoe)")
    ax1.legend(title="Energy source", bbox_to_anchor=(1.02, 1), loc="upper left")
    fig1.tight_layout()
    st.pyplot(fig1)

    st.divider()
    st.subheader("Sweden vs selected country (1995 / 2014 / 2024)")

    compare2 = st.selectbox("Compare Sweden with", [c for c in countries if c != "Sweden"], index=0, key="compare2")

    years = [1995, 2014, 2024]

    cmp_df = df_long[
        (df_long["country"].isin(["Sweden", compare2])) &
        (df_long["year"].isin(years)) &
        (df_long["energy_source"].isin(stack_sources))
    ].dropna(subset=["electricity_ktoe"])

    cmp_pivot = cmp_df.pivot_table(index=["year", "country"], columns="energy_source", values="electricity_ktoe", aggfunc="sum", fill_value=0)
    
     # Create nicer x labels like "1995 Sweden" and "1995 Germany"
    cmp_pivot.index = [f"{y} {c}" for (y, c) in cmp_pivot.index]

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    cmp_pivot.plot(kind="bar", stacked=True, ax=ax2)

    ax2.set_title(f"Energy mix comparison: Sweden vs {compare2} (selected years)")
    ax2.set_xlabel("Year / Country")
    ax2.set_ylabel("Electricity (ktoe)")
    ax2.legend(title="Energy source", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=45, ha="right")
    fig2.tight_layout()
    st.pyplot(fig2)