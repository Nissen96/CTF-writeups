---
layout: writeup
title: Space Snacks
ctf: >-
    Hacky Holidays - SPACE RACE
points: 200
solves: 197
tags: 
    - crypto
    - misc
date: 2021-08-04
description: |-
    Find the answers to the treasure hunt to gain access to the cake in the space cafe.

    ### Roten to the core [20 points]
    You find a roten apple next to a piece of paper with 13 circles on and some text. What's the message?

        Vg nccrnef lbh unq jung vg gnxrf gb fbyir gur svefg pyhr
        Jryy Qbar fcnpr pnqrg
        pgs{Lbh_sbhaq_gur_ebg}
        Npprff pbqr cneg 1: QO
    
    ### The roman space empire [25 points]
    You find a page with a roman insignia at the top with some text what could it mean?

        Jhlzhy ulcly dhz clyf nvvk ha opkpun tlzzhnlz.
        jam{Aol_vul_aybl_zhshk}
        jvkl whya: NW
    
    ### The space station that rocked [25 points]
    You hear the heavy base line of 64 speakers from the next compartment. you walk in and the song changes to writing's on the wall, there is some strange code painted on the wall what could it mean?

        RXZlbiAgaW4gc3BhY2Ugd2UgbGlrZSB0aGUgYnV0dGVyeSBiaXNjdXQgYmFzZS4gY3Rme0lfbGlrZV90aGVfYnV0dGVyeV9iaXNjdWl0X2Jhc2V9IC4gQWNjZXNzIHBhcnQgMzogWEQ=
    
    ### What the beep is that? [25 points]
    You hear beeps on the radio, maybe someone is trying to communicate? Flag format: CTF:XXXXXX

        .. -. ... .--. . -.-. - --- .-. / -- --- .-. ... . / .-- --- ..- .-.. -.. / -... . / .--. .-. --- ..- -.. / --- ..-. / -.-- --- ..- .-. / . ..-. ..-. --- .-. - ... .-.-.- / -.-. - ..-. ---... ... .--. .- -.-. . -.. .- ... .... ..--- ----- ..--- .---- / .- -.-. -.-. . ... ... / -.-. --- -.. . ---... / .--- --...
    
    ### The container docker [25 points]
    You are now in the space cafe, the cake is in the container that should not be here. You can see random names on all the containers. What will Docker never name a container? Note: Please enter it as ctf{full_name}

    ### There might be more cake [50 points]
    They ate then cake and left a note with a secret algorithm to unlock the cake treasury. We saw it happening at exactly January 1, 2030 11:23:45 AM... are you the visionary that can figure out the PIN code? PIN code generation algorithm:

        int generatePin() {
            srand(time(0));
            return rand();
        }

    ### Stars in space [30 points]
    The treasury consists of cake hidden on stars in space. 

        * ****  * * * *** ***  **    *  *  * ****  * ** *  ** ***  ** ***  ** * *  *   ** *     *  * ** *  *   ** *     *   **  *   *****  **** *  ***  *  ** * *     * 
---
