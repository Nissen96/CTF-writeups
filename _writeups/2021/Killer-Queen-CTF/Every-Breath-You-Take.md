---
layout: writeup
title: Every Breath You Take
ctf: Killer Queen CTF
points: 193
solves: 237
tags: 
    - forensics
    - osint
date: 2021-11-01
description: |-
    I would play video games and always feel like somebody's watchin' me.
    So I changed my username into my current one.
    Find the username I was using before sampinkerton.
flag: kqctf{wh0s_pl41ng_7r1k50n_m3?__e2q3}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

Based on this, it seems like we should find a gaming profile with username `sampinkerton`, likely Steam.

We can directly check if a user with that username exists by going to https://steamcommunity.com/id/sampinkerton. This does return a user, and we can click the small dropdown to find other handles for this user. There is only one other:

> wh0s_pl41ng_7r1k50n_m3?__e2q3

which wrapped in `kqctf{}` is the flag.