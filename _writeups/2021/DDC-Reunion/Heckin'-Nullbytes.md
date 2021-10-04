---
layout: writeup
title: Heckin' Nullbytes
ctf: DDC Reunion
points: 55
solves: 
tags: 
    - crypto
date: 2021-10-04
description: |-
    break the heckin scheme my friend: heckin-nullbytes.hkn:9001
---
<details> 
    <summary>tl;dr</summary>
    <code>R()</code> will never return a <code>\x00</code>-byte, so <code>k ^ R()</code> can never be <code>k</code>. Running <code>k ^ R()</code> until only one value hasn't been returned means that value must be <code>k</code>. Use this on <code>enc1(x)</code> to find <code>k1</code>, on <code>enc2(x)</code> to find <code>k2</code>, and then on <code>flag()</code> to get <code>k1 ^ k2 ^ flag</code>, from which <code>flag</code> can be found.
</details>

***

## Introduction

Connecting to the server, we get 4 options:

    a) flag()
    b) enc1(x)
    c) enc2(x)
    d) info
    inp: 

Looking first at info, this prints

    ------------------------
    flag = ==REDACTED==
    k1 = os.urandom(len(flag))
    k2 = os.urandom(len(flag))
    enc1(x) = k1 ^ x ^ R()
    enc2(x) = k2 ^ x ^ R()
    flag() = k1 ^ k2 ^ flag ^ R()


    The random function R():

    def R():
        return os.urandom(len(flag)).replace(b'\x00', b'\xff')
    ------------------------

So the server stores a flag, chooses two random values `k1` and `k2`, and contains four functions. The function `R()` gets a random number and replaces all instances of the byte `\x00` with `\xff`. The other three functions correspond to the three other options at the prompt. Each of these just XOR a few values together, including a random value from `R()`.

## Vulnerability

Had the random number not been added in the different functions, we could very easily get the flag by just doing:

    enc1(x) ^ enc2(x) ^ flag() = (k1 ^ x) ^ (k2 ^ x) ^ (k1 ^ k2 ^ flag) = flag

But this is not the case, and the added randomness seems to make the scheme secure. The key here is in the title, "Heckin' Nullbytes", and the issue is the fact that `R()` replaces the null byte with something else, meaning no byte returned by `R()` can ever be `\x00`.

Why does this break the scheme? Consider the following simpler case, with a function XORing a secret byte `k` with a byte returned by `R()`:

    enc() = k ^ R()

You can call this function as many times as you want, but you don't know `k` or the result of `R()`, only `k ^ R()`. We know that if `R()` returned `\x00`, the result would be `k ^ \x00 = k`, since XORing by 0 has no effect. But since `R()` never returns 0, we know the only value `enc()` can never return is `k` itself. This means we can keep running `enc()` until only one value hasn't been returned - this must be `k`.

## Exploit

We can exploit this vulnerability in the given scheme. First, we can keep calling `enc1(x)` with the same `x` until only one value hasn't been returned. This must then be `k1 ^ x`, and by XORing with `x` (or just using `x = 0` in the first place), we get `k1`. We do the same with `enc2(x)` to get `k2`.

Finally, we can keep running `flag()` until only one value hasn't been returned. This value must be `k1 ^ k2 ^ flag`, and we can simply get the flag by XORing this with `k1` and `k2` we just found.

This [Python script]({{ site.baseurl }}/assets/CTFs/2021/DDC-Reunion/local_exploit.py) implements the server functionality locally and performs the entire exploit almost immediately. The main exploit function is the following:
```python
def eliminate(fn):
    options = [set(range(256)) for _ in range(len(flag))]
    while not all(map(lambda x: len(x) == 1, options)):
        for k, v in enumerate(fn()):
            if v in options[k]:
                options[k].remove(v)
    return b"".join([bytes(x) for x in options])
```
Here, we first create a list of options left for each byte in the flag. The options are stored in sets, which initially contains all possible byte values, 0-255. Then we enter into a loop, where we call a function `fn` (either `enc1()`, `enc2()`, or `flag()`) which returns a byte string. We go through each byte and remove it from the list of options for the correspodning byte in `options`. We continue running the `while`-loop until just a single option remains for each byte. This *must* then be the correct byte for that position, and we join the bytes and return the result.

Finding `k1`, `k2`, and the actual flag on the server takes some time, as each request eliminates at most one of the 256 possibilities per byte, so for several thousand requests must be sent. The real exploit script can be downloaded [here]({{ site.baseurl }}/assets/CTFs/2021/DDC-Reunion/exploit.py). It works in the exact same way as the local script, there is just more IO-functionality.