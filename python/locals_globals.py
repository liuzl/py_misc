def func(arg):
    a = 1
    b = 2
    print(locals())
    print(globals())

if __name__ == "__main__":
    func(3)
