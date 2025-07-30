import numpy as np
import pandas as pd
import re

def cut_age(x, interval, right=False):
    # x의 최소값과 최대값을 interval 기준으로 내림과 올림하여 범위 설정
    mn = np.floor(np.min(x) / interval) * interval
    mx = np.ceil(np.max(x) / interval) * interval

    # mx가 x의 최대값과 같을 경우 mx 조정
    if np.max(x) == mx:
        mx = np.ceil(np.max(x) / interval + 1) * interval

    # pd.cut 이용해서 x를 구간별로 나누기
    bins = np.arange(mn, mx + interval, interval)
    categories = pd.cut(x, bins, right=right)
    

    labels = [f'{int(bins[i])}-{int(bins[i+1]-1)}' for i in range(len(bins) - 1)]
    age_groups = pd.cut(x,
                        bins=bins,
                        labels=labels,
                        right=right,
                        include_lowest=True)
    
    return age_groups


if __name__ == '__main__':
    x = np.random.randint(0, 100, size=20)
    interval = 10
    result = cut_age(x, interval)
    print(result)