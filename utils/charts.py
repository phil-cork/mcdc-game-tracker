import altair as alt
import pandas as pd

# create custom color schemes referenced throughout
color_scheme_map = {
    'aspect' : alt.Scale(
    domain=["Aggression", "Basic", "Justice", "Leadership",
            "Pool", "Protection", "Multi-Aspect", "Other"],
    range=['#FF4500', '#b4b4b4', '#FFD700', '#0086EB',
           'pink', '#00C853', "#8766C8", '#545454']),
    
    'scenario' : alt.Scale(
    domain=['Win', 'Loss'],
    range=['#518cca', '#f78f3f'])
    }

aspect_sort_order = ['Aggression', 'Justice', "Leadership", 'Protection',
                     'Pool', 'Basic', 'Multi-Aspect']


def donut_chart(df: pd.DataFrame, category_col: str, value_col: str = None,
                title: str = "", colorScheme = None) -> alt.Chart:
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
    colorScheme: str, optional
        sets color Scale based on key provided. If None, altiar default

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

    if colorScheme not in color_scheme_map:
        color_encoding = alt.Color(f"{category_col}:N",
                                   legend=alt.Legend(title=category_col, orient='bottom-right'))

    else:
        color_encoding = alt.Color(
            f"{category_col}:N",
            scale=color_scheme_map[colorScheme],
            legend=None)
            
    pie = (
        alt.Chart(df_plot)
        .mark_arc(innerRadius=50)  # innerRadius makes it a donut
        .encode(
            theta=alt.Theta(field="angle", type="quantitative"),
            color=color_encoding,
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
              height=1800,
              width=300,
              title=None):

    
    # Handle y-axis: count if None or 'count'
    if y is None or (isinstance(y, str) and y.lower() == "count"):
        y_enc = alt.Y('count()', title='Count', axis=alt.Axis(format='d', title="", tickMinStep=1))
        height = max(len(df[y].drop_duplicates())*30,600)
    else:
        y_enc = alt.Y(y, title=str(y), axis=alt.Axis(labelLimit=300, title="", tickMinStep=1), sort='-x')
        height = max(len(df[y].drop_duplicates())*30,600)

    if x is None or (isinstance(x, str) and x.lower() == "count"):
        x_enc = alt.X('count()', title='Count', axis=alt.Axis(format='d', title="", tickMinStep=1))
        height = max(len(df[y].drop_duplicates())*30,600)
    else:
        x_enc = alt.X(x, title=str(x), axis=alt.Axis(labelLimit=300, title="", tickMinStep=1), sort='-y')
        height = max(len(df[y].drop_duplicates())*30,600)
    
    # Prepare encodings
    encodings = {
        "x": x_enc,
        "y": y_enc
    }
    
    if color is not None and colorScheme is None:
        encodings["color"] = alt.Color(color, title=str(color),
                                       legend=alt.Legend(orient='bottom'))

    elif color is not None and colorScheme == 'aspect':
        encodings['color'] = alt.Color(color, title=str(color),
                                       scale=color_scheme_map[colorScheme],
                                       legend=alt.Legend(orient='bottom'))
    
    elif color is not None and colorScheme == 'scenario':
        encodings['color'] = alt.Color(color, title=str(color),
                                       scale=color_scheme_map[colorScheme],
                                       legend=alt.Legend(orient='bottom'))


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
        dx=8,    
        color='white',
        size=16
    ).encode(
        text=text
    )
        return chart + chart_text

    else:
        return chart
    

def dot_matrix_plot(df, x:str, y:str, x_sort_order=[]):
    
    base = alt.Chart(df)

    # Horizontal guide line per row, spanning all columns
    lines = base.mark_line(color='darkgrey', strokeWidth=.5).encode(
        x=alt.X(f'{x}:N', axis=alt.Axis(orient='top'), title=None, sort=x_sort_order),
        y=alt.Y(f'{y}:N', sort='ascending', title=None, axis=alt.Axis(labelLimit=300)),
        detail=f'{y}:N'   # keeps each row's line separate
    )

    dots_df = df.dropna()

    # Dots on top
    dots = alt.Chart(dots_df).mark_circle(size=250).encode(
        x=alt.X(f'{x}:N', sort=x_sort_order),
        y=alt.Y(f'{y}:N', sort='ascending'),
        color=alt.Color('aspect:N', scale=color_scheme_map.get('aspect'), legend=None),
        opacity=alt.condition(alt.datum.value, alt.value(1.0), alt.value(0.15))
    )

    return (lines + dots)