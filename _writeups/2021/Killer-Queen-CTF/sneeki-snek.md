---
layout: writeup
title: sneeki snek
ctf: Killer Queen CTF
points: 180
solves: 283
tags: 
    - rev
date: 2021-11-01
description: |-
    ssssssssssssssssssssssssssssssssssssss
flag: kqctf{dont_be_mean_to_snek_:(}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

Manually decompiled:

```python
f = ''
a = 'rwhxi}eomr\\^`Y'
z = 'f]XdThbQd^TYL&\x13g'
a = 'rwhxi}eomr\\^`Y' + 'f]XdThbQd^TYL&\x13g'

for i, b in enumerate(a):
    c = ord(b)
    c -= 7
    c += i
    c = chr(c)
    f += c

print(f)
```