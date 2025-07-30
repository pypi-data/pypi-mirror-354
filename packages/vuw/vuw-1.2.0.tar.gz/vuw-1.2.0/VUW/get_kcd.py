import pandas as pd
import re

# 예시 데이터프레임 (kcd_book)
# 실제 데이터는 kcd_book과 같은 구조로 불러와야 합니다.



def get_kcd(x, file_dir, lang='ko', type='kcd'):
    if not x:
        raise ValueError("Please insert kcd code string or regular expressions.")
    kcd_book = pd.read_excel(file_dir, engine='openpyxl')
    # 대소문자 구분 없이 x와 일치하는 kcd 코드 찾기
    matched_rows = kcd_book[kcd_book['kcd'].str.contains(x, flags=re.IGNORECASE, regex=True) |
                            kcd_book['kcd'].str.replace(r"\.", "", regex=True).str.contains(x, flags=re.IGNORECASE, regex=True)]
    
    if matched_rows.empty:
        return "No matching codes found."
    
    # 언어에 따라 결과 포맷 결정
    if lang == 'ko':
        df = matched_rows[['kcd', 'ko']]
    else:
        df = matched_rows[['kcd', 'en']]
    
    # kcd와 ko 또는 en 컬럼의 최대 길이 계산
    nc = df['kcd'].str.len().max()
    rc = df.iloc[:, 1].str.len().max()  # 'ko' 또는 'en' 컬럼
    
    # 결과 출력 폭 계산
    iter_length = nc + len(" | ") + rc
    line = '-' * min(iter_length, 80)  # 최대 80자로 줄임
    
    # 출력 형식 생성
    result = "\n".join([f"{row['kcd'].ljust(nc)} | {row[lang]}" for _, row in df.iterrows()])
    
    return f"{line}\n{result}\n{line}"


if __name__ == '__main__':
    # 사용 예시
    x = "A09"  # 찾을 KCD 코드 문자열
    lang = "ko"  # 'ko' 또는 'en' 선택
    print(kcd_book)
    print(get_kcd(x, lang))
