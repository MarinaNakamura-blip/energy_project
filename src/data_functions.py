import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


TYDY_CSV_PATH = "data/tidy_energy.csv"

def load_tidy_energy():
    df = pd.read_csv(TYDY_CSV_PATH)
    return df

# The most common renewable energy sources to show in stacked charts
CHOSEN_RENEWABLES = ["Bioenergy", "Hydropower", "Wind power", "Solar photovoltaic", "Solar thermal", "Heat pumps (renewable)"]
RENEWABLE_TOTAL = "Renewables (total)"
TOTAL_ENERGY_SOURCE = "All energy sources"

# ----------------------------------------
# Line chart: renewables trend over time
# ----------------------------------------
def renewables_over_time(df: pd.DataFrame, filtered: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=filtered, x="year", y="electricity_ktoe", hue="country", marker="o", ax=ax, legend=False)

# ------------------------------------------------------------------
# Stacked area chart: renewables share with total energy production
# ------------------------------------------------------------------
def renewables_share_with_total(
    df: pd.DataFrame,
    country: str,
    *,
    chosen_renewables: list[str] = CHOSEN_RENEWABLES,
    renewables_total_label: str = RENEWABLE_TOTAL,
    total_label: str = TOTAL_ENERGY_SOURCE,
    other_label: str = "Other renewables (calculated)"
):
    """
    Stacked area = share (%) of:
      - chosen renewables
      - calculated other renewables = Renewables(total) - sum(chosen renewables)

    Line (2nd axis) = total energy production (ktoe) using "All energy sources".
    """

    d = df[df["country"] == country].copy() # Boolean filtering and copy to avoid SettingWithCopyWarning
    
    # Pivot table for chosen renewables
    pr = d[d["energy_source"].isin(chosen_renewables)]
    chosen = (pr.pivot_table(index="year", columns="energy_source", values="electricity_ktoe", aggfunc="sum", fill_value=0)
              .fillna(0).sort_index())
    
    # Get renewables total to calculate "other" later
    rt = (d[d["energy_source"] == renewables_total_label].groupby("year", as_index=True)["electricity_ktoe"]
          .sum().sort_index())
    
    