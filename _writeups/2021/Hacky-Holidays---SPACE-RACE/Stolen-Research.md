---
layout: writeup
title: Stolen Research
ctf: >-
    Hacky Holidays - SPACE RACE
points: 550
solves: 31
tags: 
    - forensics
    - network
    - crypto
date: 2021-08-04
description: |-
    A malicious actor has broken into our research centre and has stolen some important information. Help us investigate their confiscated laptop memory dump!
    
    Note: if you need to crack passwords during this challenge, all potential passwords apear in rockyou-75.txt.
    
    Note 2: the pcap is only relevant for the last subtask.

    ### Kernel release [25 points]
    What sort of OS and kernel is the actor using? Give us the kernel release version (the output of the `uname -r` command).

    ### Tooling [125 points]
    Hope you made a good custom profile in the meantime... The attacker is using some tooling for reconaissance purposes. Give us the parent process ID, process ID, and tool name (not the process name) in the following format: `PPID_PID_NAME`

    ### Password of the actor [100 points]
    What is the password of the actor?

    ### Password of the share [50 points]
    The actor compromised sensitive credentials of the research centre and used them to authenticate to a network share. What is the password of the network share they logged on to?

    ### Stolen information [250 points]
    Unfortunately it looks like very sensitive information was stolen. Can you recover it?
---
