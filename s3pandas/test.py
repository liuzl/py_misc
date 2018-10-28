import pandas as pd
import s3fs

df = pd.read_csv("s3://izidata/gray.csv.gz", header=None)

bytes_to_write = df.to_csv(None, header=None, index=None).encode()
fs = s3fs.S3FileSystem()
with fs.open('s3://izidata/tmp/gray.csv', 'wb') as f:
    f.write(bytes_to_write)
