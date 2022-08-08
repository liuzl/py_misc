import glob, os
from datetime import datetime
p = os.path.dirname(os.path.realpath(__file__))
with open(f"{datetime.now().strftime('%Y%m%d%H%M%S')}.txt", "w") as out:
    for f in glob.glob(f"{p}{os.sep}**", recursive=True):
        out.write(f"{f}\n")

