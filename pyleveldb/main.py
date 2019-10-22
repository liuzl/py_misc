import leveldb
db = leveldb.LevelDB('./db')
#db.Put(b"key1", b"value1")
v = db.Get(b"key1")
print(v)
