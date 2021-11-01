---
layout: writeup
title: She's A Killed Queen
ctf: Killer Queen CTF
points: 290
solves: 86
tags: 
    - forensics
date: 2021-11-01
description: |-
    My picture has been corrupted. Can you fix it?
flag: kqctf{SHES_A_KILLED_QUEEN_BY_THE_GUILLOTINE_RANDOMCHRSIADHFKILIHASDKFHQIFPXKRL}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

We are given a corrupted PNG image. Expecting it, we find that width and height have both been set to 0. The CRC code therefore isn't correct.

Fixing the CRC code doesn't help, since the image is still set as a 0x0 one. What we instead need to do is find the heigth and width values that will make the provided CRC code correct.

We can fairly quickly bruteforce our way through this. We extract the IHDR info and write a script that tries inserting every possible width and height, compute the CRC and check if it matches. We try just up to 2000 for both width and height:

```python
for i in range(2000):
    for j in range(2000):
        width = i.to_bytes(4, byteorder='big')
        height = j.to_bytes(4, byteorder='big')
        a = b"\x49\x48\x44\x52" + width + height + b"\x08\x06\x00\x00\x00"
        crc_code = crc(a)
        if crc_code == 0x0DB3F6C0:
            print(width, height)
            exit()
```

where we use the following code to compute the CRC:
```python
crc_table = None

def make_crc_table():
  global crc_table
  crc_table = [0] * 256
  for n in range(256):
    c = n
    for k in range(8):
        if c & 1:
            c = 0xedb88320 ^ (c >> 1)
        else:
            c = c >> 1
    crc_table[n] = c

make_crc_table()

def update_crc(crc, buf):
  c = crc
  for byte in buf:
    c = crc_table[int((c ^ byte) & 0xff)] ^ (c >> 8)
  return c

def crc(buf):
  return update_crc(0xffffffff, buf) ^ 0xffffffff
```

We quickly get the output `b'\x00\x00\x04\xb0' b'\x00\x00\x02\xa3'` and we can insert those as the width and height in the image using `hexedit`.

The image is now repaired and can be opened. It just shows a painting of a queen:
![Queen](https://i.imgur.com/rW91umj.png)
Opening the image in `stegsolve`, we look through the different channels and planes. In all three RGB channels, plane 0 hides another image in the least significant bit:
![Cipher](https://i.imgur.com/5DqcFqv.png)
Googling a bit, we find this to be the "Mary Stuart Code", used by the Mary Queen of Scots, which can be decrypted here:
https://www.dcode.fr/mary-stuart-code
Typing in each character, we convert to ASCII and get the flag: