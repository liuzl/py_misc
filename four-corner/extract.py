import pickle
data =  pickle.load(open("data.pkl", 'rb'))
out = open("four.csv", "wb")
out.write(b"code,text\n")
for k, v in data.items():
    line = "%s,%s\n" % (k, v)
    out.write(line.encode('utf-8', 'ignore'))
out.close()
