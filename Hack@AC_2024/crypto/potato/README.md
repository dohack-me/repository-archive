# potato

Author: I-En

> i encrypted this with a potato  
> wrap the cracked word with ACSI{}

**Difficulty: Easy**

## Solution
dictionary attack on the hash
`hashcat -m 100 -a 0 enc rockyou.txt --show` or just use a site like https://hashes.com/en/tools/hash_identifier

## FAQs
Q: What does "wrapping" the word mean?  
A: Just put the flag format around the word. For e.g. if the word is "sandwich" then the wrapped flag would be ACSI{sandwich}

Q: Am I supposed/allowed to bruteforce for this challenge?  
A: Bruteforce is allowed

Q: Is the ciphertext a hash?  
A: Can't answer