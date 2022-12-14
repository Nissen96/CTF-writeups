---
layout: writeup
title: Lovens lange ARM
ctf: NC3 CTF 2022
points: 200
solves: 5
tags: 
    - rev
    - gba
date: 2022-12-13
description: |-
    Okay, krydser lige af på den seje liste: Sinus scroller? Tjek! Snesprites? Tjek! Chiptune? Tjek! En oldschool konsol? Helt sikkert! mr1oo og THeWiZRDs svanesang? Ja, det påstår de.

    Børst din disassembler af og find flaget i denne opgave til Game Boy Advance.

    #StayFrosty
flag: nc3{julesne_i_år}
---
<details>
    <summary>tl;dr</summary>
    Kør GBA-fil med emulator, den tager et input på op til 17 arrow keys i siden - nok den sekvens, der skal findes.<br>
    Decompile GBA binary og søg efter strings for at finde funktionen, der tjekker input.
    Den tjekker at input er 17 arrow keys, og selve sekvensen af key codes kan også findes her.<br>
    Translate key codes til keys og kør i emulatoren, efterfulgt af ENTER, og flaget skrives på skærmen.
</details>

***

## Introduktion

[Spilledrengen__Lovens_lange_ARM.gba]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/Spilledrengen__Lovens_lange_ARM.gba)

Se tl;dr - udvidet forklaring kommer snarest muligt.
