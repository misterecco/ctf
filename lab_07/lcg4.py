# n = ?
# m = ?
# c = ?

# s2 = (s1 * m + c) % n
# s3 = (s2 * m + c) % n
# (s3 - s2) % n = ((s2 - s1) * m) % n
# s(k) - s(k-1) == (s(k-1) - s(k-2)) * m [mod n]

import sys
sys.setrecursionlimit(1000000)  # long type,32bit OS 4B,64bit OS 8B(1bit for sign)

# return (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


m = (mulinv(s2 - s1, n) * (s3 - s2)) % n
c = (s2 - s1 * m) % n

s4 = (s3 * m + c) % n

print(s4)
