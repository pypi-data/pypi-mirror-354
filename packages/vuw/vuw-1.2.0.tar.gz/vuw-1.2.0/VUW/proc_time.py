import time

def proc_time(expr):
    stime = time.time() # 시작 시간 기록
    eval(expr)  # 표현식 실행
    etime = time.time()
    elapsed = etime - stime
    return time.strftime('%H:%M:%S', time.gmtime(elapsed))


if __name__ == '__main__':
    expr = 'sum(range(1000000))'
    print(proc_time(expr))