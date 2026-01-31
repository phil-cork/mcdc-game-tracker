import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from utils.data_loader import most_frequent_value, run_data_pipeline
from utils.charts import donut_chart, bar_chart, smart_metric

st.set_page_config(layout="wide")

def render(df, game_df, player_df, full_df):

    stats_col, player_count_col = st.columns(2)

    with stats_col:
        st.header("Stats")

        metric_1, metric_2 = st.columns(2)
        metric_3, metric_4 = st.columns(2)
        metric_5, metric_6 = st.columns(2)

        metric_1.metric(value=len(game_df.submission_id.drop_duplicates().dropna()),
                    label="Games Played", border=True)
            
        metric_2.metric(value=len(player_df.name.drop_duplicates()),
                    label="Players", border=True)
            
        metric_3.metric(value=len(game_df.scenario.drop_duplicates().dropna()),
                        label="Scenarios", border=True)
        
        metric_4.metric(value=len(player_df.hero.drop_duplicates().dropna()),
                        label="Heroes", border=True)
        
        metric_5.metric(value=round(len(game_df.query("outcome=='Win'"))/len(game_df),2), format="percent",
                        label="Win Rate", border=True)

        metric_6.metric(value=player_df[['hero', 'aspect']].drop_duplicates().shape[0],
                        label="Hero & Aspect Combinations", border=True)

    with player_count_col:
        st.header("Player Count")
        st.altair_chart(donut_chart(game_df, category_col='number_of_players'))

    scenario_col, difficulty_col = st.columns(2)

    with scenario_col:
        st.header("Scenarios")
        st.altair_chart(
            bar_chart(game_df,
                    y='scenario:N', x='count', color='outcome:N', title='')
        )

    with difficulty_col:
        st.header("Difficulty")
        st.altair_chart(
            bar_chart(game_df,
                    y='difficulty:N', x='count', color='outcome:N', title="")
        )

    st.divider()