import streamlit as st
from streamlit_autorefresh import st_autorefresh
from utils.data_loader import run_data_pipeline, load_data
from tabs import stats, scenarios, heroes, players, heatmap, aspects

st.set_page_config(layout="wide")

# Auto-refresh every 30 seconds
st_autorefresh(interval=30_000, key="autorefresh_timer")

st.title("MC/DC Game Tracker")

# pull in raw Google Sheet data and format columns
df = load_data()

# create list of regions for top-level filter
regions = ['All'] + df['region'].unique().tolist()

# set filter to "All" by default
st.session_state.setdefault("region_filter", regions[0])

# create top-level filter for regions
st.selectbox("Region",
             regions,
             key='region_filter')
region = st.session_state.region_filter

# if filter selected, filter down
if region != 'All':
    df = df[df['region']==region]

# create subsequent datasets from optionally filtered data
game_df, player_df, aspect_df, heatmap_df, full_df = run_data_pipeline(df)

stats_tab, scenarios_tab, heroes_tab, aspects_tab, heatmap_tab, player_tab = st.tabs(['Stats',
                                                                     'Scenarios',
                                                                     'Heroes',
                                                                     'Aspects',
                                                                     'Heatmap',
                                                                     'Players'])

with stats_tab:
    stats.render(game_df, player_df)

with scenarios_tab: 
    scenarios.render(game_df)

with heroes_tab:
    heroes.render(aspect_df)

with aspects_tab:
    aspects.render(aspect_df)

with heatmap_tab:
    heatmap.render(heatmap_df)

with player_tab:
    players.render(player_df, aspect_df)