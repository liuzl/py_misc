try:
    a = 0
    b = 1
    b / a
except Exception as e:
    print(e)
    line = "error: %s" % e
    print(line)
