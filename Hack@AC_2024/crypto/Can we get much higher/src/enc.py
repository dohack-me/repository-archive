from Crypto.Util.number import getPrime, bytes_to_long, GCD
from gmpy2 import invert, iroot

flag = open('flag.txt', 'rb').read()
m = bytes_to_long(flag)

def main():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p*q
    assert n>m
    
    d = getPrime(256)
    e = invert(d, (p-1)*(q-1))
    
    c = pow(m, e, n)
    
    with open('enc', 'w') as out:
        out.write(f'n = {hex(n)}\n')
        out.write(f'e = {hex(e)}\n')
        out.write(f'c = {hex(c)}')

if __name__=='__main__':
    main()