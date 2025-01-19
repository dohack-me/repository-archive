from binascii import unhexlify

enc = open('out.txt', 'r').read()
enc = unhexlify(enc)

flag = ''
for i in range(len(enc)):
    if i == 0:
        flag += chr(enc[0])
    else:
        if i%2==0:
            flag += chr(enc[i] - 15)
        else:
            flag += chr(enc[i] + 15)

print(flag)
