import ctypes

fmr = ctypes.CDLL('./fmr.so')
print(fmr.Sum(1,3))
print(fmr.GrammarFromFile("sf.grammar"))
