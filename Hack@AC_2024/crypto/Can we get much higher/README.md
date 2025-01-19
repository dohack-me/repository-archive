# Can we get much higher

Author: I-En

> My wealth and treasures? If you want it, you can have it! Crack this RSA encryption with massive values and it's yours!

**Difficulty: Medium**

## Solution
$d$ is very small here, so wieners attack can be used to crack the encryption. Solution uses the owiener module to perform the attack and find $d$, then decrypts $c$.

## FAQs
Q: How do I decrypt RSA without knowing $p$ and $q$?  
A: When $d$ is small enough you can simply use Wiener's Attack and not think of $p$ and $q$. But actually you can find $p$ and $q$ efficiently when $d < \frac{1}{3} N^{\frac{1}{4}}$ using [Wiener's theorem](https://en.wikipedia.org/wiki/Wiener%27s_attack)