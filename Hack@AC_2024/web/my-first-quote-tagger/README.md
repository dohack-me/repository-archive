# My First Quote Tagger

Author: kek

> I just started learning python and I built this _amazing_ service to help me tag my quotes with images! Give it a try! Don't steal my flag though :angry:

**Difficulty: Medium**

## Solution

Everything is(hopefully) safe, but file is only deleted after the regex check for url. ReDos attack can be used in conjunction with gunicorn's 30s default timeout to prevent the flag file from being deleted, as no check is done 
on the download function. 
https://................................mages.unsplash.com/photo-1707920266055-3c74a15fb947?q=80&w=2574&auto=format&fit=crop something like this base64 encoded should sufficiently lag the server

another better writeup for a redos solution(that uses the same ...... recursive check): https://ctftime.org/writeup/21015
