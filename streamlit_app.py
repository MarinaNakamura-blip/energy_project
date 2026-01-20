import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(layout="wide")
sns.set_theme(style="darkgrid")

@st.cache_data
def load_tidy():
    return pd.read_csv("data/tidy_energy.csv")

df_long = load_tidy()

countries = sorted(df_long["geo"].unique())
sources = sorted(df_long["siec"].unique())

source = st.sidebar.selectbox("Energy source", sources)
compare = st.sidebar.selectbox("Compare Sweden with", [c for c in countries if c != "SE"], index=0)

filtered = df_long[(df_long["siec"] == source) & (df_long["geo"].isin(["SE", compare]))]

fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered, x="year", y="value", hue="geo", marker="o", ax=ax)
st.pyplot(fig)
