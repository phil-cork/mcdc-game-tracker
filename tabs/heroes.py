import streamlit as st
from utils.charts import bar_chart

def render(aspect_df):

    st.title("Heroes Played By Aspect")
   
    st.altair_chart(
        bar_chart(aspect_df,
                  y='hero', x='plays', title="",
                  color='aspect', colorScheme='aspect',
                  height=1200, width=600
                  )
    )