import os
import csv
import pandas as pd
import numpy as np

from utils.globals import COMBINED



def normalization_method(df):
    # df_file = os.path.abspath(os.path.join(COMBINED, 'dataframe.tsv'))
    attributes_to_change = ['averageRating', 'numVotes', 'startYear', 'runtimeMinutes', 'birthYear', 'deathYear']

    for a in attributes_to_change:
        column = [float(i) for i in df[a]]
        mean_col = pd.to_numeric(df[a], errors="coerce").mean(skipna=True) # mean
        std_col = pd.to_numeric(df[a], errors="coerce").std(skipna=True) # standard deviation
        p=1
        while p < len(df):
            #if column[p] != float:
            column[p] = float(str(column[p]))
            new_value = (column[p] - mean_col) / std_col
            column[p] = new_value
            p+=1
        df[a] = column

    return df



def remove_unwanted_attributes() -> None:
    """
    Remove unwanted attributes/columns from the dataset.
    """
    final_output_file = os.path.abspath(os.path.join(COMBINED, "final.output.tsv"))
    df_file = os.path.abspath(os.path.join(COMBINED, 'dataframe.tsv'))

    print(f"Removing attributes from '{final_output_file}'...")

    print(f"\tLoading dataframe from '{final_output_file}'...")
    dataframe = pd.read_csv(final_output_file,
                            delimiter='\t',
                            na_values='\\N',
                            index_col=False,
                            dtype=
                            {
                                'language': str,
                                'types': str,
                                'attributes': str,
                                'isOriginalTitle': object,
                                'startYear': object,
                                'endYear': object,
                                'runtimeMinutes': object,
                                'birthYear': object,
                                'deathYear': object,
                            }
                            )

    # NOTE: testing if normalizing first does anything
    # Normalize specific attributes
    print("\tNormalizing attributes...")
    dataframe = normalization_method(dataframe)

    # Insert 'null' for missing values. This also replaces the string '\N'
    print("\tInserting 'nan' into empty values...")
    dataframe.fillna(value=str(np.nan), inplace=True)

    # Drop these attributes
    print("\tDropping attributes...")
    dataframe.drop(columns=['region', 'language', 'types', 'attributes', 'titleType', 'endYear'], inplace=True)


    # Create new output file.
    print(f"\tWriting output to '{df_file}'...")
    dataframe.to_csv(path_or_buf=df_file, sep='\t', index=False)

    print("Process complete.")



