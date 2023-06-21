import datetime


date_time_str = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')

print(date_time_obj)

# подбор нужных функций

dateList = ["2022-10-07", "2022-10-04", "2022-10-31", "2022-10-01"]
print(sorted(dateList, reverse=True))
