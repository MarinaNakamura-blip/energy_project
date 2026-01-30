# Individual school project / Sustainable energy production

## Overview

This project provides a platform for users to explore **renewable energy production in the European Union using Eurostat energy data**, with a focus on Sweden. 
The goal is to understand how sustainable Sweden is (and other EU countries) by analyzing long-term trends, energy mix composition, and comparisons between Sweden and the EU.

The project combines data cleaning and visual exploration in Jupyter Notebook, creating functions in Python, and an interactive Streamlit dashboard.

Streamlit app: ([Click here to see the app](https://energyeu.streamlit.app/))

## Data source ##

- Eurostat - Electricity production by energy source and country ([Link to the dataset](https://ec.europa.eu/eurostat/databrowser/view/nrg_bal_peh__custom_19676230/default/table))
- Time period : From 1995 to 2024
- Data processed into a tidy long format for analysis and visualization

The dataset was manually selected from Eurostat to include EU countries, common renewable energy sources, and a chosen time period relevant to the analysis.

## What the dashboard shows ##

The Streamlit app includes three main views:

- [ Renewable energy trends ]:  
Line charts showing how renewable energy production develops over time across countries.

- [ Renewable energy mix ]:  
Stacked charts showing renewables vs non-renewable energy in comparison with total energy production, and how different renewable sources contribute to total renewable production.

- [ Sweden vs EU comparison ]:  
Box plots comparing the distribution of renewable energy production over time in Sweden and the EU average.

Each visualization is accompanied by a short interpretation to support understanding.

## How to run the app ##
pip install -r requirements.txt

streamlit run streamlit_app.py



