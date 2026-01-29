import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


TYDY_CSV_PATH = "data/tidy_energy.csv"

def load_tidy_energy():
    df = pd.read_csv(TYDY_CSV_PATH)
    return df

# Choose the most common renewable energy sources to show in stacked charts
CHOSEN_RENEWABLES = ["Bioenergy", "Hydropower", "Wind power", "Solar photovoltaic", "Solar thermal", "Heat pumps (renewable)"]
RENEWABLE_TOTAL = "Renewables (total)"
TOTAL_ENERGY_SOURCE = "All energy sources"

# ==================================================================
# Line chart: renewables trend over time
# ==================================================================

def renewables_over_time(filtered: pd.DataFrame, energy_source: str):
    fig, ax = plt.subplots(figsize=(12, 5))

    sns.lineplot(data=filtered, x="year", y="electricity_ktoe", hue="country", marker="o", ax=ax)

    ax.set_title(f"{energy_source} production over 30 years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Electricity production (ktoe)")
    ax.grid(True)
    ax.legend(fontsize=10, bbox_to_anchor=(1.02, 1), loc="upper left")

    return fig

# ==================================================================
# Stacked area chart: renewables share with total energy production
# ==================================================================

def renewables_share_with_total(df, country):
    d = df[df["country"] == country]

    # 1) Pivot chosen renewables (ktoe per year)
    chosen = d[d["energy_source"].isin(CHOSEN_RENEWABLES)].pivot_table(
        index="year",
        columns="energy_source",
        values="electricity_ktoe",
        aggfunc="sum",
        fill_value=0
    ).sort_index()

    # 2) Renewables total (ktoe per year)
    rt = d[d["energy_source"] == RENEWABLE_TOTAL].set_index("year")["electricity_ktoe"].sort_index()

    # 3) Other renewables = total renewables - chosen renewables' sum
    other = (rt - chosen.sum(axis=1)).clip(lower=0)
    chosen["Other renewables"] = other

    # 4) Convert to shares (%)
    share = chosen.div(chosen.sum(axis=1).replace(0, 1), axis=0) * 100

    # 5) Plot
    fig, ax1 = plt.subplots(figsize=(7, 4))
    ax1.stackplot(share.index, *[share[c] for c in share.columns], labels=share.columns)
    ax1.set_ylim(0, 100)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Renewables share (%)")
    ax1.set_title(f"{country}: Renewables mix (share %) + total production")
    ax1.legend(fontsize=10, bbox_to_anchor=(1.02, 1), loc="upper left")
    return fig

# ==================================================================
# Stacked bar chart: renewables vs non-renewables
# ==================================================================

def renewables_vs_nonrenewables_bar(df, country):
    d = df[df["country"] == country]

    total = (d[d["energy_source"] == TOTAL_ENERGY_SOURCE].set_index("year")["electricity_ktoe"].sort_index())
    renew = (d[d["energy_source"] == RENEWABLE_TOTAL].set_index("year")["electricity_ktoe"].reindex(total.index, fill_value=0))
    nonrenew = (total - renew).clip(lower=0)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(total.index, renew, label="Renewables (total)")
    ax.bar(total.index, nonrenew, bottom=renew, label="Non-renewables (calculated)")

    ax.set_title(f"{country}: Total energy production (renewables vs non-renewables)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Electricity production (ktoe)")
    ax.legend(fontsize=10, bbox_to_anchor=(1.02, 1), loc="upper left")

    return fig

# ==================================================================
# Box plot: Sweden vs EU27 average
# ==================================================================

def renewables_boxplot(df: pd.DataFrame, energy_source: str):
    # Filter to Sweden and EU27 average
    d = df[(df["energy_source"] == energy_source) & (df["country"].isin(["Sweden", "EU27 (average of EU)"]))]

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.boxplot(data=d, x="country", y="electricity_ktoe", ax=ax)

    ax.set_title(f"{energy_source}: Sweden vs EU27")
    ax.set_xlabel("")
    ax.set_ylabel("Electricity production (ktoe)")
    ax.grid(True, axis="y")

    return fig