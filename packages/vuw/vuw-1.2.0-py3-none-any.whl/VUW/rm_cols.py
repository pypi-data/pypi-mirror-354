import pandas as pd

def rm_cols(df, cols):
    if isinstance(cols, str):
        cols = [cols]

    df = df.drop(columns=cols)
    return df
