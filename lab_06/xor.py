def sxor(s1,s2):
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))


s1 = sxor('guest', 'admin')

k = "\x23\x75\x78\xe1\xc7"

o = sxor(k, s1)

for c in o:
    print(hex(ord(c)))
