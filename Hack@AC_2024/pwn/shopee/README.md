# Shopee 11.11 Sale

Author: samuzora

> Shopee-pee-pee-pee-pee 9.9 Super Shopping Day
> 
> Buy Everything on Shopee Shopee 9.9 Super Shopping Day
> 
> Don't play play Use your brain (after free)
> 
> 9.9. Super Shopping Day!

**Difficulty: Medium**

## Solution

Refer to `./solve` for full solve script.

Basic UAF vuln with standard operations. First leak libc by using OOB to leak a libc address and add it to cart. Afterwards free the cart to prepare for UAF.

Using set_name, craft a payload such that the target pointer (__free_hook) aligns with an integer on the items array. This will subsequently allow us to replace the previously freed item with our payload, inserting __free_hook into the freed chunk.

Lastly, craft another payload with our desired write and malloc it to trigger the write primitive, and trigger one more free to pop a shell.
