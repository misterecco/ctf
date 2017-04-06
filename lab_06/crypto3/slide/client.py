import requests

addr = "http://p4.team:8353/"

def _encrypt_request(req, data):
    r = req.get(addr+data)
    ciphertext = r.text.split()[3].decode('hex')

    assert len(ciphertext) == 3
    return ciphertext

def encrypt_request(data):
    return _encrypt_request(requests, data)

def encrypt_session(datas):
    req = requests.session()
    return [_encrypt_request(req, data) for data in datas]

def encrypt(s):
    assert len(s) == 3
    return encrypt_request(s.encode('hex'))

def encrypt_many(s):
    for x in s:
        assert len(x) == 3
    return encrypt_session([x.encode('hex') for x in s])
