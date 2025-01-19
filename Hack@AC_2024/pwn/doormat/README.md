# Doormat

Author: samuzora

> Welcome to my humble abode!
>
> Please feel free to enter, but don't break anything plz

**Difficulty: Medium**

## Solution

Refer to `./solve` for full solve script.

Unfortunately this is not a heap challenge.

Idea is to leak libc base via OOB to stderr, which is just slightly above the GOT. Then use the 32 byte write and OOB to write to GOT, overwriting atoi to system and popping a shell.
