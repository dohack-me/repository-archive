# Think backwards

Author: I-En

> Welcome to Reverse Engineering (RE)! As a warmup, prove to me you can think backwards!

**Difficulty: Warmup**

## Solution
Simple python reversing.  
Analyse the function and write a script to reverse.
Unhexlify the ciphertext. Loop through the ciphertext and deduct 15 for each character in an even position and add 15 for each character in an odd position.

## FAQs
Q: What does `ord` do?  
A: Returns the number representing the unicode code of a specified character: https://www.w3schools.com/python/ref_func_ord.asp

Q: What does `[2:]` do?  
A: Removes the "0x" prefix from the hex value