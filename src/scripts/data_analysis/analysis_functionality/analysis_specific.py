"""
'Specific' functions that call functions from analysis.py
"""

import pandas as pd
from scripts.data_analysis.analysis_functionality.analysis import get_genre_information, get_run_time_mins_information, \
    get_averageRating_information, get_region_information, get_start_year_info, get_end_year_info
from scripts.data_analysis.data_visualization.visualization import display_visualization


def display_numeric_data() -> None:
    """
    Get data and display for ordering, averageRating, start year, end year, run time minutes
    """
    display_average_ratings()
    display_runtime()
    display_start_year()
    # display_end_year() #end year is /N so commented out this


def display_bivariate_data() -> None:
    """
    Display bivariate charts for: Average Ratings vs Genre
                                  Average Runtime vs Genre
                                  Average Rating vs Runtime Minutes
    """
    average_average_ratings_vs_genre()
    average_run_time_per_genre()
    average_rating_vs_run_time_mins()


def display_average_ratings() -> None:
    """
    Gets avg ratings info with premade function then displays
    """
    # get average ratings
    averageRating_df = get_averageRating_information()
    # coerce averageRating_df to a float
    averageRating_df["averageRating"] = pd.to_numeric(averageRating_df["averageRating"], errors="coerce")
    # box plot visual
    display_visualization(averageRating_df, 'boxplot', ("averageRating",))


def display_runtime() -> None:
    """
    Gets runtime info with premade function then displays
    """
    runtimeMins_df = get_run_time_mins_information()
    # coerce runtimeMins_df to a float
    runtimeMins_df["runtimeMinutes"] = pd.to_numeric(runtimeMins_df["runtimeMinutes"], errors="coerce")
    display_visualization(runtimeMins_df, 'boxplot', ("runtimeMinutes",))


def display_start_year() -> None:
    """
    Gets start year information and displays with box plot
    """
    startYear_df = get_start_year_info()
    startYear_df["startYear"] = pd.to_numeric(startYear_df["startYear"], errors="coerce")
    display_visualization(startYear_df, 'boxplot', ("startYear",))

# def display_end_year():
# #end year is /N so function is commented out
#     """
#     Gets end year information and displays with box plot
#     """
#     endYear_df = get_end_year_info()
#     endYear_df["startYear"] = pd.to_numeric(endYear_df["endYear"], errors="coerce")
#     display_visualization(endYear_df, 'boxplot', ("endYear",))


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
