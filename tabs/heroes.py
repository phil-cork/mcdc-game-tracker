import streamlit as st
from utils.charts import bar_chart
from utils.data_loader import explode_with_weights, replace_with_other

def render(player_df):

    st.title("Heroes")

    aspect_df = explode_with_weights(player_df, 'aspect', 'individual_aspect')
    aspect_df = replace_with_other(aspect_df,
                                   allowed_set = set(['Aggression', 'Basic', 'Leadership', 'Justice', 'Pool', 'Protection']),
                                   col='individual_aspect')
   
    st.altair_chart(
        bar_chart(aspect_df,
                  y='hero:N', x='value', title="",
                  color='individual_aspect:N', colorScheme='aspect',
                  height=1200, width=600
                  )
    )