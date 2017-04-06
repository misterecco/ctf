from client import encrypt

def ask_server(msg):
    print("Ask: {}".format(msg))
    print(encrypt(msg))


# cnst = "\x42\x42"

def left(sb):
    return ord(sb[0]) * 256 + ord(sb[1]) // 16


def right(sa):
    return ord(sa[2]) + (ord(sa[1]) % 16) * 16


def compare_halves(sa, sb):
    ia = right(sa)
    ib = left(sa)
    return ia == ib


def generate_B_pairs():
    res = []
    for i in xrange(0,256):
        for j in xrange(0,16):
            res.append(''.join((chr(i), chr(j + 1), chr(1))))
    return res


def generate_A_pairs():
    res = []
    for i in xrange(0,256):
        for j in xrange(0,16):
            res.append(''.join((chr(1), chr(16 + j), chr(i))))
    return res


pairs_A = generate_A_pairs()
pairs_B = generate_B_pairs()


left_pool = {}
right_pool = {}

for p_a in pairs_A:
    c_a = encrypt(p_a)
    right_pool[right(c_a)] = (p_a, c_a)

for p_b in pairs_B:
    c_b = encrypt(p_b)
    left_pool[left(c_b)] = (p_b, c_b)

    if left(c_b) in left_pool:
        print(right_pool(left(c_b)))
        print(p_b, c_b)
