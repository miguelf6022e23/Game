import shelve
sf = shelve.open('lavT')
for i in sf.keys():
    print(i)
sf.close()
