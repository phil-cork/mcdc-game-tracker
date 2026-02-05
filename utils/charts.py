import altair as alt
import pandas as pd
import streamlit as st

aspect_color_scheme = alt.Scale(
    domain=["Aggression", "Basic", "Justice", "Leadership",
            "Pool", "Protection", "Other"],
    range=['#FF4500', 'lightgrey', '#FFD700', '#0086EB',
           'pink', '#00C853', 'darkgrey']
)

scenario_color_scheme = alt.Scale(
    domain=['Win', 'Loss'],
    range=['#518cca', '#f78f3f']
)

# The standard aspect colors in Marvel Champions: The Card Game correspond to specific HEX codes used for deck building and card identification. The approximate hex codes are: Aggression (Red) #FF4500 or #F7481D, Leadership (Yellow/Gold) #FFD700 or #FFC331, Justice (Blue) #0086EB or #0052F2, and Protection (Green) #00C853 or #3DA35A. 

def donut_chart(df: pd.DataFrame, category_col: str, value_col: str = None, title: str = "") -> alt.Chart:
    """
    Create a donut chart in Altair.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing the data
    category_col : str
        Column name for categorical variable
    value_col : str, optional
        Column with values/counts. If None, counts each category
    title : str, optional
        Chart title

    Returns
    -------
    alt.Chart
        Donut chart as an Altair object
    """

    # If no value column, count occurrences
    if value_col is None:
        df_plot = df.groupby(category_col).size().reset_index(name="count")
        value_col = "count"
    else:
        df_plot = df.groupby(category_col)[value_col].sum().reset_index()

    # Compute angles
    df_plot["angle"] = df_plot[value_col] / df_plot[value_col].sum()

    # Base pie chart
    pie = (
        alt.Chart(df_plot)
        .mark_arc(innerRadius=50)  # innerRadius makes it a donut
        .encode(
            theta=alt.Theta(field="angle", type="quantitative"),
            color=alt.Color(field=category_col, type="nominal", legend=alt.Legend(title=category_col)),
            tooltip=[alt.Tooltip(category_col), alt.Tooltip(value_col)]
        )
        .properties(title=title, width=400, height=400)
    )

    return pie


def bar_chart(df: pd.DataFrame,
              x=None,
              y=None,
              *,
              color=None,
              colorScheme=None,
              text=None,
              height=600,
              width=300,
              title=None):

    
    # Handle y-axis: count if None or 'count'
    if y is None or (isinstance(y, str) and y.lower() == "count"):
        y_enc = alt.Y('count()', title='Count', axis=alt.Axis(format='d'))
    else:
        y_enc = alt.Y(y, title=str(y), axis=alt.Axis(labelLimit=300), sort='-x')

    if x is None or (isinstance(x, str) and x.lower() == "count"):
        x_enc = alt.X('count()', title='Count', axis=alt.Axis(format='d'))
    else:
        x_enc = alt.X(x, title=str(x), axis=alt.Axis(labelLimit=300), sort='-y')
    
    # Prepare encodings
    encodings = {
        "x": x_enc,
        "y": y_enc
    }
    
    if color is not None and colorScheme is None:
        encodings["color"] = alt.Color(color, title=str(color))

    elif color is not None and colorScheme == 'aspect':
        encodings['color'] = alt.Color(color, title=str(color),
                                       scale=aspect_color_scheme)
    
    elif color is not None and colorScheme == 'scenario':
        encodings['color'] = alt.Color(color, title=str(color),
                                       scale=scenario_color_scheme)


    # Build chart
    chart = alt.Chart(df).mark_bar().encode(**encodings).properties(
        height=height,
        width=width,
        title=title
    )
    
    if text is not None:
        chart_text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=10,    
        color='white',
        size=16
    ).encode(
        text=text
    )
        return chart + chart_text

    else:
        return chart
    

def heatmap_chart(df, x:str, y:str, color:str,
                  x_title:str, y_title:str, color_title:str):

    heatmap = (
        alt.Chart(df)
        .mark_rect(stroke="grey",
        strokeWidth=1)
        .encode(
            x=alt.X(
                f"{x}:N",
                title="",
                sort="ascending",
                axis=alt.Axis(orient="top", labelAngle=-45)
            ),
            y=alt.Y(
                f"{y}:N",
                title="",
                sort="ascending",
                axis=alt.Axis(labelLimit=300)
            ),
            color=alt.Color(
                "value:N",
                title="Played",
                legend=None,
                scale=alt.Scale(domain=[0,1], range=['black', '#0086EB'])
            ),
            tooltip=[
                alt.Tooltip(x, title=x_title),
                alt.Tooltip(y, title=y_title),
                alt.Tooltip(color, title=color_title)
            ]
        )
        .properties(
            width=450,
            height=800
        )
    )

    return heatmap


def smart_metric(label: str, value: str):
    """
    Streamlit metric replacement for dark mode:
    - Fixed height to align with other metrics
    - Auto-shrinking font for long values
    - Dark mode styling
    """
    container_height = 100  # pixels

    # Auto-shrink font size based on value length
    value_length = len(str(value))
    value_font = max(20, min(60, container_height // 2 - value_length))  # shrink if too long
    label_font = max(12, value_font // 2.5)

    st.markdown(f"""
    <div style="
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        text-align:center;
        border:1px solid #262730;  /* dark mode border */
        border-radius:8px;
        padding:10px;
        height:{container_height}px;
        box-sizing:border-box;
        background-color:var(--stMetricBackgroundColor, #1e1e25);  /* dark background */
    ">
        <div style="font-size:{label_font}px; color:#d3d3d3; margin-bottom:3px;">{label}</div>
        <div style="font-size:{value_font}px; font-weight:600; line-height:1.1; color:white;">{value}</div>
    </div>
    """, unsafe_allow_html=True)


