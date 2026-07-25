import streamlit as st
from utils.charts import bar_chart

def render(region_df):

    st.header("Total Games Played By Region")

    games_bar = bar_chart(region_df,
                  y='region', x='plays', title="", text='plays')

    st.altair_chart(games_bar)