
import numpy as np
import pandas as pd


from dataframe_helpers.generic import to_array



def chunk_maker(df, group_by_cols, chunk_condition, sort_by_values = None):
    """
    Groups a DataFrame by the specified columns and then further chunks each group
    using a custom condition. Returns a Series of chunk IDs.

    Parameters:
    df (pd.DataFrame): The input dataframe.
    group_by_cols (list): List of column names to group by.
    chunk_condition (function): A function that takes two rows and returns True if they belong to the same chunk.

    Returns:
    pd.Series: A series containing chunk IDs corresponding to the original dataframe index.
    """
    group_by_cols = to_array(group_by_cols)
    if sort_by_values:
        sort_by_values = to_array(sort_by_values)
        df = df.copy()  # Avoid modifying the original dataframe
        df.sort_values(sort_by_values, inplace=True)  # Sort to ensure order within groups
    chunk_id_series = pd.Series(index=df.index, dtype=int)  # Initialize chunk ID Series

    chunk_counter = 0
    grouped = df.groupby(group_by_cols)  # Group by specified columns
    
    for _, group in grouped:
        group = group.reset_index()  # Reset index for easier row access
        chunk_labels = np.full(len(group), -1)  # Initialize chunk labels for the group
        
        for i in range(len(group)):
            if chunk_labels[i] == -1:  # If not yet assigned to a chunk
                chunk_labels[i] = chunk_counter
                for j in range(i + 1, len(group)):
                    if chunk_labels[j] == -1 and chunk_condition(group.iloc[i], group.iloc[j]):
                        chunk_labels[j] = chunk_counter
                chunk_counter += 1

        chunk_id_series[group["index"]] = chunk_labels  # Assign chunk labels back to original index
    
    return chunk_id_series
