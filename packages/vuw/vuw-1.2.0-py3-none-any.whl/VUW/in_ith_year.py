import pandas as pd
import numpy as np
from datetime import datetime
from .add_year import add_year


def in_ith_year(df, id_var, from_var, to_var, udate, year, col=None, tp='hos'):
    id_var = str(id_var)
    from_var = str(from_var)
    to_var = str(to_var)


    # 음수일 경우
    if year < 0:
        # 기본 날짜 컬럼이 없으면 생성
        if col is None:
            col = f'{tp}_pst{abs(year)}y'
        df_filtered = df[(pd.to_datetime(df[from_var]).dt.date < datetime.strptime(udate, '%Y-%m-%d').date()) & (pd.to_datetime(df[to_var]) >= pd.to_datetime(add_year(udate, year)))]
        z = df_filtered[[id_var]].drop_duplicates()
        z[col] = 1

    
    else:
        if col is None:
            col = f'{tp}_ftr{abs(year)}y'
        df_filtered = df[(df[from_var] < add_year(udate, year)) & (pd.to_datetime(df[to_var]).dt.date >= datetime.strptime(udate, '%Y-%m-%d').date())]
        z = df_filtered[[id_var]].drop_duplicates()
        z[col] = 1

    return z


if __name__=='__main__':
    data = {
        'id': [1, 2, 3, 4],
        'from_date': ['2018-01-01', '2019-06-14', '2020-03-20', '2021-07-01'],
        'to_date': ['2019-12-31', '2020-12-31', '2021-12-31', '2022-12-31']
    }

    df = pd.DataFrame(data)
    df['from_date'] = pd.to_datetime(df['from_date']).dt.date
    df['to_date'] = pd.to_datetime(df['to_date']).dt.date

    udate = '2020-01-01'
    year = 2

    result = in_ith_year(df, 'id', 'from_date', 'to_date', udate, year, col='sur_pst_1y', tp='sur')
    print(result)