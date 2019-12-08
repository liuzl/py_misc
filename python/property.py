class A(object):
    def __init__(self):
        self.ok = True

    @property
    def size(self):
        return self.ok

if __name__ == "__main__":
    a = A()
    print(a.size)
