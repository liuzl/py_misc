import pycorrector
import sys
s = '少先队员因该为老人让坐'
for s in sys.stdin:
    ret, detail = pycorrector.correct(s)
    print(ret, detail)
