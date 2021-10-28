"""
'Specific' functions that call functions from analysis.py
"""

import pandas as pd
from scripts.data_analysis.analysis_functionality.analysis import get_genre_information, get_run_time_mins_information, get_averageRating_information, get_region_information
from scripts.data_analysis.data_visualization.visualization import display_visualization

def average_average_ratings_vs_genre():
    """
    ( Specific function )
    Bivariate.
    Gets the average of 'average ratings' per genre.
    Will be displayed using bar chart.
    """

    # get the necessary dataframes
    genres_df = get_genre_information()
    averageRating_df = get_averageRating_information()

    # coerce averageRating_df to a float
    averageRating_df["averageRating"] = pd.to_numeric(averageRating_df["averageRating"], errors="coerce")

    # reset indicies
    averageRating_df.index = genres_df.index

    # concatenate the two datasets
    concatenated_df = pd.concat([genres_df, averageRating_df], axis=1)

    # average by group
    grouped_df = concatenated_df.groupby("genres", as_index=False).mean()

    display_visualization(grouped_df, 'barplot', ("genres", "averageRating"))

    return

def average_run_time_per_genre():
    """
    ( Specific function )
    Bivariate.
    Gets the average of runtimemins per genre.
    Will be displayed using bar chart.
    """
    
    # get the necessary dataframes
    genres_df = get_genre_information()
    runtimeMins_df = get_run_time_mins_information()

    # coerce runtimeMins_df to a float
    runtimeMins_df["runtimeMinutes"] = pd.to_numeric(runtimeMins_df["runtimeMinutes"], errors="coerce")

    # reset indicies
    runtimeMins_df.index = genres_df.index

    # concatenate the two datasets
    concatenated_df = pd.concat([genres_df, runtimeMins_df], axis=1)

    # average by group
    grouped_df = concatenated_df.groupby("genres", as_index=False).mean()

    display_visualization(grouped_df, 'barplot', ("genres", "runtimeMinutes"))

    return

def average_rating_vs_run_time_mins():
    """
    ( Specific function )
    Bivariate.
    Gets the average of runtimemins per genre.
    Will be displayed using bar chart.
    """
    
    # get the necessary dataframes
    averageRating_df = get_averageRating_information()
    runtimeMins_df = get_run_time_mins_information()

    # coerce to a float
    runtimeMins_df["runtimeMinutes"] = pd.to_numeric(runtimeMins_df["runtimeMinutes"], errors="coerce")
    averageRating_df["averageRating"] = pd.to_numeric(averageRating_df["averageRating"], errors="coerce")

    # get quantile and remove outliers
    q = runtimeMins_df["runtimeMinutes"].quantile(0.99)
    runtimeMins_df = runtimeMins_df[runtimeMins_df["runtimeMinutes"] < q]

    # concatenate the two datasets
    concatenated_df = pd.concat([averageRating_df, runtimeMins_df], axis=1)

    display_visualization(concatenated_df, 'lineplot', ("runtimeMinutes", "averageRating"))

    return

