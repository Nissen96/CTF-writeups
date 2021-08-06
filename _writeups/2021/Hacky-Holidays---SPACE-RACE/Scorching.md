---
layout: writeup
title: Scorching
ctf: >-
    Hacky Holidays - SPACE RACE
points: 175
solves: 49
tags: 
    - redteam
    - privesc
date: 2021-08-04
description: |-
    Windows domains are hot. Scorching even.

    ### Password [75 points]
    Can you find out the password for the hash in the file? It is the account for the "NAccount" user.
    
    Hint: The password does not meet the password complexity policy as it is less than 8 characters and only includes letters and numbers.

    ### Scorching [100 points]
    Can you find out the flag hidden in the shared directory for the "SAccount" user? 
    
    Hint: the password is part of rockyou.txt.
---
