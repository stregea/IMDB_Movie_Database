"""
File for data visualization.
Make different types of graphs.
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


# set the seaborn theme for the visualizations
sns.set()


def histogram(df: pd.DataFrame, attribute_to_visualize: str, attributes: tuple[str, str]) -> None:
    """
    Display a Histogram visualization
    :param df: Pandas dataframe containing the information to visualize.
    :param attribute_to_visualize: Semantic variable that is mapped to determine the color of plot elements.
    :param attributes: Tuple that contains the variables that specify positions on the x and y axes.
    """
    sns.histplot(data=df, hue=attribute_to_visualize, x=attributes[0], y=attributes[1], multiple="stack")
    plt.show()


def make_histogram_checker():
    """
    run unique values function for all non-numeric data attributes.
    If less than 15 unique values, then make histogram for each.
    (Calls histogram() )
    """
    pass


def bar_chart(df: pd.DataFrame) -> None:
    """
    Display a Histogram visualization
    :param df: Pandas dataframe containing the information to visualize.
    """
    pass


def pie_chart(df: pd.DataFrame) -> None:
    """
    Display a Histogram visualization
    :param data_frame: Pandas dataframe containing the information to visualize.
    """
    pass


def scatter_plot(df: pd.DataFrame) -> None:
    """
    Display a Histogram visualization
    :param df: Pandas dataframe containing the information to visualize.
    """
    pass
