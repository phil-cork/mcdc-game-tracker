import streamlit as st

st.set_page_config(layout="wide")

def render(df, game_df, player_df, full_df):

    st.title("DEMO DATA VIEW")

    st.header("Live Google Sheet Data")
    st.dataframe(df)

    ### Game DF Section
    st.header("Game DF")
    st.dataframe(game_df)

    st.header("Player DF")
    st.dataframe(player_df)

    st.header("Full DF")
    st.dataframe(full_df)