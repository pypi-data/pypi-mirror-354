import re
import numpy as np
import pandas as pd
from .add_mon import add_mon
from datetime import datetime

# def pull_code(code, x):
#     '''
#     주어진 코드 패턴을 x에서 찾아서 반환하는 함수
#     :param code: 찾고자 하는 패턴 (정규 표현식)
#     :param x: 대상 문자열
#     '''

#     result = [re.search(code, item).group(0) if re.search(code, item) else np.nan for item in x]
#     return result

# def rmv_code(code, x):
#     return re.sub(code, '', x)

def subset_id_with_kcd_terms(df, id_var, kcd_var, from_var, to_var, udate, kcd_term):
    """
    Filter data based on date range and KCD term.

    :param df: pandas DataFrame
    :param id_var: Column name representing unique identifiers (e.g., 'id')
    :param kcd_var: Column name containing KCD codes
    :param from_var: Column name containing start dates
    :param to_var: Column name containing end dates
    :param udate: Reference date for filtering
    :param kcd_term: List with [start_years, end_years, pattern] for filtering
    :return: Filtered DataFrame containing all rows for the matching IDs
    """
    # Copy DataFrame to avoid modifying the original
    df_copy = df.copy()

    # Parse kcd_term
    start, end, pattern = kcd_term

    # Calculate filtering date range
    fdate = pd.to_datetime(add_mon(udate, start * 12))
    tdate = pd.to_datetime(add_mon(udate, end * 12))

    # Filter rows based on the date range
    date_condition = (df_copy[from_var] >= fdate) & (df_copy[to_var] <= tdate)

    # Filter rows based on the KCD pattern (if pattern is not empty)
    if pattern:
        kcd_condition = df_copy[kcd_var].str.contains(pattern, regex=True, na=False)
    else:
        kcd_condition = True  # No pattern provided, include all

    # Combine conditions
    combined_condition = date_condition & kcd_condition

    # Get matching IDs based on combined conditions
    matching_ids = df_copy.loc[combined_condition, id_var].unique()

    # Return all rows for the matching IDs
    result_df = df_copy[df_copy[id_var].isin(matching_ids)]

    return result_df

