import pandas as pd

def metrics(df):
    '''
    Gets the number of rows, columns, and number of rows with nulls for each column.  Also returns description for common values from table.
    '''
    rows = df.shape[0]
    cols = df.shape[1]
    nulls = df.isna().sum()
    print(f'There are {rows} rows and {cols} columns in this dataframe.')
    print(f'Plus the following nulls:\n{nulls}')
    return df.describe().T


def get_numbers(df):
    for column in df.columns:
        print(column)
        print(df[column].value_counts())
        print("-----------------")
        

def percentage_dropper(df):
    df = df.loc[:, df.isnull().mean() < .02]
    return df

def get_nan_cols(df, nan_percent=0.8):
    threshold = len(df.index) * nan_percent
    return [c for c in df.columns if sum(df[c].isnull()) >= threshold]


