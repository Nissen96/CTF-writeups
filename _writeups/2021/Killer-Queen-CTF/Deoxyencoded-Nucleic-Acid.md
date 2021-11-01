---
layout: writeup
title: Deoxyencoded Nucleic Acid
ctf: Killer Queen CTF
points: 283
solves: 92
tags: 
    - crypto
date: 2021-11-01
description: |-
    Adenine, thymine, guanine, and cytosine.
    Theres only four, which was really convenient.
flag: kqctf{its_basica11y_base_four}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

We are given a short DNA string:

    TGGCTCATTGACTCTATGTGTCGCTGGTTCTATCACTTCCTGAGTGATTCACTGGTTGACTGATACATACATTCGTTTCCTGAGTGATTCACTGTTTTCCTGTGTGCCTCTTTCAGTCCT

From the title including "encoded" we can guess they have just used a basic encoding scheme. The simplest one with four possible characters is to assign a bit pair per character. In the standard ATGC order this would be

    A: 00
    T: 01
    G: 10
    C: 11

Converting each character to the bit pairs, we get

    011010110111000101100011011101000110011001111011011010010111010001110011010111110110001001100001011100110110100101100011011000010011000100110001011110010101111101100010011000010111001101100101010111110110011001101111011101010111001001111101

Assuming these are 8-bit bytes, we split them in bytes, convert to ASCII and print the characters. The final Python script for this is:

```python
dna = "TGGCTCATTGACTCTATGTGTCGCTGGTTCTATCACTTCCTGAGTGATTCACTGGTTGACTGATACATACATTCGTTTCCTGAGTGATTCACTGTTTTCCTGTGTGCCTCTTTCAGTCCT"
mappings = {"A": "00", "T": "01", "G": "10", "C": "11"}
mapped = "".join([mappings[c] for c in dna])
characters = [chr(int(mapped[i:i + 8], 2)) for i in range(0, len(s), 8)]
flag = "".join(characters)
```
Printing the flag we get