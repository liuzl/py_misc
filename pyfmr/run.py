import ctypes

fmr = ctypes.CDLL('./fmr.so')
fmr.Hello("Zhanliang")
print(fmr.InitGrammar("./sf.grammar"))
ret = fmr.Extract("北京市", "cities")
