import glob
from datetime import datetime
with open(f"{datetime.now().strftime('%Y%m%d%H%M%S')}.txt", "w") as out:
    for f in glob.glob("**", recursive=True):
        out.write(f"{f}\n")

