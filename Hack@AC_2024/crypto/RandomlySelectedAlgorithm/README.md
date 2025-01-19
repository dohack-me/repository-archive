# RandomlySelectedAlgorithm

Author: I-En

> An introduction to the RSA algorithm! Go to /index.html if it doesn't work

**Difficulty: Warmup**

## Solution
```py
from Crypto.Util.number import inverse, long_to_bytes

phi = (p-1)*(q-1)
d = inverse(e, phi)
m = pow(c, d, n)
print(long_to_bytes(m))
```

## FAQs
Q: What is the `long_to_bytes` function and how do I use it?  
A: `long_to_bytes` converts a long integer into a bytestring, and in this case converts the integer form of the decrypted plaintext to a readable string form. To use it, you need to install the `Crypto` package of python and import the function using `from Crypto.Util.number import long_to_bytes`.

Q: What is a modular multiplicative inverse?  
A: The modular multiplicative inverse of a number a under modulus p is the value x such that a*x = 1 (mod p). Think of it liek a reciprocal, but under a modulus. https://en.wikipedia.org/wiki/Modular_multiplicative_inverse

Q: How do I compute c^d mod n?  
A: Use the `pow` function in python: https://www.w3schools.com/python/ref_func_pow.asp