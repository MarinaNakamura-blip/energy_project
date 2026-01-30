# This file contains reusable functions for:
# - Loading the cleaned (tidy) Eurostat energy dataset from CSV
# - Creating matplotlib/seaborn figures used in the Streamlit dashboard
# Each plotting function returns a matplotlib Figure (fig) object.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


TYDY_CSV_PATH = "data/tidy_energy.csv"

def load_tidy_energy():
    df = pd.read_csv(TYDY_CSV_PATH)
    return df

# Choose the most common renewable energy sources to show in stacked charts
CHOSEN_RENEWABLES = ["Bioenergy", "Hydropower", "Wind power", "Solar photovoltaic", "Solar thermal", "Heat pumps (renewable)"]
RENEWABLE_TOTAL = "Renewables (total)" # Dataset labels
TOTAL_ENERGY_SOURCE = "All energy sources" # renewable + non-renewable

# ==================================================================
# Line chart: renewables trend over time
# ==================================================================
# The only chart where user filters both countries and the energy source in Streamlit app

def renewables_over_time(filtered: pd.DataFrame, energy_source: str): # filtered: subset of df filtered by energy_source and countries
    fig, ax = plt.subplots(figsize=(12, 5))

    sns.lineplot(data=filtered, x="year", y="electricity_ktoe", hue="country", marker="o", ax=ax) # One line per country

    ax.set_title(f"{energy_source} production over 30 years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Electricity production (ktoe)")
    ax.grid(True)
    ax.legend(fontsize=10, bbox_to_anchor=(1.02, 1), loc="upper left") # Legend outside plot so it won't cover the lines

    return fig

# ==================================================================
# Stacked bar chart: renewables vs non-renewables
# ==================================================================

def renewables_vs_nonrenewables_bar(df, country):
    d = df[df["country"] == country] # Filter to a chosen country

    total = (d[d["energy_source"] == TOTAL_ENERGY_SOURCE].set_index("year")["electricity_ktoe"].sort_index())
    renew = (d[d["energy_source"] == RENEWABLE_TOTAL].set_index("year")["electricity_ktoe"].reindex(total.index, fill_value=0)) # Aligned to total's years
    nonrenew = (total - renew).clip(lower=0) # Avoid negative values if any data inconsistency, non-renewables = Total - Renewables

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(total.index, renew, label="Renewables (total)")
    ax.bar(total.index, nonrenew, bottom=renew, label="Non-renewables (calculated)")

    ax.set_title(f"{country}: Total energy production (renewables vs non-renewables)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Electricity production (ktoe)")
    ax.legend(fontsize=10, bbox_to_anchor=(1.02, 1), loc="upper left")

    return fig

# ==================================================================
# Stacked area chart: composition of renewable energy sources as %
# ==================================================================
# The renewable energy mix as shares (%) of total renewable production.

def renewables_share(df, country):
    d = df[df["country"] == country]

    chosen = d[d["energy_source"].isin(CHOSEN_RENEWABLES)].pivot_table(  # Pivot chosen renewables (ktoe per year)
        index="year", # rows
        columns="energy_source",
        values="electricity_ktoe",
        aggfunc="sum",
        fill_value=0
    ).sort_index()

    rt = d[d["energy_source"] == RENEWABLE_TOTAL].set_index("year")["electricity_ktoe"].sort_index()  # Renewables total (ktoe per year)
    other = (rt - chosen.sum(axis=1)).clip(lower=0)  # Other renewables = Renewables (total) - sum of chosen ones
    chosen["Other renewables"] = other  # Redefine "Other renewables" column for accuracy

    share = chosen.div(chosen.sum(axis=1).replace(0, 1), axis=0) * 100  # Divide each year by the year's total to get percentages

    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax1.stackplot(share.index, *[share[c] for c in share.columns], labels=share.columns)
    ax1.set_ylim(0, 100)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Renewables share (%)")
    ax1.set_title(f"{country}: Renewable energy mix (share %)")
    ax1.legend(fontsize=10, bbox_to_anchor=(1.02, 1), loc="upper left")
    return fig

# ==================================================================
# Box plot: Sweden vs EU27 average
# ==================================================================
# It shows typical level (median), variation across years (spread), and unusually high/low years (outliers)

def renewables_boxplot(df: pd.DataFrame, energy_source: str):
    d = df[(df["energy_source"] == energy_source) & (df["country"].isin(["Sweden", "EU27 (average of EU)"]))] # The user selects energy_source

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=d, x="country", y="electricity_ktoe", ax=ax)

    ax.set_title(f"{energy_source}: Sweden vs EU27")
    ax.set_xlabel("")
    ax.set_ylabel("Electricity production (ktoe)")
    ax.grid(True, axis="y")

    return fig

# ==================================================================
# Bar chart: ranking of renewables' share in EU
# ==================================================================

def top10_renewable_share(df, year=2024):
    d = df[df["year"] == year] # Filter for selected year data
    
    # Pivot to get one row per country, with columns for totals
    pivot = d.pivot_table(index="country", columns="energy_source", values="electricity_ktoe", aggfunc="sum")
    pivot = pivot.dropna(subset=["Renewables (total)", "All energy sources"]) # Keep only rows that have both values
    pivot["renewable_share"] = (pivot["Renewables (total)"] / pivot["All energy sources"]) * 100  # Calculate share with %
    
    top10 = (pivot["renewable_share"].sort_values(ascending=False).head(10).reset_index())
    
    return top10

def top10_renewable_share_bar(top10_df, year=2024):
    top10_sorted = top10_df.sort_values("renewable_share")  # Horizontal order

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(top10_sorted["country"], top10_sorted["renewable_share"])
    ax.set_xlabel("Renewable share (%)")
    ax.set_title(f"Top 10 countries by renewable share ({year})")
    
    return fig