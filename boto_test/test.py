import boto
bucket = boto.connect_s3().get_bucket('izidata')
for k in bucket.list("online_svc_log/s3/log2018/10/22/", "/"):
    print(k.name)

