import streamlit as st
from utils.charts import dot_matrix_plot, aspect_sort_order
from utils.data_loader import hero_list


def render(heatmap_df):

    st.header("Hero & Aspect Heatmap")
    st.markdown("Can we fill in every hero and aspect over the course of the weekend? Let's find out!")

    col1, col2, col3 = st.columns(3, gap='xsmall')

    with col1:

        hero_list_a = hero_list[:23]
        heatmap_df_a = heatmap_df[heatmap_df['hero'].isin(hero_list_a)]

        st.altair_chart(dot_matrix_plot(heatmap_df_a, x='aspect', y='hero', x_sort_order=aspect_sort_order))

    with col2:

        hero_list_b = hero_list[23:46]
        heatmap_df_b = heatmap_df[heatmap_df['hero'].isin(hero_list_b)]

        st.altair_chart(dot_matrix_plot(heatmap_df_b, x='aspect', y='hero', x_sort_order=aspect_sort_order))

    with col3:

        hero_list_c = hero_list[46:]
        heatmap_df_c = heatmap_df[heatmap_df['hero'].isin(hero_list_c)]

        st.altair_chart(dot_matrix_plot(heatmap_df_c, x='aspect', y='hero', x_sort_order=aspect_sort_order))