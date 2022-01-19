# pip install python-dateutil

from datetime import *
from dateutil.relativedelta import *

today = datetime.today()

this_month = datetime(today.year, today.month, 1)
print(this_month)
last_month = this_month + relativedelta(months=-1)
print(last_month)
