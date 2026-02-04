import streamlit as st
from utils.charts import bar_chart
from utils.data_loader import explode_with_weights, replace_with_other

def render(aspect_df):

    st.title("Heroes")
   
    st.altair_chart(
        bar_chart(aspect_df,
                  y='hero:N', x='value', title="",
                  color='individual_aspect:N', colorScheme='aspect',
                  height=1200, width=600
                  )
    )