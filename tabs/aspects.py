import streamlit as st
from utils.charts import bar_chart, donut_chart

def render(aspect_df):

    st.title("Decks Played by Aspect")
   
    col1, col2 = st.columns([2,1])

    with col1:
        st.altair_chart(
        bar_chart(aspect_df,
                  y='aspect', x='plays', title="",
                  color='aspect', colorScheme='aspect',
                  height=600, width=600, text='plays'))
        
    with col2:
        st.altair_chart(donut_chart(aspect_df, category_col='aspect',
                                    value_col='percent', colorScheme='aspect'))