---
layout: writeup
title: Nissezonen
ctf: NC3 CTF 2022
points: 200
solves: 3
tags: 
    - boot2root
    - web
    - sqli
    - rev
    - privesc
date: 2022-12-13
description: |-
    Man kan da ikke have en julectf uden en boot2root... Nisserne har hyret en ny udvikler til at sikre deres server for sårbarheder, hack serveren og se om han er sin vægt værd i gløgg.

    Opgaven kan tilgås her: [Nissezonen](https://tryhackme.com/jr/nissezonen). Start derefter maskinen og få tildelt dens IP-adresse.
flag: <br>nc3{1-0_over_nissedev!}<br>nc3{nissedev_er_taget_paa_juleferie}<br>nc3{To_nisser_men_ingen_gloegg}<br>nc3{Velkommen_i_nissezonen!!!}<br>
---
<details>
    <summary>tl;dr</summary>
    Enumerate serveren og find port 80 åben. Enumerate directories og find <code>/login.php</code>.
    Denne har en login form med POST method, der IKKE er vulnerable.
    Gives login details i stedet som GET parametre i URLen, ER der SQL injection, som giver adgang til første flag.<br><br>
    Ved login redirectes til en side med command injection, kørt af user <code>www-data</code>, hvorfra initial access til serveren kan opnås med reverse shell.<br>
    Her findes brugeren <code>nissedev</code> og i filen <code>con.php</code> findes credentials til SQL databasen.
    Samme password giver SSH-adgang til <code>nissedev</code> og andet flag findes.<br><br>
    Filen <code>/usr/bin/nis</code> har setuid capabilities, og reverses med decompiler.
    Køres den som <code>nis whatever NissedevErGenial</code> kører den <code>/home/nissedev/bash</code> som brugeren <code>nisserik</code>, vi dermed kan escalate til og få tredje flag.<br><br>
    Køres filen i stedet som <code>nisserik</code> med <code>nis whatever NissedevErGenial CMD</code>, køres <code>CMD</code> som root, så vi escalater med <code>nis 0 NissedevErGenial bash</code> og får root shell og sidste flag.
</details>

***

## Introduktion

Se tl;dr - udvidet forklaring kommer snarest muligt.
