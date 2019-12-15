import gzip
import json
import pydict
from tqdm import tqdm

codelen = {2:"province", 4:"city", 6:"county", 9:"town", 12:"village"}

def process(infile):
    if infile.endswith(".gz"): fp = gzip.open(infile, 'rt')
    else: fp = open(infile, 'rt')
    db = pydict.Dict("addrdb")

    lines = fp.read().strip().split("\n")
    pbar = tqdm(total=len(lines))
    for line in lines:
        pbar.update(1)
        item = line.strip().split('\t')
        if len(item) != 2:
            print("err line: %s" % line.strip())
            continue
        for key in item[1].split(','):
            key = key.strip()
            if len(key) <= 1: continue
            db.insert(key, {codelen[len(item[0])]: item[0]})
    db.save()
    pbar.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python %s <in_file>" % sys.argv[0])
        sys.exit(1)
    process(sys.argv[1])
