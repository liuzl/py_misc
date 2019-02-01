import ctypes
fmr = ctypes.CDLL('./fmr.so')
charptr = ctypes.POINTER(ctypes.c_char)

fmr.extractx.restype = charptr

def c(s): return ctypes.create_string_buffer(s.encode('utf-8'))

g = c("./sf.grammar")
s = c("cities")

i = fmr.init_grammar(g)

strs = [
    "直辖市：北京、上海、天津",
    "直辖市：帝都、津城、魔都",
    "中国现在有四个直辖市：帝都、魔都、天津、重庆。",
    "中国曾经的直辖市：帝都、魔都、天津、重庆、旧都。",
    "天津大学",
]

for l in strs:
    ret = fmr.extractx(i, c(l), s)
    value = ctypes.cast(ret, ctypes.c_char_p).value
    fmr.gofree(ret)
    print(value.decode('utf-8'))
