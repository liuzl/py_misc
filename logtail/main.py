import multitail2
mt = multitail2.MultiTail("./log/*.txt")
for line in mt:
    print(line)
