import pandas as pd
import numpy as np
import streamlit as st
import re

hero_list = ["Black Panther (T'challa)", "Captain Marvel", "Ironman", "She-Hulk",
        "Spider-Man (Peter)", "Captain America", "Ms. Marvel", "Thor", 
        "Black Widow", "Doctor Strange", "Hulk", "Hawkeye", "Spider-Woman", 
        "Ant-Man", "Wasp", "Quicksilver", "Scarlet Witch", "Groot", "Rocket Racoon", 
        "Star-Lord", "Gamora", "Drax", "Venom", "Adam Warlock", "Spectrum", "Nebula",
        "War Machine", "Valkyrie", "Vision", "Ghost-Spider", "Spider-Man (Miles)",
        "Nova", "Ironheart", "Spider-Ham", "Sp//dr", "Colossus", "Shadowcat", "Cyclops",
        "Phoenix", "Wolverine", "Storm", "Gambit", "Rogue", "Cable", "Domino", "Psylocke",
        "Angel", "X-23", "Deadpool", "Magik", "Bishop", "Iceman", "Jubilee", "Nightcrawler",
        "Magneto", "Maria Hill", "Nick Fury", "Black Panther (Shuri)", "Silk", "Falcon",
        "Winter Soldier", "Tigra", "Hulkling", "Wonder Man", "Hercules", "Daredevil", "Echo",
        "Jessica Jones", "Luke Cage"]

hero_list.sort()

aspect_list = ['Aggression', 'Justice', 'Leadership', 'Protection',
                   'Pool', "Basic", "Multi-Aspect"]

def run_data_pipeline(df, region:str):

    # before filtering down to region, create a copy for regional comparison
    region_df = df.copy()
    region_df = region_df.groupby(['region']).aggregate(plays=('submission_id', 'count')).reset_index()

    # if filter selected, filter down
    if region != 'All':
        df = df[df['region']==region]
    
    # for stats, keep only relevant columns
    game_df = df[['submission_id', 'submission_time', 'region', 'number_of_players',
              'scenario', 'difficulty', 'skirmish_mode', 'outcome']].copy().drop_duplicates()
    # condensing down to standard and expert for plotting
    game_df['difficulty'] = np.where(game_df['difficulty'].str.contains('Standard'), "Standard", "Expert")
    
    # for scenarios, group by the scenario name and difficulty, 
    scenario_df = game_df.groupby(['scenario', 'difficulty']).aggregate(plays=('submission_id', 'count')).reset_index()
    
    # pivot players from wider to longer
    player_df = reshape_players(df)
    # drop all custom aspects, if any, to Other
    player_df = replace_with_other(player_df,
                                   allowed_set = set(['Aggression', 'Basic', 'Leadership', 'Justice', 
                                                      'Pool', 'Protection', 'Multi-Aspect']),
                                   col='aspect')
    player_df = pd.merge(player_df, game_df[['submission_id', 'difficulty']], on='submission_id')
    
    # for heroes, aggregate both by hero and aspect for stacked bar chart
    hero_aspect_df = player_df.groupby(['hero', 'aspect']).aggregate(plays=('submission_id', 'count')).reset_index()


    # for aspects, total up only aspect plays, then calculate percentages for donut chart
    aspect_df = player_df.groupby('aspect').agg(plays=('submission_id', 'count')).reset_index()
    aspect_df['percent'] = round(aspect_df['plays'] / sum(aspect_df['plays']), 3)*100
    
    # generate heatmap data in separate function
    heatmap_df = get_heatmap_data(player_df[['hero', 'aspect']])


    return game_df, scenario_df, player_df, hero_aspect_df, aspect_df, heatmap_df, region_df


def load_data():
    df = pd.read_csv(st.secrets["sheets"]["spreadsheet"])
    df = normalize_column_names(df)
    return df


def clean_name(name):
    # Lowercase
    name = name.lower()
    # Replace non-alphanumeric with underscore
    name = re.sub(r'[^a-z0-9]+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    return name


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:    
    # Avoid modifying original df
    df = df.copy()
    df.columns = [clean_name(col) for col in df.columns]
    return df


def reshape_players(
    df: pd.DataFrame,
    id_col: str = 'submission_id',
    player_pattern: str = r'_player_\d+$'
) -> pd.DataFrame:
    """
    Reshape wide player columns (e.g. name_player_1, hero_player_1, ...)
    into a long, per-player dataframe.

    Players whose entire set of features is NA are dropped.
    Feature column order matches the original dataframe.
    """

    # identify player columns that contain _player_ pattern
    player_cols = df.columns[df.columns.str.contains(player_pattern)]

    # same feature order for later output
    feature_order = (
        pd.Series(player_cols)
        .str.replace(r'_player_\d+$', '', regex=True)
        .drop_duplicates()
        .tolist()
    )

    # melt into long format
    long = df.melt(
        id_vars=id_col,
        value_vars=player_cols,
        var_name='variable',
        value_name='value'
    )

    # from the long format, extract the feature (name, hero, aspect) and the player number 
    # and store it in a dataframe that is the 'variable' column, split across two columns
    extracted = long['variable'].str.extract(
        r'^(?P<feature>.+)_player_(?P<player_num>\d+)$'
    )

    # create new columns in the long df, assigning them from the values stored in extracted
    long = long.assign(
        feature=extracted['feature'],
        player_num=extracted['player_num'].astype(int)
    ).drop(columns='variable')

    # with the split column names, transform the features extracted back into columns
    player_df = (
        long
        .pivot_table(
            index=[id_col, 'player_num'],
            columns='feature',
            values='value',
            aggfunc='first')
    )

    # drop rows where all player info is NA (player 4 in a 3p game)
    player_df = player_df.dropna(how='all')

    # reorder feature columns to match original dataframe
    player_df = player_df.reindex(columns=feature_order)

    # cleanup for return
    player_df = player_df.reset_index()
    player_df.columns.name = None

    return player_df


def replace_with_other(df, allowed_set:set, col:str):
    df[col] = df[col].where(df[col].isin(allowed_set), "Other")
    return df


def get_heatmap_data(current_form_df):

    # create a new column that gives each entry a count of 1
    # to test abensence with fillna below
    current_form_df['value'] = 1
    
    heatmap_df = pd.MultiIndex.from_product(
            [hero_list, aspect_list],
            names=['hero', 'aspect']
        ).to_frame(index=False)
    
    heatmap_df = pd.merge(heatmap_df, current_form_df, how='left', on=['hero', 'aspect']).fillna(0)
    heatmap_df.sort_values(by='hero', inplace=True)
    heatmap_df = heatmap_df.reset_index().drop('index', axis=1)
    heatmap_df = heatmap_df.drop_duplicates()

    heatmap_df['value'] = np.where(heatmap_df['value'] > 0, 1, 0)

    multi_aspect_heroes = ['Adam Warlock', 'Spider-Woman']
    # drop multi-aspect from list
    non_ma_aspects = aspect_list[:6]


    heatmap_df['value'] = heatmap_df['value'].case_when([
    # make all multi-aspect heroes NA for everything but MA
    (
        (heatmap_df['hero'].isin(multi_aspect_heroes)) & (heatmap_df['aspect'].isin(non_ma_aspects)),
        np.nan
    ),
    # for all heroes not MA, set it to NA
    (
        (~heatmap_df['hero'].isin(multi_aspect_heroes)) & (heatmap_df['aspect'] == "Multi-Aspect"),
        np.nan
    )
])

    return heatmap_df