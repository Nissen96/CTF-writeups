---
layout: writeup
title: sneeki snek 2 oh no what did i do
ctf: Killer Queen CTF
points: 189
solves: 249
tags: 
    - rev
date: 2021-11-01
description: |-
    Did snek steal your pasta because this is some spaghetti.
flag: kqctf{snek_waas_not_so_sneeki}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

Manual decompilation:
```python
a = [
    1739411,
    1762811,
    1794011,
    1039911,
    1061211,
    1718321,
    1773911,
    1006611,
    1516111,
    1739411,
    1582801,
    1506121,
    1783901,
    1783901,
    1773911,
    1582801,
    1006611,
    1561711,
    1039911,
    1582801,
    1773911,
    1561711,
    1582801,
    1773911,
    1006611,
    1516111,
    1516111,
    1739411,
    1728311,
    1539421
]

b = ""
for i in a:
    c = str(i)[::-1]
    c = c[:-1]
    c = int(c)
    c ^= 5
    c -= 55555
    c //= 555
    b += chr(c)

print(b)
```