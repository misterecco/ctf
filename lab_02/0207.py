from sys import argv

def print_ascii(word):
    print(list(map(ord, word)))

print_ascii(argv[1])
