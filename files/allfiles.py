import glob, os, sys
from datetime import datetime

if getattr(sys, 'frozen', False):
    p = os.path.dirname(os.path.realpath(sys.executable))
else:
    p = os.path.dirname(os.path.abspath(__file__))
p = p + os.sep
print(p)
with open(f"{p}{datetime.now().strftime('%Y%m%d%H%M%S')}.txt", "wb") as out:
    for f in glob.glob(f"{p}**", recursive=True):
        if os.path.isdir(f):
            continue
        if f.startswith(p):
            f = f[len(p):]
        if f == "": continue
        print(f)
        f = (f+"\r\n").encode("utf-8")
        out.write(f)

