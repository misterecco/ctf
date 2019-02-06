import marshal
import dis
import sys


pyc_file = open(sys.argv[1], 'rb')
magic = pyc_file.read(4)
date = pyc_file.read(4)
code_object = marshal.load(pyc_file)
pyc_file.close()
code = dis.dis(code_object)
print(code)
