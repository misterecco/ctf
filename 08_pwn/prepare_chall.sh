#!/bin/bash

# dodajemy nowego użytkownika
adduser --disabled-password --gecos pwn pwn
# zmieniamy właściciela programu
chown pwn chall
# set-user-ID odsyłam do:
# man chmod
# https://unix.stackexchange.com/questions/79395/how-does-the-sticky-bit-work
# https://en.wikipedia.org/wiki/Setuid
chmod u+s chall

# należy odpalić "/bin/sh" z prawami nowego użytkownika (pwn)
# przez eksploitację danego programu
