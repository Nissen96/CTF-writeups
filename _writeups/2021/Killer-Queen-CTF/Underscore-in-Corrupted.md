---
layout: writeup
title: Underscore in Corrupted
ctf: Killer Queen CTF
points: 409
solves: 24
tags: 
    - forensics
date: 2021-11-01
description: |-
    My music is ruined.
flag: kqctf{y0u_r3c0v3r3d_my_m4573rp13c3!_1_c4n_m4k3_34r5_bl33d_4n07h3r_d4y.}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

We are given a sound file with a phone conversation where a lady types in her credit card number on her mobile phone.

The phone is old, so each character emits a different sound -- their Dual-Tone Multi-Frequency (DTMF). Based on these frequencies, we can decode the numbers pressed and get her card number.

This can be done manually by inspecting frequency pairs and using a lookup table, but we can also just download a tool to do it automatically:
https://github.com/ribt/dtmf-decoder

With this, we just run

    ./dtmf.py tippytappiesbutmobile.wav

This doesn't give an output that looks correct, but we can change the interval. Setting it to half a second looks good:

    ./dtmf.py tippytappiesbutmobile.wav -i 0.5

This results in

    14716097646384761

When we listen to the file, we hear she first types in the 1 as an option and then the card number. So we remove the first 1, leaving the 16-digit number, which is the flag when wrapped in the flag format.