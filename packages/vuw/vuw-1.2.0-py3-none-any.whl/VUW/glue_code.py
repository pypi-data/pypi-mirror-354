def glue_code_(x, collapse='|'):
    #NAl 값이 None으로 표현된 경우를 처리하고 고유값만 추출
    unique_values = set(filter(lambda v: v is not None, x))

    # 고유값을 collapse 구분자로 결합하여 변환
    return collapse.join(map(str, unique_values))

    

def glue_code(x, new_code):

    temp = x

    temp.append(new_code)
    return temp
