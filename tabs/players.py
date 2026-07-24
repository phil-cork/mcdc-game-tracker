import streamlit as st
from utils.charts import bar_chart

def render(player_df):

    st.header("Most Games Played")

    most_games_played = player_df.groupby(['name']).aggregate(plays=('name', 'count')).reset_index()
    
    games_bar = bar_chart(most_games_played,
                  y='name', x='plays', title="", text='plays')
    
    st.altair_chart(games_bar)