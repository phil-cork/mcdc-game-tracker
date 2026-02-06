import streamlit as st
from utils.charts import bar_chart, donut_chart

def render(aspect_df):

    st.title("Aspects")

    aspects_played = aspect_df.groupby('individual_aspect').aggregate(plays=('value', 'sum')).reset_index()
   
    col1, col2 = st.columns([2,1])

    with col1:
        st.altair_chart(
        bar_chart(aspects_played,
                  y='individual_aspect:N', x='plays', title="",
                  color='individual_aspect:N', colorScheme='aspect',
                  height=600, width=600, text='plays'))
        
    with col2:
        st.altair_chart(donut_chart(aspects_played, category_col='individual_aspect',
                                    value_col='plays', colorScheme='aspect'))