import streamlit as st

st.set_page_config(layout="wide")

def render(game_df, player_df):

    st.header("MC/DC Gameplay Stats")

    metric_1, metric_2 = st.columns(2)
    metric_3, metric_4 = st.columns(2)
    metric_5, metric_6 = st.columns(2)

    metric_1.metric(value=len(game_df.submission_id.drop_duplicates().dropna()),
                label="Total Games Played", border=True)
        
    metric_2.metric(value=len(player_df.name.drop_duplicates()),
                label="Total Players", border=True)
        
    metric_3.metric(value=len(game_df.scenario.drop_duplicates().dropna()),
                    label="Total Scenarios Played", border=True)
    
    metric_4.metric(value=len(player_df.hero.drop_duplicates().dropna()),
                    label="Total Heroes Played", border=True)
    
    metric_5.metric(value=round(len(game_df.query("outcome=='Win'"))/len(game_df),2), format="percent",
                    label="Win Rate", border=True)

    metric_6.metric(value=player_df[['hero', 'aspect']].drop_duplicates().shape[0],
                    label="Total Hero & Aspect Combinations", border=True)