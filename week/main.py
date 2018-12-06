import datetime
import sys
import time

d = datetime.date(2018,11,30)
print(d.isocalendar()[1])

for line in sys.stdin:
    t = datetime.datetime.strptime(line.strip(), "%Y%m%d")
    print(t.isocalendar()[1])
