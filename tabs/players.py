import streamlit as st
from utils.charts import bar_chart, stacked_bar_chart

def render(player_df):

    st.header("Most Games Played")

    player_sb = st.selectbox("Display",
             ['Games Played', 'By Aspect', 'By Difficulty'],
             key='player_chart_filter')

    if player_sb == "Games Played":

        most_games_played = player_df.groupby(['name']).aggregate(plays=('name', 'count')).reset_index()
    
        player_bar_chart = bar_chart(most_games_played,
                  y='name', x='plays', title="", text='plays')

    elif player_sb == "By Aspect":

        most_games_played_aspect = player_df.groupby(['name', 'aspect']).aggregate(plays=('name', 'count')).reset_index()
        player_bar_chart = stacked_bar_chart(most_games_played_aspect, group_col='name', category_col='aspect', count_col='plays', color_scheme='aspect')

    elif player_sb == "By Difficulty":

        most_games_played_difficulty = player_df.groupby(['name', 'difficulty']).aggregate(plays=('name', 'count')).reset_index()
        player_bar_chart = stacked_bar_chart(most_games_played_difficulty, group_col='name', category_col='difficulty', count_col='plays', color_scheme='difficulty')


    st.altair_chart(player_bar_chart)