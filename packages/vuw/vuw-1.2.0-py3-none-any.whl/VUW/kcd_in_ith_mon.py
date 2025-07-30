import pandas as pd
import numpy as np
from .add_mon import add_mon
from .subset_id_with_kcd_ import subset_id_with_kcd_
from datetime import datetime
import re


def kcd_in_ith_mon(df, id_var, kcd_var, from_var, to_var, kcd_code, udate, mon, col=None):
    """
    특정 날짜에 맞는 데이터를 필터링하고, 해당하는 id만 반환하는 함수.
    :param df: 데이터프레임
    :param id_var: ID 변수 이름
    :param kcd_var: KCD 코드 변수 이름
    :param from_var: 시작 날짜 변수 이름
    :param to_var: 종료 날짜 변수 이름
    :param kcd_code: 필터링할 KCD 코드
    :param udate: 기준 날짜
    :param mon: 주어진 월 수
    :param col: 결과로 추출할 컬럼 (기본값 None)
    :return: 필터링된 데이터프레임
    """
 
    # KCD 코드로 필터링
    # dm = subset_id_with_kcd_(df, id_var, kcd_var, kcd_code)
    dm = df[df[kcd_var].str.contains(kcd_code, regex=True, na=False)]
    # print(dm)
    # dm = dm[dm[kcd_var].str.contains(kcd_code, regex=True, na=False)]
    
    # 컬럼 이름 생성
    if col is None:
        if mon < 0:
            col = f"{kcd_code}_pst_{abs(mon)}"
        else:
            col = f"{kcd_code}_ftr_{abs(mon)}"

    # 날짜 조건에 맞는 데이터 필터링
    if mon < 0:
        df_filtered = dm[(pd.to_datetime(dm[from_var]).dt.date < datetime.strptime(udate, '%Y-%m-%d').date()) & (pd.to_datetime(dm[to_var]) >= pd.to_datetime(add_mon(udate, mon)))]
    else:
        df_filtered = dm[(pd.to_datetime(dm[from_var]) < pd.to_datetime(add_mon(udate, mon))) & (pd.to_datetime(dm[to_var]).dt.date >= datetime.strptime(udate, '%Y-%m-%d').date())]
    
    # 결과에서 고유한 id만 추출
    result = df_filtered[[id_var]].drop_duplicates()
    
    # 새로운 컬럼 추가
    result[from_var] = df_filtered[from_var]
    result[to_var] = df_filtered[from_var]
    result[kcd_var] = df_filtered[kcd_var]
    result[col] = 1

    return result

if __name__ == '__main__':
    # 예시 데이터프레임 생성
    data = {
        'id': [1, 2, 3, 4],
        'kcd_code': ['A01', 'A02', 'A01', 'A03'],
        'from': ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01'],
        'to': ['2023-06-01', '2023-05-01', '2023-07-01', '2023-08-01']
    }

    df = pd.DataFrame(data)
    udate = '2023-03-01'
    # 함수 호출
    result = kcd_in_ith_mon(df, id_var='id', kcd_var='kcd_code', from_var='from', 
                            to_var='to', kcd_code='A01', udate=udate, 
                            mon=-1)

    print(result)
