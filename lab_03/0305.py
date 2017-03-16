from hashlib import md5
import random
import string
import re

salt = '2234479'
reg = re.compile(r"^0e\d*$")

def hash(pwd):
    m = md5()
    m.update(bytes(salt + pwd, 'ascii'))
    return m.hexdigest()

i = 0

while True:
    i += 1
    s = str(i)
    if i % 1000000 == 0:
        print(i)

    # print(s)

    h = hash(s)

    if (reg.match(h)):
        print('OK')
        print(s)
        break
