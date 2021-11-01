---
layout: writeup
title: Hammer To Fall
ctf: Killer Queen CTF
points: 204
solves: 207
tags: 
    - pwn
date: 2021-11-01
description: |-
    Dynamically sized integers huh?
    (wrap the proper input in a flag wrapper kqctf{number}).
flag: kqctf{2635249153387078802}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

We are presented with the following Python code:

```python
import numpy as np

a = np.array([0], dtype=int)
val = int(input("This hammer hits so hard it creates negative matter\n"))
if val == -1:
	exit()
a[0] = val
a[0] = (a[0] * 7) + 1
if a[0] == -1:
	print("flag!")
```

So we have to find some number that overflows and becomes -1.
More specifically, we want a number that iself is within the ranges of a Python integer AND within the numpy integer, since otherwise it will throw an error at `a[0] = val`, when converting the Python int to a numpy int.

A numpy integer is a 64-bit signed integer:
https://numpy.org/doc/stable/reference/arrays.scalars.html#numpy.int_

meaning it takes values from $-2^{63}$ to $2^{63} - 1$. We want a number which when multiplied by 7 and added to 1 gives -1. We can start out by considering what happens if we just input $\frac{2^{63} - 1}{7}$ - so divide the largest integer by 7. When this input is multiplied by 7, it gets back to the largest possible input, and adding 1, we overflow to the smallest possible value, $-2^{63}$.

This is not exactly what we want, but close - we want to find the midpoint between the smallest and largest integer, not the smallest itself. We can do this by simply multiplying the input by 2.

Inputting $2 \cdot \frac{2^{63} - 1}{7} = 2635249153387078802$, we get exactly back to -1 and this number is the flag (wrapped in the flag format).