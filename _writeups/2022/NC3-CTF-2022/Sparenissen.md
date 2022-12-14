---
layout: writeup
title: Sparenissen
ctf: NC3 CTF 2022
points: 200
solves: 3
tags: 
    - forensics
    - compression
date: 2022-12-13
description: |-
    Sparenissen har været på spil, hvad har han egentlig gang i?
flag: nc3{sparenissen-synes-det-er-enormt-hyggeligt-og-lidt-sjovt-med-et-laaaangt-flag-i-en-lille-kort-fil}
---
<details>
    <summary>tl;dr</summary>
    Den binære fil er compressed, og konverteres først til bits.
    Den komprimerede bitstring består af to typer datafelter, der enten starter med 0 eller 1.<br>
    Starter feltet med 0, er de efterfølgende 7 bits en ny ASCII-værdi.
    Denne skrives ned og appendes til en liste over fundne chars.<br>
    Starter feltet med 1, er de efterfølgende 5 bits et index ind i den liste, og karakteren ved det index skrives ned.<br>
    På den måde bruges i alt 8 bits på hver ny karakter, men derefter kun 6 for hver gentagen brug.
</details>

***

## Introduktion

Vi får givet ZIP-filen [sparenissen.zip]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/sparenissen.zip) med de to filer `sparenissen.txt` og `sparenissen`. Tekstfilen indeholder et lille digt:

```

	Sparenissen skriver kort og trangt,
	hilser ikke først,
	og siger ej farvel,
	modsætter sig størst,
	at gentage sig selv,
	hvordan kan brevet blive stort og langt.

```

og `sparenissen` er en binær fil, vi kan køre `xxd` på for at få hexdump:

```
00000000: 6e63 337b 7370 6172 6581 a649 2880 b647  nc3{spare..I(..G
00000010: 9828 92a6 4a1d 2aa2 7aa8 81be 76db 6a68  .(..J.*.z...v.jh
00000020: ad9f 1a1b 29c6 daae c6ac a9b2 daa4 6ab9  ....).........j.
00000030: dada afa2 caa8 b6ac a69a 69a0 c6da 99b2  ..........i.....
00000040: 9b1a a9aa 882a ca9c b2a2 a6bb a7b6 ad69  .....*.........i
00000050: c9f4                                     ..
```

Vi ser her først starten på et flag som almindelig ASCII-tekst, men herefter er resten umiddelbart ulæseligt.

## Analyse

Digtet hinter meget til komprimering - teksten er "kort og trang", men brevet skal blive "stort og langt". "hilser ikke først og siger ej farvel" kunne hinte mod enten manglende header og footer eller mod at nogle unødvendige bits fjernes for at komprimere indholdet. F.eks. bruger ASCII chars kun 7 bits, men gemmes typisk i en 8-bit byte. Eller måske hinter det bare til, at resultatet ikke indeholder noget overflødigt.

Sidst kunne "modsætter sig størst at gentage sig selv" hinte til at samme karakter aldrig skrives to gange. Med mange komprimeringsteknikker skrives hver karakter kun første gang, den optræder i teksten. De resterende gange refereres til den første for at spare bits.

Denne hypotese passer umiddelbart godt på den komprimerede tekst, hvor vi i starten ser en række ASCII-karakterer, der hver optræder første gang. En fornuftig antagelse er, at næste bid af flaget er `nissen`, så det starter med `nc3{sparenissen`. Dette kan stadig passe fint, da næste karakter så er `n`, og da den allerede er brugt, er det ikke nødvendigt at skrive den igen. Men hvordan refereres der så til den første forekomst?

Vi kan starte med at konvertere filen til bits, så vi bedre kan se, hvad der foregår. Dette gøres nemt med Python:

```py
with open("sparenissen", "rb") as f:
    data = f.read()

bits = "".join([bin(c)[2:].zfill(8) for c in data])
```

Koden konverterer hver byte til 8 bits og concatenater dem, så vi får et samlet output. Printer vi det, får vi et stort output:

```
 01101110011000110011001101111011011100110111000001100001011100100110010110000001
 10100110010010010010100010000000101101100100011110011000001010001001001010100110
 01001010000111010010101010100010011110101010100010000001101111100111011011011011
 01101010011010001010110110011111000110100001101100101001110001101101101010101110
 11000110101011001010100110110010110110101010010001101010101110011101101011011010
 10101111101000101100101010101000101101101010110010100110100110100110100110100000
 11000110110110101001100110110010100110110001101010101001101010101000100000101010
 11001010100111001011001010100010101001101011101110100111101101101010110101101001
 1100100111110100
```

Vi ved, hvad de første bytes er og noterer dette:

```
 01101110 : n
 01100011 : c
 00110011 : 3
 01111011 : {
 01110011 : s
 01110000 : p
 01100001 : a
 01110010 : r
 01100101 : e
 10000001101001100100100100101000100000001011011001000111100110000010100010010010
 10100110010010100001110100101010101000100111101010101000100000011011111001110110
 11011011011010100110100010101101100111110001101000011011001010011100011011011010
 10101110110001101010110010101001101100101101101010100100011010101011100111011010
 11011010101011111010001011001010101010001011011010101100101001101001101001101001
 10100000110001101101101010011001101100101001101100011010101010011010101010001000
 00101010110010101001110010110010101000101010011010111011101001111011011010101101
 011010011100100111110100
```

Hvis vores antagelse holder stik, skal de næste bits referere til det første `n`, og herefter bør vi have 8 bits, der svarer til ASCII-værdien for `i`, altså `01101001` i bits. Den sekvens er nem at identificere, og vi ser faktisk, at nemlig de bits optræder kort efter:

```
 01101110 : n
 01100011 : c
 00110011 : 3
 01111011 : {
 01110011 : s
 01110000 : p
 01100001 : a
 01110010 : r
 01100101 : e
 100000   : n?
 01101001 : i
 10010010010010100010000000101101100100011110011000001010001001001010100110010010
 10000111010010101010100010011110101010100010000001101111100111011011011011011010
 10011010001010110110011111000110100001101100101001110001101101101010101110110001
 10101011001010100110110010110110101010010001101010101110011101101011011010101011
 11101000101100101010101000101101101010110010100110100110100110100110100000110001
 10110110101001100110110010100110110001101010101001101010101000100000101010110010
 10100111001011001010100010101001101011101110100111101101101010110101101001110010
 0111110100
```

Vi ved stadig ikke, hvordan `n` decodes mellem `e` og `i`, men vi kan se, der bruges seks bits på det. De næste to karakterer bør begge være `s`, og det passer perfekt, da de næste to sekvenser af seks bits er ens. Vi ved også at de to efterfølgende karakterer er `e` og `n`, der begge har været brugt før, så vi antager at de også er seks bits, og ser på de sekvenser, vi har identificeret:

```
 01101110 : n
 01100011 : c
 00110011 : 3
 01111011 : {
 01110011 : s
 01110000 : p
 01100001 : a
 01110010 : r
 01100101 : e
 100000   : n?
 01101001 : i
 100100   : s?
 100100   : s?
 101000   : e?
 100000   : n?
 00101101100100011110011000001010001001001010100110010010100001110100101010101000
 10011110101010100010000001101111100111011011011011011010100110100010101101100111
 11000110100001101100101001110001101101101010101110110001101010110010101001101100
 10110110101010010001101010101110011101101011011010101011111010001011001010101010
 00101101101010110010100110100110100110100110100000110001101101101010011001101100
 10100110110001101010101001101010101000100000101010110010101001110010110010101000
 101010011010111011101001111011011010101101011010011100100111110100
```

Vi ser her, at begge instanser af `n` encodes med `100000`, `e` med `101000` og `s` med `100100`.
Måske kan du nu spotte et mønster: nye karakterer starter med `0`, efterfulgt af de syv bits, der udgør ASCII-værdien. Når en karakter optræder igen, starter den i stedet altid med `1`, efterfulgt af fem bits. Så første bit i hver sekvens afgør, hvilken type det er.

De fem resterende bits er `00000 = 0` for `n`, `01000 = 8` for `e` og `00100 = 4` for `s`. Det passer præcis med den rækkefølge, karaktererne forekommer i:

```
0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8
n | c | 3 | { | s | p | a | r | e
```

Så når en karakter forekommer anden gang bruges indekset på den første forekomst i listen over brugte karakterer.
Dvs. hver gang f.eks. `p` forekommer, vil vi forvente at se sekvensen `100101` - et 1-tal efterfulgt af `00101 = 5`. Det sparer på den måde to bits på hver eneste gentagen karakter. Hver gang en ny karakter forekommer, lægger vi den til listen over brugte karakterer, så vi kan referere til dens indeks senere. F.eks. vil `i` placeres som næste element på indeks `9`.

Vi tjekker om dette passer med de næste bits - når vi ser et 0 har vi en ny 7-bit karakter, og et 1 har vi en reference til en foregående:

```
 01101110 : n
 01100011 : c
 00110011 : 3
 01111011 : {
 01110011 : s
 01110000 : p
 01100001 : a
 01110010 : r
 01100101 : e
 100000   : n  (0)
 01101001 : i
 100100   : s  (4)
 100100   : s  (4)
 101000   : e  (8)
 100000   : n  (0)
 00101101 : _
 100100   : s  (4)
 01111001 : y
 100000   : n  (0)
 101000   : e  (8)
 100100   : s  (4)
 101010   : _  (10)
 01100100101000011101001010101010001001111010101010001000000110111110011101101101
 10110110101001101000101011011001111100011010000110110010100111000110110110101010
 11101100011010101100101010011011001011011010101001000110101010111001110110101101
 10101010111110100010110010101010100010110110101011001010011010011010011010011010
 00001100011011011010100110011011001010011011000110101010100110101010100010000010
 10101100101010011100101100101010001010100110101110111010011110110110101011010110
 10011100100111110100
```

Vi har `_` som næste karakter, der altså får index `10` i listen over fundne karakterer:

```
0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10
n | c | 3 | { | s | p | a | r | e | i | _
```

Og rigtig nok ser vi kort tid efter en reference til `10`, som passer med `_`, og vi har `nc3{sparenissen_synes_` som start på flaget.

Dekomprimeringen automatiseres nemt med Python:

```py
with open("sparenissen", "rb") as f:
    data = f.read()

bits = "".join([bin(c)[2:].zfill(8) for c in data])


flag = ""
chars = []
i = 0
while i < len(bits):
    if bits[i] == "0":
        # Bit er 0 = næste 7 bits er ny char
        char = chr(int(bits[i:i + 8], 2))
        flag += char
        chars.append(char)  # Gem i listen over brugte chars
        i += 8
    else:
        # Bit er 1 = næste 5 bits er index i listen over brugte chars
        idx = int(bits[i + 1:i + 6], 2)
        flag += chars[idx]
        i += 6
```

Køres dette får vi hele flaget dekomprimeret. Dette er givetvis en velkendt komprimeringsalgoritme, men jeg har ikke forsøgt at finde den efterfølgende.
