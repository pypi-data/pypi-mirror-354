import pandas as pd
from collections import defaultdict

def map_kcd(codes):
    """
    KCD(병명 코드) 리스트를 받아 3자리와 4자리 코드를 분리하고, 
    정규표현식을 생성하는 함수.
    """
    # 3자리와 4자리 코드 분리
    codes_3digit = [code for code in codes if len(code) == 3]
    codes_4digit = [code for code in codes if len(code) == 4]

    def create_regex(groups):
        """
        주어진 코드 그룹을 정규표현식으로 변환.
        """
        regex_list = []
        for key, group in groups.items():
            if len(group) == 1 | len(group) == 4:
                regex_list.append(f"{group[0]}")
            else:
                start = min(group)
                end = max(group)
                regex_list.append(f"{key}[{start}-{end}]")
                regex_list.append(f"{key}[{start}-{end}][0-9]")
        return "|".join(regex_list)

    # 3자리 코드 그룹화 및 정규표현식 생성
    group_3digit = defaultdict(list)
    for code in codes_3digit:
        prefix = code[:2]  # 첫 두 자리
        suffix = code[2]   # 세 번째 자리
        group_3digit[prefix].append(suffix)

    regex_3digit = create_regex(group_3digit)

    # 4자리 코드 그룹화 및 정규표현식 생성
    group_4digit = defaultdict(list)
    # for code in codes_4digit:
    #     prefix = code[:3]  # 첫 세 자리
    #     suffix = code[3]   # 네 번째 자리
    #     group_4digit[prefix].append(suffix)

    regex_4digit = create_regex(group_4digit)

    # 최종 정규표현식 반환
    return f"{regex_3digit}|{regex_4digit}"
