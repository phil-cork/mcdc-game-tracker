import streamlit as st
from streamlit_autorefresh import st_autorefresh
from utils.data_loader import run_data_pipeline
from tabs import stats, data_demo, scenarios, heroes, players

st.set_page_config(layout="wide")

# Auto-refresh every 30 seconds
st_autorefresh(interval=30_000, key="autorefresh_timer")

st.title("MC/DC Game Tracker")

# Read sheet directly (always fresh)
df, game_df, player_df, full_df = run_data_pipeline()

stats_tab, scenarios_tab, heroes_tab, player_tab, demo_tab = st.tabs(['Stats',
                                                                     'Scenarios',
                                                                     'Heroes',
                                                                     'Players',
                                                                     'DEMO'])

with stats_tab:
    stats.render(game_df, player_df)

with scenarios_tab: 
    scenarios.render(game_df)

with heroes_tab:
    heroes.render(player_df)

with player_tab:
    players.render(player_df)

with demo_tab:
    data_demo.render(df, game_df, player_df, full_df)