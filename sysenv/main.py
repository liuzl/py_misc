import os
for key in os.environ.keys():
    print(key, os.environ.get(key))
