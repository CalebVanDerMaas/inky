import calendar
import datetime
import os

cal = calendar.Calendar()
now = datetime.datetime.now()
dates = cal.monthdatescalendar(now.year, now.month)

print('cal: ' + str(cal))
print('now: ' + str(now))
print('dates: ' + str(dates))