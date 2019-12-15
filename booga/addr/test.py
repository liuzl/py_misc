import pydict
d = pydict.Dict("addrdb")
ret = d.multi_max_match("河北省邢台市柏乡县")
print(ret)
