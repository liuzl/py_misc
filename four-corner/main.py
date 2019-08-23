import pickle
import sys

data =  pickle.load(open("data.pkl", 'rb'))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: %s <汉字>")
        sys.exit(1)
    print(data.get(sys.argv[1], None))
