import types

def foo(a, b):
    return ''.join([chr(ord(ac) ^ ord(bc)) for (ac, bc) in zip(a, b)])


def bar(a, b):
    return ''.join([chr((ord(ac) + ord(bc)) % 256) for (ac, bc) in zip(a, b)])


def minus(a, b):
    if a - b < 0:
        return a - b + 256
    return a - b


def baz(a):
    K = 'secret' * 100
    return bar(foo(bar(a, K), K), K)


def main():
    data = raw_input('Password> ')
    if baz(data) == '5b361806081005100e3008201a1b121750'.decode('hex'):
        print foo(data, ']8ADPC\x15\x05\x04)\x15;\x15\x0f\x1a\x0eT')
    else:
        print 'Sorry, bad password'


main()