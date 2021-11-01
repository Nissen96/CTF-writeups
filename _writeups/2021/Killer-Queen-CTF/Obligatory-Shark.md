---
layout: writeup
title: Obligatory Shark
ctf: Killer Queen CTF
points: 149
solves: 473
tags: 
    - forensics
date: 2021-11-01
description: |-
    Remember to wrap the flag.
flag: kqctf{dancingqueen}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

Opening the file in Wireshark, we see a single Telnet stream.
We right-click and Follow TCP Stream and see a user logging in with username `user2` and password `33a465747cb15e84a26564f57cda0988`. This is likely just an MD5 hash, which we can crack with

```
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-MD5
```
which immediately spits out the password `dancingqueen`. Wrapped in the flag format, this is the correct flag.