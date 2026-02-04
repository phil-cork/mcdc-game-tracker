import streamlit as st
import pandas as pd
import altair as alt
from utils.charts import bar_chart, heatmap_chart
from utils.data_loader import get_heatmap_data

def render(heatmap_df):

    st.title("Hero/Aspect Heatmap")

    col1, col2, col3 = st.columns(3, gap='xsmall')

    with col1:

        heatmap = heatmap_chart(heatmap_df.iloc[0:138,:], x='individual_aspect', y='hero', color='value',
                            x_title="Aspect", y_title="Hero", color_title="Value")

        st.altair_chart(heatmap, use_container_width=False)

    with col2:

        heatmap = heatmap_chart(heatmap_df.iloc[138:276, :], x='individual_aspect', y='hero', color='value',
                            x_title="Aspect", y_title="Hero", color_title="Value")

        st.altair_chart(heatmap, use_container_width=False)

    with col3:

        heatmap = heatmap_chart(heatmap_df.iloc[276:,:], x='individual_aspect', y='hero', color='value',
                            x_title="Aspect", y_title="Hero", color_title="Value")

        st.altair_chart(heatmap, use_container_width=False)

