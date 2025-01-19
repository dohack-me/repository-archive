from pwn import *

r = remote("localhost", "3002")

junk = r.recvuntil(b"Encrypted Secret:  ")
secret = r.recvline()[:-1]
secret = int(secret.decode("utf-8"))

low = int(1e50)
high = int(1e80)

turn = 1

while True:
    mid = (low + high) // 2
    r.sendline(str(int(mid)).encode('utf-8'))
    
    l2 = r.recvuntil(b'Here you go:\n')
    l2 = int(r.recvline()[:-1].decode("utf-8"))
    print(turn, low % 10000, high % 10000)
    
    turn += 1
    
    if l2 == secret:
        print(f'\n\nSOLVED: {mid}')
        break
    
    if l2 > secret:
        high = mid-1
    else:
        low = mid+1