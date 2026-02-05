import streamlit as st
from utils.charts import bar_chart

def render(player_df, aspect_df):

    st.title("Player Leaderboards")

    st.header("Most Games Played")

    most_games_played = player_df.groupby(['name']).aggregate(plays=('name', 'count')).reset_index()
    
    games_bar = bar_chart(most_games_played,
                  y='name:N', x='plays', title="", text='plays')
    
    st.altair_chart(games_bar)


    st.header("Most Heroes Played")

    most_heroes_df = (player_df[['name', 'hero']].drop_duplicates()
                     .groupby(['name'])
                     .aggregate(plays=('name', 'count'))).reset_index()

    hero_bar = bar_chart(most_heroes_df,
                  y='name:N', x='plays', title="", text='plays')

    
    st.altair_chart(hero_bar)


    most_plays_df = (player_df[['name', 'hero', 'aspect']]
                     .groupby(['name', 'hero', 'aspect'])
                     .aggregate(plays=('name', 'count'))
    ).reset_index()

    # Define the styling function for individual cells
    def color_rating(aspect):
        if aspect == 'Aggression':
            color = '#FF4500'
        elif aspect == 'Basic':
            color = 'lightgrey'
        elif aspect == 'Leadership':
            color = '#0086EB'
        elif aspect == 'Justice':
            color = '#FFD700'
        elif aspect == 'Pool':
            color = 'pink'
        elif aspect == 'Protection':
            color = '#00C853'                                            
        else:
            color = 'grey'
        return f'background-color: {color}'

    styled_df = most_plays_df.style.map(color_rating, subset=['aspect'])

    st.header("Most Played Single Deck")
    st.dataframe(styled_df, use_container_width=True)