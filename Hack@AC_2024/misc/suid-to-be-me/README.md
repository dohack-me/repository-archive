# SUID to be me

## Description

Very simple SUID privilege escalation with PATH override:

## Intended exploit path

- Generate a reverse shell which connects back to an ngrok proxy ([Revshells](https://www.revshells.com/) has some cool payloads)
- `ls` is disabled, so we have to use `echo *` to check contents of current directory, and we see a `checkflag` binary
- We cannot use `ls` to check the permissions of this file. `echo /bin/*` and `echo /usr/bin/*` give you a list of files you can check.
- To check permissions without `ls`, we can try alternative methods. `tar cf - <filename> | tar tvf -` works.
- `tar cf - checkflag | tar tvf -` tells us that the file is owned by root, and has `-rwsrwxrwx` perms. This is an SUID binary that runs as root.
- Modifying the file removes the SUID bit. We have to figure out exactly what `checkflag` does. Checking permissions of all the files in /bin and /usr/bin tells us that base64 is available for use. We can use this to extract and reverse the binary.
- reversing the binary tells us that the program executes `sha256sum`, but does not specify an absolute path. This relies on the PATH variable, which we can hijack.
- We can make a file in `/tmp` called `sha256sum`, containing `cat /root/flag.txt`. `chmod 777 /tmp/sha256sum` makes the file executable to all users.
- `export $PATH=/tmp:$PATH` makes it so that /tmp is the first directory in the path, and thus the directory in which files are looked for in first. 
- We can then run our checkflag binary, giving us the flag!

