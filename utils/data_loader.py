import pandas as pd
import numpy as np
import streamlit as st
import re

def run_data_pipeline():
    df = load_data()
    df = normalize_column_names(df)

    game_df = df[['submission_id', 'submission_time', 'region', 'number_of_players',
              'scenario', 'difficulty', 'skirmish_mode', 'outcome']].copy().drop_duplicates()
    player_df = reshape_players(df)
    player_df = merge_aspects(player_df)

    aspect_df = explode_with_weights(player_df, 'aspect', 'individual_aspect')
    aspect_df = replace_with_other(aspect_df,
                                   allowed_set = set(['Aggression', 'Basic', 'Leadership', 'Justice', 'Pool', 'Protection']),
                                   col='individual_aspect')
    
    heatmap_df = get_heatmap_data(aspect_df[['hero', 'individual_aspect', 'value']])

    full_df = pd.merge(player_df, game_df, how='left', on='submission_id')

    return df, game_df, player_df, aspect_df, heatmap_df, full_df


def load_data():
    df = pd.read_csv(st.secrets["sheets"]["spreadsheet"])
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

    # from the long format, extract the feature (name, her, aspect) and the player number 
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


def merge_aspects(df):
    # merge aspect and multi-aspect together
    df['aspect'] = df['aspect'].fillna(df['multi_aspect'])
    df.drop('multi_aspect', axis=1, inplace=True)
    return df


def most_frequent_value(df: pd.DataFrame, column: str) -> str:
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame.")
    
    # Use value_counts for efficiency
    most_freq = df[column].value_counts().idxmax()
    
    # Convert to string before returning
    return str(most_freq)


def explode_with_weights(df, col, new_col, sep=", "):

    # Split into lists
    df = df.copy()
    df["_items"] = df[col].str.split(sep)

    # Number of items per row
    df["_n_items"] = df["_items"].str.len()

    # Explode
    out = df.explode("_items")

    # Assign value = 1 / number of items
    out["value"] = 1 / out["_n_items"]

    # Clean up
    out = out.drop(columns=["_n_items"]).rename(columns={"_items": new_col})

    return out


def replace_with_other(df, allowed_set:set, col:str):
    df[col] = df[col].where(df[col].isin(allowed_set), "Other")
    return df


def get_heatmap_data(current_form_df):

    aspect_list = ['Aggression', 'Basic', 'Justice', 'Leadership',
                                       'Pool', "Protection"]
    
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

    heatmap_df = pd.MultiIndex.from_product(
            [hero_list, aspect_list],
            names=['hero', 'individual_aspect']
        ).to_frame(index=False)
    
    heatmap_df = pd.merge(heatmap_df, current_form_df, how='left', on=['hero', 'individual_aspect']).fillna(0)
    heatmap_df.sort_values(by='hero', inplace=True)
    heatmap_df = heatmap_df.reset_index().drop('index', axis=1)
    heatmap_df = heatmap_df.drop_duplicates()

    heatmap_df['value'] = np.where(heatmap_df['value'] > 0, 1, 0)

    return heatmap_df