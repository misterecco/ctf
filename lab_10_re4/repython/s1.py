import marshal
import sys
import dis

f = open('crackme/this_function_contains_the_flag_1.pyc', 'rb')
f.read(8)
code_object = marshal.load(f)
code = dis.dis(code_object)
print(code)

foo = code_object.co_consts[0]

print(dis.dis(foo.co_code[7:]))
