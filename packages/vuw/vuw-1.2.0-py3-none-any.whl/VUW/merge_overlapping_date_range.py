import pandas as pd
from datetime import timedelta
from joblib import Parallel, delayed
from .glue_code import glue_code_
import numpy as np

def merge_group(group, additional_col, interval=0):
    """
    각 그룹에 대해 날짜 범위를 병합하며, additional_col 값이 다르면 병합하지 않음.
    """
    group = group.sort_values(by=['sdate'] + additional_col)  # 날짜 및 추가 컬럼 기준 정렬
    merged_rows = []
    current_start, current_end = None, None
    current_kcds = []
    unique_treatment_days = set()
    previous_values = {col: None for col in additional_col}

    for _, row in group.iterrows():
        row_start = row['sdate']
        row_end = row['edate']
        if pd.isna(row_start) or pd.isna(row_end):
            continue

        row_days = set(pd.date_range(start=row_start, end=row_end))  # 치료 날짜들
        current_values = {col: row[col] for col in additional_col}  # 현재 행의 additional_col 값들

        if current_start is None:
            # 첫 번째 행 초기화
            current_start = row_start
            current_end = row_end
            current_kcds.append(row['kcd'])
            unique_treatment_days.update(row_days)
            previous_values = current_values
        elif (
            row_start <= current_end + timedelta(days=interval+1) and 
            all(previous_values[col] == current_values[col] for col in additional_col)
        ):
            # 병합 조건: 날짜가 겹치고 additional_col 값이 모두 같을 경우에만 병합
            current_end = max(current_end, row_end)
            current_kcds.append(row['kcd'])
            unique_treatment_days.update(row_days)  # 중복 제거된 치료 날짜 업데이트
        else:
            # 병합된 결과 추가
            merged_row = {
                'ID': row['ID'],
                'gender': row['gender'],
                'age': row['age'],
                'age_band': row['age_band'],
                'kcd': glue_code_(current_kcds),
                'sdate': current_start,
                'edate': current_end,
                'stay': len(unique_treatment_days),  # 고유 치료 날짜 수
            }
            merged_row.update(previous_values)
            merged_rows.append(merged_row)

            # 새로운 기간 시작
            current_start = row_start
            current_end = row_end
            current_kcds = [row['kcd']]
            unique_treatment_days = row_days
            previous_values = current_values  # 새로운 값으로 갱신

    # 마지막 병합된 결과 추가
    if current_start is not None:
        merged_row = {
            'ID': group['ID'].iloc[0],
            'gender': group['gender'].iloc[0],
            'age': group['age'].iloc[0],
            'age_band': group['age_band'].iloc[0],
            'kcd': glue_code_(current_kcds),
            'sdate': current_start,
            'edate': current_end,
            'stay': len(unique_treatment_days),  # 고유 치료 날짜 수
        }
        merged_row.update(previous_values)
        merged_rows.append(merged_row)

    return merged_rows


def merge_overlapping_date_range(df, additional_col=[], interval=0, n_jobs=-1):
    """
    최적화된 중첩 날짜 병합 함수.
    additional_col 값이 같을 경우에만 날짜를 병합.
    치료가 발생한 고유 날짜를 기준으로 stay를 계산합니다.
    """

    tmp = df.copy()
    
    tmp['sdate'] = pd.to_datetime(tmp['sdate'])
    tmp['edate'] = pd.to_datetime(tmp['edate'])

    # 그룹화 및 병렬 처리
    groups = tmp.groupby(['ID'] + additional_col)  # additional_col 값이 다르면 자동으로 병합이 안 되도록 그룹화
    results = Parallel(n_jobs=n_jobs)(
        delayed(merge_group)(group, additional_col, interval) for _, group in groups
    )

    # 결과 병합
    merged_rows = [row for group in results for row in group]
    result = pd.DataFrame(merged_rows)

    return result

