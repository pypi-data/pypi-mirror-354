# # import pandas as pd

# # def split_date_range(df, from_var, to_var, udates, all=True):
# #     """
# #     Split a DataFrame by udates, modifying date ranges and adding rows as needed.
    
# #     :param df: DataFrame to process
# #     :param from_var: Column name for start date
# #     :param to_var: Column name for end date
# #     :param udates: List of dates to split the ranges
# #     :param all: If True, keeps non-overlapping rows as well
# #     :return: Updated DataFrame
# #     """
# #     # Ensure udates is a list of datetime objects
# #     if isinstance(udates, str) or not isinstance(udates, list):
# #         udates = [pd.to_datetime(udates)]
# #     else:
# #         udates = [pd.to_datetime(date) for date in udates]

# #     for udate in udates:
# #         # Rows that do not include the split date
# #         tmp_e = df[~((df[from_var] < str(udate)) & (df[to_var] >= str(udate)))]

# #         # Rows that include the split date
# #         tmp_a = df[((df[from_var] < str(udate)) & (df[to_var] >= str(udate)))]

# #         if not tmp_a.empty:
# #             # Copy tmp_a for the second part of the split
# #             tmp_b = tmp_a.copy()

# #             # Adjust the end date of tmp_a
# #             tmp_a[to_var] = udate - pd.Timedelta(days=1)

# #             # Adjust the start date of tmp_b
# #             tmp_b[from_var] = udate

# #             # # Ensure no invalid ranges are created
# #             tmp_a = tmp_a[tmp_a[from_var] <= tmp_a[to_var]]
# #             tmp_b = tmp_b[tmp_b[from_var] <= tmp_b[to_var]]

# #             # Combine rows based on the 'all' parameter
# #             if all:
# #                 df = pd.concat([tmp_e, tmp_a, tmp_b], ignore_index=True)
# #             else:
# #                 df = pd.concat([tmp_a, tmp_b], ignore_index=True)

# #     # Sort the resulting DataFrame
# #     df = df.sort_values(by=df.columns.tolist()).reset_index(drop=True)

# #     return df


# # if __name__ == '__main__':
# #     data = {
# #         'id': ['A', 'A', 'A', 'B', 'B'],
# #         'gender': [1, 1, 1, 2, 2],
# #         'age': [16, 16, 16, 16, 16],
# #         'age_band': ['10-19', '10-19', '10-19', '10-19', '10-19'],
# #         'kcd': ['x', 'y', 'z', 'w', 'p'],
# #         'sdate': ['2024-01-01', '2024-01-05', '2024-01-10', '2024-01-01', '2024-01-03'],
# #         'edate':  ['2024-01-06', '2024-02-10', '2024-01-15', '2024-01-05', '2024-01-06']
# #     }

# #     df = pd.DataFrame(data)
# #     udate = ['2024-01-06']

# #     df_adjusted = split_date_range(df, 'sdate', 'edate', udate)
# #     print(df_adjusted)


# import pandas as pd
# from joblib import Parallel, delayed

# def split_date_range(df, from_var, to_var, udates, all=True, n_jobs=-1):
#     """
#     Split a DataFrame by udates with parallel processing and vectorized operations.

#     :param df: DataFrame to process
#     :param from_var: Column name for start date
#     :param to_var: Column name for end date
#     :param udates: List of dates to split the ranges
#     :param all: If True, keeps non-overlapping rows as well
#     :param n_jobs: Number of parallel jobs (-1 for all CPUs)
#     :return: Updated DataFrame
#     """
#     # Ensure udates is a list of datetime objects
#     if isinstance(udates, str) or not isinstance(udates, list):
#         udates = [pd.to_datetime(udates)]
#     else:
#         udates = [pd.to_datetime(date) for date in udates]

#     def process_udate(udate):
#         # Rows that do not include the split date
#         tmp_e = df[~((df[from_var] < udate) & (df[to_var] >= udate))]

#         # Rows that include the split date
#         tmp_a = df[((df[from_var] < udate) & (df[to_var] >= udate))]

#         if not tmp_a.empty:
#             # Copy tmp_a for the second part of the split
#             tmp_b = tmp_a.copy()

#             # Adjust the end date of tmp_a
#             tmp_a[to_var] = udate - pd.Timedelta(days=1)

#             # Adjust the start date of tmp_b
#             tmp_b[from_var] = udate

#             # Combine rows based on the 'all' parameter
#             if all:
#                 combined = pd.concat([tmp_e, tmp_a, tmp_b], ignore_index=True)
#             else:
#                 combined = pd.concat([tmp_a, tmp_b], ignore_index=True)
#         else:
#             combined = tmp_e

#         return combined

#     # Process each udate in parallel
#     results = Parallel(n_jobs=n_jobs)(
#         delayed(process_udate)(udate) for udate in udates
#     )

#     # Combine results from all splits
#     final_df = pd.concat(results, ignore_index=True)

#     # Sort the resulting DataFrame
#     final_df = final_df.sort_values(by=final_df.columns.tolist()).reset_index(drop=True)

#     return final_df


import pandas as pd
from joblib import Parallel, delayed


def process_udate(df, from_var, to_var, udate, all_flag):
    tmp_e = df[~((df[from_var] < udate) & (df[to_var] >= udate))]
    tmp_a = df[((df[from_var] < udate) & (df[to_var] >= udate))]

    if not tmp_a.empty:
        tmp_b = tmp_a.copy()
        tmp_a[to_var] = udate - pd.Timedelta(days=1)
        tmp_b[from_var] = udate
        combined = pd.concat([tmp_e, tmp_a, tmp_b], ignore_index=True) if all_flag else pd.concat([tmp_a, tmp_b], ignore_index=True)
    else:
        combined = tmp_e

    return combined


def split_date_range(df, from_var, to_var, udates, all=True, n_jobs=-1):
    if isinstance(udates, str) or not isinstance(udates, list):
        udates = [pd.to_datetime(udates)]
    else:
        udates = [pd.to_datetime(date) for date in udates]

    results = Parallel(n_jobs=n_jobs)(
        delayed(process_udate)(df, from_var, to_var, udate, all) for udate in udates
    )

    final_df = pd.concat(results, ignore_index=True)
    final_df = final_df.sort_values(by=final_df.columns.tolist()).reset_index(drop=True)
    return final_df
