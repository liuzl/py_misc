import datetime
import sys
import time

for line in sys.stdin:
    t = datetime.datetime.strptime(line.strip(), "%Y%m%d")
    print(t.isocalendar()[1])
