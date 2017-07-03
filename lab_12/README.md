# PWN 2

## pwntools

recv, recvn, recvuntil, recvall

u64, u32 (string to number)

p32, p64 (number to byte string)

b64e b64e (base64 encode/decode)

unhex enhex

## ASLR

echo 0 | sudo tee /proc/sys/kernel/randomize_va_space

## gdb

b
stack
c
memsearch
p
x/s <addr>

strings -t x <binarka>