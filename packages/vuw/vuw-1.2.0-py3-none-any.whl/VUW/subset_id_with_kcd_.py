import pandas as pd
import re
import numpy as np


def pull_code(code, x):
    '''
    주어진 코드 패턴을 x에서 찾아서 반환하는 함수
    :param code: 찾고자 하는 패턴 (정규 표현식)
    :param x: 대상 문자열
    '''

    result = [re.search(code, item).group(0) if re.search(code, item) else np.nan for item in x]
    return result

def rmv_code(code, x):
    return re.sub(code, '', x)


def subset_id_with_kcd_(df, id_var, kcd_var, kcd_code_list):

    z = df.copy()
    print(kcd_code_list)
    if kcd_code_list:
        # grepl로 조건 필터링
        filtered_rows = z[z[kcd_var].isin(kcd_code_list)]

        return filtered_rows

    return z


    