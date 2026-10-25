import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from utils.data_loader import run_data_pipeline, load_data
from tabs import stats, scenarios, heroes, players, heatmap, aspects, regions

st.set_page_config(layout="wide")

# Auto-refresh every 30 seconds
st_autorefresh(interval=30_000, key="autorefresh_timer")

# pull in raw Google Sheet data and format columns
df = load_data()

with st.container(horizontal=True):
  st.image("https://images.squarespace-cdn.com/content/68505f7ba6f6d35a7e5e0412/efa683f1-b11e-4ad5-83e6-6f482f9f0477/mdc-game-tracker-3.png",
           width=400)
  st.space("stretch")

  st.link_button(label="Report Games", 
                 type='secondary',
                 url="https://mcdc.fillout.com/game-tracker",
                 help="Follow this link to fill out the form and see game reports appear in the app",
                 icon=":material/open_in_new:")
st.divider()

with st.container():
    st.header("Download Player Data")

    # bring in all usernames and sort into unique list
    USERNAMES_LIST = ['Select a Player'] + sorted(
            pd.unique(df[['name_player_1', 'name_player_2', 'name_player_3', 'name_player_4']].stack().astype(str)),
            key=str.lower,
        )
    
    # create selectbox and store username
    st.selectbox(label='Player Name', options=USERNAMES_LIST, key='username_filter', width=300)
    st.session_state.setdefault("username_filter", USERNAMES_LIST[0])
    username = st.session_state.username_filter
    username_filename = username.replace(" ", "-")

    # filter dataframe and export data
    download_df = df[(df['name_player_1']==username) | (df['name_player_2']==username) | (df['name_player_3']==username) | (df['name_player_4']==username)].copy()
    st.download_button(label='Download', data=download_df.to_csv(), file_name=f"exports/mcdc26-game-tracker-output-{username_filename}.csv", icon=':material/download:')


st.divider()

# create list of regions for top-level filter
regions_list = ['All'] + df['region'].unique().tolist()

# set filter to "All" by default
st.session_state.setdefault("region_filter", regions_list[0])

# create top-level filter for regions
st.selectbox("Region",
             regions_list,
             key='region_filter')
region = st.session_state.region_filter

# create subsequent datasets from optionally filtered data
game_df, scenario_df, player_df, hero_aspect_df, aspect_df, heatmap_df, region_df = run_data_pipeline(df, region)

stats_tab, scenarios_tab, heroes_tab, aspects_tab, heatmap_tab, player_tab, regions_tab = st.tabs([
                                                                     'Stats',
                                                                     'Scenarios',
                                                                     'Heroes',
                                                                     'Aspects',
                                                                     'Checklist',
                                                                     'Players',
                                                                     'Regions'])

with stats_tab:
    stats.render(game_df, player_df)

with scenarios_tab: 
    scenarios.render(scenario_df)

with heroes_tab:
    heroes.render(hero_aspect_df)

with aspects_tab:
    aspects.render(aspect_df)

with heatmap_tab:
    heatmap.render(heatmap_df)

with player_tab:
    players.render(player_df)

with regions_tab:
    regions.render(region_df)