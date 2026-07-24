import streamlit as st
from utils.charts import bar_chart, stacked_bar_chart

def render(aspect_df):

    st.header("Heroes Played By Aspect")

    st.altair_chart(
        stacked_bar_chart(aspect_df,
                          group_col='hero',
                          category_col='aspect',
                          count_col='plays',
                          color_scheme='aspect')
    )