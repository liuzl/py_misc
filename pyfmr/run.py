import ctypes
fmr = ctypes.CDLL('./fmr.so')
charptr = ctypes.POINTER(ctypes.c_char)

fmr.extract.restype = charptr

def c(s): return ctypes.create_string_buffer(s.encode('utf-8'))

g = c("./sf.grammar")
s = c("cities")

fmr.init_grammar(g)

strs = ["直辖市：北京、上海、天津","直辖市：帝都、津城、魔都"]

for l in strs:
    ret = fmr.extract(c(l), s)
    value = ctypes.cast(ret, ctypes.c_char_p).value
    print(value.decode('utf-8'))
