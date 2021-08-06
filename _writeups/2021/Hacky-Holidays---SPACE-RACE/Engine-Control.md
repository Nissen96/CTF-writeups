---
layout: writeup
title: Engine Control
ctf: >-
    Hacky Holidays - SPACE RACE
points: 375
solves: 22
tags: 
    - pwn
date: 2021-08-04
description: |-
    These space engines are super powerful. Note: the .py file is merely used as a wrapper around the binary. We did not put any vulnerabilities in the wrapper (at least not on purpose). The binary is intentionally not provided, but here are some properties:
    ```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    ```
    ### Environmental Disaster [75 points]
    These new space engines don't have any regard for their environment. Hopefully you can find something useful.

    ### Control the engine [300 points]
    Can you take control of the engine?
---
