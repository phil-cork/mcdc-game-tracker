import streamlit as st
from utils.charts import stacked_bar_chart

def render(game_df):

    st.header("Scenarios Played By Difficulty")
    st.altair_chart(
        stacked_bar_chart(game_df,
                    group_col='scenario', category_col='difficulty', count_col='plays',
                     color_scheme='difficulty')
        )
