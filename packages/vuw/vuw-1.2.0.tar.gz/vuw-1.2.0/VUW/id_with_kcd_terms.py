import pandas as pd
from .add_year import add_year


def id_with_kcd_terms(df, id_var, kcd_var, from_var, to_var, udate, terms):
    """
    특정 조건(pst, ftr 등)에 따라 데이터를 필터링합니다.
    :param df: pandas DataFrame
    :param id_var: ID 컬럼 이름 리스트 (예: ['id', 'gender', 'age_band'])
    :param kcd_var: KCD 코드 컬럼 이름
    :param from_var: 시작 날짜 컬럼 이름
    :param to_var: 종료 날짜 컬럼 이름
    :param udate: 기준 날짜
    :param terms: 필터링 조건 (예: pst, ftr)
    :return: 필터링된 pandas DataFrame
    """
    import pandas as pd
    
    id_var = id_var[0] if isinstance(id_var, list) else id_var
    start, end, pattern = terms
    
    # 기간 설정
    start_date = add_year(udate, start)
    end_date = add_year(udate, end)

    df[kcd_var] = df[kcd_var].astype(str).str.strip()

    # 필터 조건
    filtered = df[
        (df[kcd_var].str.contains(pattern, regex=True, na=False)) &
        (df[from_var] <= str(end_date)) &
        (df[to_var] >= str(start_date))
    ]

    
    # 결과에 term_name 컬럼 추가
    filtered_df = filtered.drop_duplicates(subset=[id_var])

    # df['raw'] = df[id_var].isin(filtered_df).astype(int)

    return filtered_df
    # # Summarize results
    # nsum = result['raw'].sum()
    # ratio = nsum / result.shape[0]
    # summary = pd.DataFrame([{
    #     'term': 'raw',
    #     'nsum': nsum,
    #     'ratio': ratio,
    #     'label': f'{ratio*100:.2f}%'
    # }])
    # result.attrs['summary'] = summary

    
    return result    
    #     filtered[term_name] = 1
    #     results.append(filtered)
    
    # # 모든 id를 기준으로 초기 결과 생성
    # all_ids = df[id_var].drop_duplicates()
    # result = all_ids.copy()
    
    # # 조건별로 병합
    # for partial_result in results:
    #     result = pd.merge(result, partial_result, on=id_var, how='left')
    
    # # 결측값을 0으로 채움
    # # result.fillna(0, inplace=True)
    # print(result.columns)
    
    # # 모든 결과를 정수형으로 변환
    # # result.update(result.select_dtypes(include=['float']).astype(int))
    
    # return result


