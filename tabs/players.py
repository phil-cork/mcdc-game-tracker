import streamlit as st
from utils.charts import bar_chart

def render(player_df):

    st.title("Player Leaderboards")


    st.altair_chart(
        bar_chart(player_df,
                  y='name:N', x='count', title=""
                  )
    )