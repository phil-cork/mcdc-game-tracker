import streamlit as st
from utils.charts import bar_chart

def render(player_df):

    st.title("Player Leaderboards")

    st.header("Most Games Played")

    most_games_played = player_df.groupby(['name']).aggregate(plays=('name', 'count')).reset_index()
    
    games_bar = bar_chart(most_games_played,
                  y='name', x='plays', title="", text='plays')
    
    st.altair_chart(games_bar)


    st.header("Most Heroes Played")

    most_heroes_df = (player_df[['name', 'hero']].drop_duplicates()
                     .groupby(['name'])
                     .aggregate(plays=('name', 'count'))).reset_index()

    hero_bar = bar_chart(most_heroes_df,
                  y='name', x='plays', title="", text='plays')

    
    st.altair_chart(hero_bar)