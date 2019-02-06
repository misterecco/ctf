def myfact(n):
    i = 1
    acc = 1
    while i <= n:
        acc *= i
        i += 1
    return acc


#import dis
#dis.dis(myfact)

print myfact(10)
