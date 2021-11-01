---
layout: writeup
title: jazz
ctf: Killer Queen CTF
points: 232
solves: 152
tags: 
    - rev
date: 2021-11-01
description: |-
    9xLmMiI2znmPam'D_A_1:RQ;Il\*7:%i".R<
flag: jazz{D34D_0N_T1|\/|3_3vgy90N51Fob1s}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

jar file can be decompiled with jd-gui. Encryption function does the following (rewritten to Python):

```python
def encrypt(flag):
    temp = [158 - ord(c) for c in flag]
    print(temp)
    ciphertext = ""
    for i in range(len(temp) // 2):
        t1, t2 = temp[2 * i], temp[2 * i + 1]
        ciphertext += chr((2 * t1 - t2 + 153) % 93 + 33)
        ciphertext += chr((t2 - t1 + 93) % 93 + 33)
    return ciphertext
```

So it first subtracts each character from 158 and then enters a loop where it adds two characters at a time based on some math performed on the two next characters from `temp`.

We can reverse this to create a decryption function. This is a bit difficult since we in the above function really now want to extract `t1` and `t2` from the two next characters in the ciphertext. We look at the first line:

```python
ciphertext += chr((2 * t1 - t2 + 153) % 93 + 33)  # call this c1
```
Reversing this, we get
```python
c1 = chr((2 * t1 - t2 + 153) % 93 + 33)
ord(c1) = (2 * t1 - t2 + 153) % 93 + 33
ord(c1) - 33 = (2 * t1 - t2 + 153) % 93  # let's ignore the modulo for now
ord(c1) - 33 - 153 = 2 * t1 - t2  # call this x
```

from the next line:
```python
ciphertext += chr((t2 - t1 + 93) % 93 + 33)  # call this c2
```
we get
```python
c2 = chr((t2 - t1 + 93) % 93 + 33)
ord(c1) = (t2 - t1 + 93) % 93 + 33
ord(c1) - 33 = t2 - t1 + 93  # ignore modulo again
ord(c1) - 33 - 93 = t2 - t1  # call this y
```

So now we have an expression for `t2 - t1` and `2 * t1 - t2` -- two equations with two unknowns. If we just add them, we get

```python
(t2 - t1) + (2 * t1 - t2) = t1 = x + y
```
and knowing `t1`, we get
```python
(t2 - t1) + t1 = t2 = y + t1
```
So now we (almost) have the two original characters! All there is left is we need to take the result modulo 93 in some of the cases (we don't know which, that was lost when doing the original modulo in the encryption). Instead, we just do modulo on each and subtract them from 158 to reverse the final part. And if this result is above 127 (not ASCII), then we know we shouldn't have done modulo on this, so we subtract 93 again. See script below:

```python
def decrypt(ciphertext):
    temp = []
    for i in range(len(ciphertext) // 2):
        c1, c2 = ciphertext[2 * i], ciphertext[2 * i + 1]
        x = ord(c1) - 33 - 153  # reversing first equation
        y = ord(c2) - 33 - 93   # reversing second equation
        t1 = x + y              # solve two equations with two unknowns
        t2 = y + t1
        temp.extend([t1, t2])
    flag = ""
    for n in temp:
        r = 158 - (n % 93)  # do modulo before subtracting
        if r > 127:  # except when you shouldn't have!
            r -= 93  # then fix
        flag += chr(r)
    return flag
```
Inputting the encrypted flag to this gives us back the original flag (minus the final curly brace due to an odd length flag)