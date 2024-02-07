import time

ts = 1707441895
expire_time = time.localtime(ts)
now = time.localtime()

ret = now > expire_time

print(ret)
print(now < expire_time)