import pycorrector
s = '少先队员因该为老人让坐'
ret, detail = pycorrector.correct(s)
print(ret, detail)
