import streamlit as st
from utils.charts import bar_chart
from utils.data_loader import explode_with_weights

def render(player_df):

    st.title("Heroes")

    aspect_df = explode_with_weights(player_df, 'aspect')
    aspect_df.rename(columns={'item':'individual_aspect'}, inplace=True)

    # can't control for what aspects folks may type in, set all to Other for color scale
    allowed_set = set(['Aggression', 'Basic', 'Leadership', 'Justice', 'Pool', 'Protection'])
    aspect_df["individual_aspect"] = aspect_df["individual_aspect"].where(aspect_df["individual_aspect"].isin(allowed_set), "Other")

    st.altair_chart(
        bar_chart(aspect_df,
                  y='hero:N', x='value', title="",
                  color='individual_aspect:N', colorScheme='aspect',
                  height=1200, width=600
                  )
    )