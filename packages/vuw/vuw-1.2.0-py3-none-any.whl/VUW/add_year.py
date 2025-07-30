from datetime import datetime
from dateutil.relativedelta import relativedelta

def add_year(date, year):
    date = datetime.strptime(str(date), '%Y-%m-%d')
    new_date = date + relativedelta(years=year)

    return str(new_date.date())

if __name__ == '__main__':
    date = '2024-12-15'
    year = 1
    new_date = add_year(date, year)
    print(new_date)