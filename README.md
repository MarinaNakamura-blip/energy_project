# Individual school project / Sustainable energy production

## Overview

This project provides a platform for users to explore **renewable energy production in the European Union using Eurostat energy data**, with a focus on Sweden. 
The aim is to understand how sustainable Sweden and other EU countries are by analyzing long-term trends, energy mix composition, and comparative performance within the EU.

The project combines:
- data cleaning exploration in Jupyter Notebook
- reusable Python functions for analysis and visualization
- an interactive Streamlit dashboard for presentation

Streamlit app: ([Click here to see the app](https://energyeu.streamlit.app/))

## Data source ##

- Eurostat - Electricity production by energy source and country ([Link to the dataset](https://ec.europa.eu/eurostat/databrowser/view/nrg_bal_peh__custom_19676230/default/table))
- Time period : From 1995 to 2024
- Data processed into a tidy long format for analysis and visualization

The dataset was manually selected from Eurostat to include EU countries, common renewable energy sources, and a chosen time period relevant to the analysis.

## What the dashboard shows ##

The Streamlit app includes four main views:

1. [ Renewable energy trends ]:  
- **Line chart** showing how renewable energy production develops over time across countries.

2. [ Renewable energy mix overview ]:  
- **Stacked bar chart**: Comparison of renewable vs non-renewable energy within total energy production
- **Stacked area chart**: Composition of renewable energy sources as shares (%) of total renewable production over time

3. [ Sweden vs EU comparison ]:  
- **Box plots** comparing the distribution of renewable energy production over time in Sweden and the EU average, highlighting typical levels, variation, and extreme years.

4. [Top 10 EU countries on renewable energy share (2024)]:
- A ranking **bar chart** of the top 10 EU countries based on the share of renewable energy relative to total energy production in 2024.

Each visualization is accompanied by a short interpretation to support understanding.

## How to run the app ##
pip install -r requirements.txt

streamlit run streamlit_app.py



