"""
File for data visualization.
Make different types of graphs.
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# set the seaborn theme for the visualizations
sns.set()


def display_visualization(data: pd.DataFrame, visualization: str, attributes: tuple, **kwargs) -> None:
    """
    Display the data visualization.
    """
    if visualization.lower() == "histplot":
        sns.histplot(data=data, x=attributes[0], y=attributes[1], hue=kwargs['hue'], multiple=kwargs['multiple'])

    elif visualization.lower() == "barplot":
        sns.barplot(data=data, x=attributes[0], y=attributes[1])

    elif visualization.lower() == "scatterplot":
        sns.scatterplot(data=data, x=attributes[0], y=attributes[1], hue=kwargs['hue'])

    plt.show()


def histogram(df: pd.DataFrame, attribute_to_visualize: str, attributes: tuple) -> None:
    """
    Display a Histogram visualization.
    Reference: https://seaborn.pydata.org/generated/seaborn.histplot.html
    :param df: Pandas dataframe containing the information to visualize.
    :param attribute_to_visualize: Semantic variable that is mapped to determine the color of plot elements.
    :param attributes: Tuple that contains the variables that specify positions on the x and y axes.
    """
    display_visualization(data=df,
                          visualization="histplot",
                          attributes=attributes,
                          hue=attribute_to_visualize,
                          multiple="stack")


def make_histogram_checker():
    """
    run unique values function for all non-numeric data attributes.
    If less than 15 unique values, then make histogram for each.
    (Calls histogram() )
    """
    pass


def bar_chart(df: pd.DataFrame, attributes: tuple[str, str]) -> None:
    """
    Display a Bar Plot visualization.
    Reference: https://seaborn.pydata.org/generated/seaborn.barplot.html
    :param df: Pandas dataframe containing the information to visualize.
    :param attributes: Tuple that contains the variables that specify positions on the x and y axes.
    """
    display_visualization(data=df,
                          visualization="barplot",
                          attributes=attributes)


def pie_chart(df: pd.DataFrame, attribute_to_plot, labels_for_attribute) -> None:
    """
    TODO: This has not been tested at all. Look back into later while working on
    TODO: the creation of the dataframes to send in.
    Display a Pie Chart visualization.
    Reference: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pie.html
    Reference: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html
    :param df: Pandas dataframe containing the information to visualize.
    """
    values = df[attribute_to_plot]

    def get_exploding_values(list_of_values: list) -> tuple:
        """
        This function will determine which value is the largest in the list, and
        will return a tuple containing the information that will have the largest percentage
        within the pie chart pop off.
        :param list_of_values:
        :return: A tuple of 'exploding' values for a pie chart.
        """
        exploding_values = [0.0 for value in list_of_values]
        largest_value = list_of_values[0]
        pop_out_index = 0

        # iterate through the list of values and find the index that contains the largest value.
        for i, value in enumerate(list_of_values):
            if value > largest_value:
                largest_value = value
                pop_out_index = i

        # set the popout value
        exploding_values[pop_out_index] = 0.1

        return tuple(exploding_values)

    fig, ax = plt.subplots()

    ax.pie(values,
           explode=get_exploding_values(values),
           labels=labels_for_attribute,
           autopct='%1.1f%%',
           shadow=True,
           startangle=90)

    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


def scatter_plot(df: pd.DataFrame, attribute_to_visualize: str, attributes: tuple) -> None:
    """
    Display a Scatter Plot visualization.
    Reference: https://seaborn.pydata.org/generated/seaborn.scatterplot.html
    :param df: Pandas dataframe containing the information to visualize.
    :param attribute_to_visualize: Semantic variable that is mapped to determine the color of plot elements.
    :param attributes: Tuple that contains the variables that specify positions on the x and y axes.
    """
    display_visualization(data=df,
                          visualization="scatterplot",
                          attributes=attributes,
                          hue=attribute_to_visualize)
