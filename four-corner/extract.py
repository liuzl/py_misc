import pickle
data =  pickle.load(open("data.pkl", 'rb'))
out = open("data.txt", "wb")
for k, v in data.items():
    line = "%s\t%s\n" % (k, v)
    out.write(line.encode('utf-8', 'ignore'))
out.close()
