# pip install python-dateutil

from datetime import *; from dateutil.relativedelta import *

x = datetime.today()+relativedelta(months=+1)
print(x)
