'''import marshal

redata = marshal.loads(var)
'''

import pickle

filename = 'data'
infile = open(filename,'rb')
new_dict = pickle.load(infile)
infile.close()

print(new_dict)
print(type(new_dict))

'''
import time
starttime=time.time()
while True:
  print("tick")
  time.sleep(3.0 - ((time.time() - starttime) % 3.0))
'''
