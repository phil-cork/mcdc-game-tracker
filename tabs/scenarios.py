import streamlit as st
from utils.charts import bar_chart

def render(game_df):

    st.title("Scenarios")

    scenario_col, difficulty_col = st.columns(2)

    with scenario_col:
        st.header("Scenarios")
        st.altair_chart(
            bar_chart(game_df,
                    y='scenario:N', x='count', color='outcome:N',
                     colorScheme='scenario', title='')
        )

    with difficulty_col:
        st.header("Difficulty")
        st.altair_chart(
            bar_chart(game_df,
                    y='difficulty:N', x='count', color='outcome:N', colorScheme='scenario', title="")
        )