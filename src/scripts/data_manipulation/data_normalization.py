from math import e
import numpy as np
from numpy.core.fromnumeric import mean, std
import tensorflow as tf
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import os
from utils.globals import DATASETS

EPOCHS = 3
BATCH_SIZE = 1


def run_normalization_tests() -> None:
    """
    General function that sets up the data and runs it throughout the individual tests
    """

    file_name = os.path.abspath(DATASETS + "/Combined/final.output.tsv")

    if os.path.isfile(file_name):

        # Get the dataframe
        original_dataframe = pd.read_csv(file_name, sep="\t", dtype={
            'isOriginalTitle': str,
            'averageRating': str,
            'numVotes': str,
            'startYear': str,
            'runtimeMinutes': str
        })

        # Get the target array which is basically whether it's of genre Drama or not
        target = original_dataframe.pop('genres')
        target_array = target.to_numpy()
        for i in range(len(target_array)):
            if target_array[i] == 'Drama':
                target_array[i] = 1
            else:
                target_array[i] = 0
        target_array = target_array.astype(int)

        # Get array of just numeric features and temporarily replace missing values with 0s
        numeric_features_names = ['averageRating', 'numVotes', 'startYear', 'runtimeMinutes', 'birthYear', 'deathYear']
        numeric_features = original_dataframe[numeric_features_names]
        numeric_features.loc[(numeric_features['averageRating'] == '\\N'), 'averageRating'] = 0
        numeric_features.loc[(numeric_features['numVotes'] == '\\N'), 'numVotes'] = 0
        numeric_features.loc[(numeric_features['startYear'] == '\\N'), 'startYear'] = 0
        numeric_features.loc[(numeric_features['runtimeMinutes'] == '\\N'), 'runtimeMinutes'] = 0
        numeric_features.loc[(numeric_features['birthYear'] == '\\N'), 'birthYear'] = 0
        numeric_features.loc[(numeric_features['deathYear'] == '\\N'), 'deathYear'] = 0

        # Convert above array for use in tensorflow
        numeric_nparray = numeric_features.to_numpy().astype('float32')
        tf.convert_to_tensor(numeric_nparray, dtype=tf.float32)

        baseline_test(numeric_nparray.copy(), target_array)
        minmax_test(numeric_nparray.copy(), target_array)
        sigmoidal_test(numeric_nparray.copy(), target_array)
        softmax_test(numeric_nparray.copy(), target_array)
    else:
        print("Error: final.output.tsv not found.")


def get_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
        metrics=['accuracy']
    )

    return model


def baseline_test(numeric_features, target) -> None:
    """
    Run the data (as is) through the keras model as a baseline test
    """

    model = get_model()

    print("Baseline results -----------------------------------------------------------------------")
    model.fit(numeric_features, target, epochs=EPOCHS, batch_size=BATCH_SIZE)
    print("----------------------------------------------------------------------------------------\n\n")


def minmax_test(numeric_features, target) -> None:
    """
    Run normalized data (using minmax normalization) through the keras model
    """

    model = get_model()

    # Min-max normalization
    for i in range(len(numeric_features[0])):
        column = numeric_features[:,i]
        min_col = min(column)
        max_col = max(column)
        for j in range(len(numeric_features)):
            new_value = (column[j] - min_col) / (max_col - min_col)
            numeric_features[j][i] = new_value

    print("Min-max results ----------------------------------------------------------------------")
    model.fit(numeric_features, target, epochs=EPOCHS, batch_size=BATCH_SIZE)
    print("--------------------------------------------------------------------------------------\n\n")


def sigmoidal_test(numeric_features, target) -> None:
    """
    Run normalized data (using sigmoidal normalization) through the keras model
    """

    model = get_model()

    # Sigmoidal normalization
    for i in range(len(numeric_features[0])):
        column = numeric_features[:,i]
        mean_col = mean(column)
        stdv_col = std(column)
        for j in range(len(numeric_features)):
            new_value = (column[j] - mean_col) / stdv_col
            numeric_features[j][i] = new_value

    print("Sigmoidal results ------------------------------------------------------------------------")
    model.fit(numeric_features, target, epochs=EPOCHS, batch_size=BATCH_SIZE)
    print("------------------------------------------------------------------------------------------\n\n")


def softmax_test(numeric_features, target) -> None:
    """
    Run normalized data (using softmax normalization) through the keras model
    """

    model = get_model()

    # Softmax normalization
    for i in range(len(numeric_features[0])):
        column = numeric_features[:,i]
        mean_col = mean(column)
        stdv_col = std(column)
        for j in range(len(numeric_features)):
            a = (column[j] - mean_col) / stdv_col
            numeric_features[j][i] = 1 / (1 + pow(e, -1 * a))

    print("Softmax results ----------------------------------------------------------------------")
    model.fit(numeric_features, target, epochs=EPOCHS, batch_size=BATCH_SIZE)
    print("--------------------------------------------------------------------------------------\n\n")


