import random

def genPerm(seed, size):
   random.seed(seed)
   perm = range(size)
   random.shuffle(perm)
   return perm     

perm1 = genPerm("ala ma kota", 2**12)
perm2 = genPerm("ula ma psa", 2**12)

BLOCK_BITS = 24

def round(data, key):
   k1 = (key >> (BLOCK_BITS/2)) % (2 ** (BLOCK_BITS / 2))
   k2 = key % (2 ** (BLOCK_BITS / 2))
   return perm2[ perm1[data ^ k1] ^ k2]

def encrypt(plaintext, key, rounds):
    l = plaintext % (2 ** (BLOCK_BITS / 2))
    r = (plaintext >> (BLOCK_BITS / 2)) % (2 ** (BLOCK_BITS / 2))

    #print hex(plaintext), hex(key)
    #print 'r0', hex(l),hex(r)
    for i in xrange(rounds):
       l, r = r, l ^ round(r, key)
       #print 'r',i+1, hex(l),hex(r)

    return (r << (BLOCK_BITS / 2)) | l