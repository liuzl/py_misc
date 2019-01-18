import ctypes
fmr = ctypes.CDLL('./fmr.so')
g = ctypes.create_string_buffer("./sf.grammar".encode('utf-8'))
l = ctypes.create_string_buffer("直辖市：北京、上海、天津".encode('utf-8'))
s = ctypes.create_string_buffer("cities".encode('utf-8'))
fmr.init_grammar(g)
ret = fmr.extract(l, s)
print(type(ret))
