import pandas as pd
import numpy as np
from datetime import datetime
from .add_mon import add_mon

def in_ith_mon(df, id_var, from_var, to_var, udate, mon, col=None, tp='hos'):
    id_var = str(id_var)
    from_var = str(from_var)
    to_var = str(to_var)

    
    # 월이 음수일 경우
    if mon < 0:
        # 기본 날짜 컬럼이 없으면 생성
        if col is None:
            col = f'{tp}_pst{abs(mon)}m'
        # print(type(pd.to_datetime(add_mon(udate, mon))))
        df_filtered = df[(pd.to_datetime(df[from_var]).dt.date < datetime.strptime(udate, '%Y-%m-%d').date()) & (pd.to_datetime(df[to_var]) >= pd.to_datetime(add_mon(udate, mon)))]
        z = df_filtered[[id_var]].drop_duplicates()
        # z[from_var] = df_filtered[from_var] 
        # z[to_var] = df_filtered[to_var] 
        z[col] = 1

    
    else:
        if col is None:
            col = f'{tp}_ftr{abs(mon)}m'
        df_filtered = df[(df[from_var] < pd.to_datetime(add_mon(udate, mon))) & (pd.to_datetime(df[to_var]).dt.date >= datetime.strptime(udate, '%Y-%m-%d').date())]
        z = df_filtered[[id_var]].drop_duplicates()
        z[col] = 1

    return z


if __name__=='__main__':
    data = {
        'id': [1, 2, 3],
        'from_date': ['2024-01-06', '2024-07-14', '2023-03-01'],
        'to_date': ['2024-12-31', '2024-09-18', '2023-06-30']
    }

    df = pd.DataFrame(data)
    df['from_date'] = pd.to_datetime(df['from_date']).dt.date
    df['to_date'] = pd.to_datetime(df['to_date']).dt.date

    udate = '2024-05-01'
    mon = 2

    result = in_ith_mon(df, 'id', 'from_date', 'to_date', udate, mon, col='sur_ftr_2m', tp='sur')
    print(result)