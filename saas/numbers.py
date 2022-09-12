import stdnum.cn.ric
number = '110108196403026127'
b = stdnum.cn.ric.get_birth_date(number)
p = stdnum.cn.ric.get_birth_place(number)
print(b, p)