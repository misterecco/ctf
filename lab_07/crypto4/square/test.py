from client import encrypt_request, encrypt, get_encrypted_flag
import itertools

# candidates = [[0,1,2],[0,3],...]
# for key in itertools.product(*candidates)

plaintexts = [ chr(i) + '\x00' * 15 for i in xrange(0,256) ]

ciphertexts = [encrypt(t) for t in plaintexts]

def xor(key, text):
    [chr(ord(k) ^ ord(t)) for (k, t) in zip(key, text)]

def guess_bute(k):
    results = []

    plaintexts = [ '\x00' * (k) + chr(i) + '\x00' * (15-k) for in xrange(2,256)]
    ciphertexts = [encrypt(t) for t in plaintexts]

    keys = [chr(i) * 16 for i in xrange(0,256)]

    for k in keys:
        cands
