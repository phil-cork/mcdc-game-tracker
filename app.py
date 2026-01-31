import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from utils.data_loader import most_frequent_value, run_data_pipeline
from utils.charts import donut_chart, bar_chart, smart_metric
from tabs import stats, data_demo

st.set_page_config(layout="wide")

# Auto-refresh every 30 seconds
st_autorefresh(interval=30_000, key="autorefresh_timer")

st.title("MC/DC Game Tracker")

# Read sheet directly (always fresh)
df, game_df, player_df, full_df = run_data_pipeline()

stats_tab, demo_tab = st.tabs(['Stats', 'DEMO'])

with stats_tab:
    stats.render(df, game_df, player_df, full_df)

with demo_tab:
    data_demo.render(df, game_df, player_df, full_df)