---
layout: writeup
title: Mie and me
ctf: DDC Reunion
points: 50
solves: 
tags: 
    - crypto
date: 2021-10-04
description: |-
    You and your friend, Mie, do not trust Facebook, so when you communicate over Facebook, you always encrypt the messages using Mie’s own python script.
    
    The problem is, that at a critical time, you’ve forgotten your shared 64 byte key!
    
    You and Mie are particapating in a CTF right now, and you know that the last message Mie sent was the flag to the first challenge.
    
    You also remember that Mie sent your team name, CryptogangFTW, not long ago.
flag: HKN{AES_i5_n0t_vu1n_t0_kn0wn-pl4int3xt_4tt4ck}
---
<details> 
    <summary>tl;dr</summary>
    Encryption of a block <code>B = L + R</code> turns out to be <code>(L xor R xor C1) + (L xor C2)</code> for some <code>C1</code> and <code>C2</code>. Use (plaintext, ciphertext) pair of "CryptogangFTW" to find <code>C1</code> and <code>C2</code> with XORs, and use <code>C1</code> and <code>C2</code> to decrypt the entire conversation.
</details>

***

## Introduction

We are given the following encrypted conversation:

    Mie > axhISCBIMF1wOH9yank8eUpST09zGGIKGXR4aWk8c2tMRjUoGi8KLVpwdnF2eXJq
    Me  > ckhVRDFhdxVxeX98Ol9udCEkKEJwTGJMX2xgEBcREQA=
    Mie > bFFbTCNZMFlrfXB0aWhubEpfEUBUekY7XHl6MTouPH4=
    Mie > Z0htZlMgBi56am5tbnN7bA==
    Mie > FVgzIkx3JQVVUyNFampuRQ==
    Me  > bUlQU2cQYnBqbWd4aDI8Xgl6Z2UaIgtlVDglPXd1ciM=
    Mie > dkdFBzgARUJ3cXR4NDxaZH9dUkJwTGJMAxcYEhUTEwI=
    Mie > ayNDVwF9bmVxU1lmW1lPUlFcS3MpDFETTCl5Qm4sQ2ZXRxISY0U/elB2Yy5iaEM5

and the script used for encryption and decryption:

```python
#!/usr/bin/env python3
import sys
import base64
from Crypto.Util.Padding import pad, unpad

# xor with byte strings
def byte_xor(a, b):
    return bytes([_a^_b for _a,_b in zip(a,b)])


def text_to_blocks(text):
    return [text[i:i+16] for i in range(0,len(text),16)]

def blocks_to_text(blocks):
    return b"".join(blocks)

def encrypt(plaintext: bytes, key: bytes) -> (bytes, bytes):
    blocks = text_to_blocks(pad(plaintext,16))
    key_list = [key[i:i+8] for i in range(0,64,8)]
    for j,block in enumerate(blocks):
        for i in range(8):
            left = block[:8]
            right = block[8:]
            block = right + byte_xor(right, byte_xor(key_list[i], left))
        blocks[j] = block
    ciphertext = blocks_to_text(blocks)
    return ciphertext


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    ciphertext = ciphertext
    blocks = text_to_blocks(ciphertext)
    key_list = [key[i:i+8] for i in range(0,64,8)]
    for j,block in enumerate(blocks):
        for i in range(7,-1,-1):
            left = block[:8]
            right = block[8:]
            block = byte_xor(key_list[i], byte_xor(left, right)) + left
        blocks[j] = block
    plaintext = unpad(blocks_to_text(blocks), 16)
    return plaintext


def main():
    key = sys.argv[1].encode()
    assert len(key) == 64
    mode = sys.argv[2]
    plaintext = sys.argv[3].encode()

    if mode == "encrypt":
        ciphertext = encrypt(plaintext, key)
        print(base64.b64encode(ciphertext).decode())
    elif mode == "decrypt":
        plaintext = decrypt(base64.b64decode(plaintext), key)
        print(plaintext)
    else:
        print("Invalid mode selected")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

The script takes a 64-byte `key`, a `mode` (encrypt/decrypt), and a piece of `plaintext`. Choosing "encrypt", `plaintext` is encrypted with `key` and the result base64 encoded. Choosing "decrypt", `plaintext` (here the ciphertext) is passed as base64 and first decoded before decrypting with `key`. 

Let's take a closer look at the encryption function:

```python
def encrypt(plaintext: bytes, key: bytes) -> (bytes, bytes):
    blocks = text_to_blocks(pad(plaintext,16))
    key_list = [key[i:i+8] for i in range(0,64,8)]
    for j,block in enumerate(blocks):
        for i in range(8):
            left = block[:8]
            right = block[8:]
            block = right + byte_xor(right, byte_xor(key_list[i], left))
        blocks[j] = block
    ciphertext = blocks_to_text(blocks)
    return ciphertext
```
First, the plaintext is padded and split in 16-byte blocks, and the key split in eight 8-byte chunks. Then, every block is encrypted individually by repeating the following steps for `i = 1..8`:
    
1. Split the block in two halves, `L` and `R`, and get the `i`th key chunk, `Ki`
2. Concatenate `R` with `(L ^ R ^ Ki)`
3. Overwrite the block with this result, `R + (L ^ R ^ Ki)`

After 8 rounds, the block should be encrypted. This is done for each block, and these are joined together and returned in the end.

## Vulnerability

Let's try understanding the encryption function a bit better by running a block `B = L + R` through it, noting how the two halves of the block are updated throughout the rounds:

| i | L                                | R                                 |
|:--|:---------------------------------|:----------------------------------|
| 1 | `R`                              | `L ^ R ^ K1`                      |
| 2 | `L ^ R ^ K1`                     | `L ^ K1 ^ K2`                     |
| 3 | `L ^ K1 ^ K2`                    | `R ^ K2 ^ K3`                     |
| 4 | `R ^ K2 ^ K3`                    | `L ^ R ^ K1 ^ K3 ^ K4`            |
| 5 | `L ^ R ^ K1 ^ K3 ^ K4`           | `L ^ K1 ^ K2 ^ K4 ^ K5`           |
| 6 | `L ^ K1 ^ K2 ^ K4 ^ K5`          | `R ^ K2 ^ K3 ^ K5 ^ K6`           |
| 7 | `R ^ K2 ^ K3 ^ K5 ^ K6`          | `L ^ R ^ K1 ^ K3 ^ K4 ^ K6 ^ K7`  |
| 8 | `L ^ R ^ K1 ^ K3 ^ K4 ^ K6 ^ K7` | `L ^ K1 ^ K2 ^ K4 ^ K5 ^ K7 ^ K8` |

Although this may look a bit complicated, notice in the end the left half is just the XOR of the original left and right plus some key chunks. Let's just call the XOR of the key chunks `C1`, so the result is `L ^ R ^ C1`. Similarly the resulting right half is just `L ^ C2`.

So, the encryption of a block `B = L + R` is just

    (L ^ R ^ C1) + (L ^ C2)

Let's call these two encrypted halves `S` and `T`, so `enc(B) = S + T` where

    S = L ^ R ^ C1
    T = L ^ C2

This gives us a simple way to find the plaintext `L + R` from the ciphertext `S + T`:

    L = T ^ C2
    R = S ^ L ^ C1

So, if we know `C1` and `C2` for some key, we can decrypt any block of ciphertext encrypted with that key.

But how do we find these? Let's try isolating these instead in the previous equations:

    C1 = S ^ L ^ R
    C2 = T ^ L

We see that we can find `C1` and `C2` if we know a plaintext block `B = L + R` and the corresponding encrypted ciphertext `enc(B) = S + T`. Finding or guessing such a (plaintext, ciphertext) pair is often not very hard, and any scheme vulnerable to such an attack is very weak. This type of attack is called a *known-plaintext attack*.

Notice in this scheme we don't even find the key itself with the attack method, but we can still decrypt everything.

## Exploit

We are told in the challenge text, that Mie at some point sent the message "CryptogangFTW". If we can find the corresponding ciphertext in the encrytped chat, then we have a known (plaintext, ciphertext) pair and we can compute `C1` and `C2`. "CryptogangFTW" fits within a single block, so looking at the encrypted chat, the corresponding cipher is very likely one of the two following:

    Mie > Z0htZlMgBi56am5tbnN7bA==
    Mie > FVgzIkx3JQVVUyNFampuRQ==

Starting from the first, we base64 decode it and split it into its two halves, `S` and `T`. We then compute `C1` and `C2` as explained above:

```python
plain = pad(b"CryptogangFTW", 16)
L, R = plain[:8], plain[8:]

cipher = base64.b64decode("Z0htZlMgBi56am5tbnN7bA==")
S, T = cipher[:8], cipher[8:]

C1 = xor(S, L, R)
C2 = xor(T, L)
```

If we actually got a matching pair, then we can now decrypt the entire chat with the method previously explained:

```python
for cipher in ciphers:  # ciphers is the list of messages after base64 decoding
    decrypted = b""
    for block in text_to_blocks(cipher):
        left = xor(block[8:], C2)
        right = xor(block[:8], C1, left)
        decrypted += left + right
    print(unpad(decrypted, 16).decode())
```
The entire decryption script can be downloaded [here]({{ site.baseurl }}/assets/CTFs/2021/DDC-Reunion/decrypt.py).

This successfully decrypts all messages, so our choice of ciphertext apparently was the one produced by encrypting "CryptogangFTW":

    Mie > I hope there are lots of crypto challenges
    Me  > Haha Cryptogang ftw
    Mie > Registrating a team, 2 sec..
    Mie > CryptogangFTW
    Mie > lK4XpvrH3NU8LM5
    Me  > Super. Starter om 2 min..
    Mie > Nice. First flag:
    Mie > HKN{AES_i5_n0t_vu1n_t0_kn0wn-pl4int3xt_4tt4ck}

We see the conversation is about registering a team for a CTF and "CryptogangFTW" was their team name. The other ciphertext candidate was their password. We get the flag, which seems to hint at using a cryptosystem that is *not* vulnerable to a known-plaintext attack, such as AES: