from datetime import datetime
from dateutil.relativedelta import relativedelta

def add_mon(date, mon):
    date = datetime.strptime(str(date), '%Y-%m-%d')
    new_date = date + relativedelta(months=mon)

    return str(new_date.date())

if __name__ == '__main__':
    date = '2024-12-15'
    mon = 2
    new_date = add_mon(date, mon)
    print(new_date)