import hyperscan

db = hyperscan.Database()
patterns = (
    # expression,  id, flags
    (br'fo+',      0,  0),
    (br'^foobar$', 1,  hyperscan.HS_FLAG_CASELESS),
    (br'BAR',      2,  hyperscan.HS_FLAG_CASELESS
                       | hyperscan.HS_FLAG_SOM_LEFTMOST),
)
expressions, ids, flags = zip(*patterns)
db.compile(
    expressions=expressions, ids=ids, elements=len(patterns), flags=flags
)
print(db.info().decode())
# Version: 5.1.1 Features: AVX2 Mode: BLOCK
