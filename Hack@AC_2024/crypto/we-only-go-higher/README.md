# We Only Go Higher

## Intended Solution

This is a hash function that is strictly increasing. This can be observed by reading the source carefully, or by just experimenting.

Hence we can easily binary search through the range of possible keys to encrypt, and eventually get to something that encrypts to the encrypted flag (i.e. the plaintext flag).
