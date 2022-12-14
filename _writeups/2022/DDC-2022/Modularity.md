---
layout: writeup
title: Modularity
ctf: DDC 2022
points: 1
solves: 
tags: 
    - crypto
date: 2022-03-20
description: |-
    Moderne krypteringssystemer gør stor brug af modulære aritmetiske og algebraiske operationer.

    Her er et hjemmebygget krypteringssystem baseret på disse operationer, kan du implementere dekrypteringen og knække chifferteksten?

    Chifferteksten er krypteret med en firecifret streng mellem 0000 og 9999.

    [Download](/assets/CTFs/2022/DDC-2022/Modularity.zip)
flag: DDC{youtu.be/wfG6z5J4PRI}
---
<details>
    <summary>tl;dr</summary>
    Krypteringen foregår ved 128 gange at anvende en funktion, der først foretager modulær multiplikation, så modulær addition og til sidst modulær eksponentiering. Hver af de tre operationer kan inverteres, for at gå modsatte vej og dekryptere. Først den modulære eksponentiering ved at opløfte resultatet i den multiplikative inverse af <code>c</code> modulo <code>p - 1</code>. Så den modulære addition ved at trække <code>b</code> fra, modulo <code>p</code>. Og sidst den modulære multiplikation ved at gange med den multiplikative inverse af <code>a</code> modulo <code>p</code>. Dette gentages 128 gange, og her skal de samme tilfældige tal bruges som i krypteringen. Det sikres ved at seede med samme password, hvilket kan bruteforces.
</details>

***

## Introduktion

Vi får givet to filer, `algebra.py` og `output.txt`. Tekstfilen indeholder det krypterede flag og et primtal, der blev brugt til krypteringen:
```
p = 97953958723054470944201407781333999671402425802271290596631886639255617548503
ciphertext = 69494773765711558796303044899201719046500256450239245029456014825686379192778
```
Python scriptet indeholder selve krypteringskoden og viser os, hvordan flaget blev læst og krypteret:
```python
import random

# 256 bit prime
p = 97953958723054470944201407781333999671402425802271290596631886639255617548503

# Encrypt a plaintext using a password
def encrypt(plaintext, pw):
    random.seed(pw)
    encryption = plaintext
    for i in range(128):
        a = random.randint(2, 2**255)
        b = random.randint(2, 2**255)
        c = random.randint(2, 2**255)
        if c % 2 == 0:
            c -= 1
        encryption = pow((a * encryption + b) % p, c, p)
    return encryption

# Decrypt ciphertext using a password
def decrypt(ciphertext, pw):
    # TODO: Implement decryption
    return ciphertext


if __name__ == '__main__':
    # Read the flag from a file
    with open("flag.txt", "rb") as f:
        flagbytes = f.read().strip()

    # flag starts with the flag prefix, `DDC{`
    assert flagbytes.startswith(b'DDC{')

    # convert bytes to integer
    flag = int.from_bytes(flagbytes, 'big')

    # How to convert the integer back to bytestring
    assert flagbytes == int.to_bytes(flag, (flag.bit_length() + 7) // 8, 'big')

    # Generates a password containing a 4 digit password between 0000 and 9999
    pw = str(random.randint(0, 9999)).zfill(4)

    print(pw)

    # Write the encrypted flag to the output.txt file!
    with open('output.txt', 'w') as f:
        f.write(f'p = {p}\n')
        f.write(f'ciphertext = {encrypt(flag, pw)}')
```
Vi ser, at `main`-funktionen først læser flaget fra en fil, tjekker om det starter med `DDC{`, og konvereter det fra bytes til en integer. Herefter vælges et tilfældigt 4-cifret password, som gives til krypteringsfunktionen `encrypt()` sammen med flaget.

Lad os tage et nærmere kig på selve krypteringskoden:
```python
def encrypt(plaintext, pw):
    random.seed(pw)
    encryption = plaintext
    for i in range(128):
        a = random.randint(2, 2**255)
        b = random.randint(2, 2**255)
        c = random.randint(2, 2**255)
        if c % 2 == 0:
            c -= 1
        encryption = pow((a * encryption + b) % p, c, p)
    return encryption
```
Funktionen starter med at bruge det valgte password som seed til `random` - dvs. giver vi samme seed en anden gang, vil vi få samme ciphertext som output. Herefter køres 128 runder, hvor `encryption` sættes til `pow((a * encryption + b) % p, c, p)`, hvor `a`, `b` og `c` er tilfældige tal mellem $$2$$ og $$2^{255}$$ og `p` er primtallet fra filen. Skrevet med mere matematisk notation, har vi altså følgende funktion:

$$ enc(e) = (e \cdot a + b)^{c} \mod p $$

Vores opgave er nu at forsøge at skrive dekrypteringskoden, så vi kan få flaget.

## Dekryptering

For at dekryptere flaget, skal vi gøre to ting:

1. Finde det rigtige password
2. Reverse krypteringskoden

### Password

Passwordet bruges som seed, og seedet afgør, hvilke tilfældige tal `random.randint()` returner. Vi har derfor brug for at kende passwordet, der blev brugt til kryptering af flaget, så vi får de samme tilfældige tal til vores dekryptering.

Vi er så heldige, at passwordet kun består af fire cifre, så det kan bruteforces relativt hurtigt. Dvs. når vi har skrevet dekrypteringskoden, kan vi forsøge at køre den på vores ciphertext med alle de 10000 mulige passwords og tjekke, om resultatet bliver en bytestring, der starter med `DDC{`.

Vi kan bruteforce og tjekke resultatet med følgende code snippet:
```python
ciphertext = 69494773765711558796303044899201719046500256450239245029456014825686379192778

for i in range(10000):
    pw = str(i).zfill(4)
    decrypted = decrypt(ciphertext, pw)
    plaintext = int.to_bytes(decrypted, (decrypted.bit_length() + 7) // 8, 'big')
    
    if plaintext.startswith(b"DDC{"):
        print(f"Password: {pw}")
        print(f"Flag: {plaintext.decode()}")
        break
```

### Reversing

For at dekryptere flaget skal vi reverse krypteringskoden, så vi får en dekrypteringsfunktion, der gør det præcis modsatte af krypteringen. Til det skal vi finde den inverse funktion af krypteringsfunktionen vi så tidligere, og så anvende den 128 gange på ciphertexten.

Vi har også brug for de samme tilfældige tal, som nu skal bruges i omvendt rækkefølge. Den del kan vi håndtere ved at generere alle de samme tal og så poppe dem fra listens slutning i hver runde:
```python
def decrypt(ciphertext, pw):
    random.seed(pw)

    # Generer alle 3 * 128 tilfældige tal brugt
    randints = [random.randint(2, 2**255) for _ in range(3 * 128)]
    
    decryption = ciphertext
    for _ in range(128):
        # Pop de tilfældige tal fra listens slutning i omvendt rækkefølge
        c = randints.pop()
        if c % 2 == 0:
            c -= 1
        b = randints.pop()
        a = randints.pop()

        # Sidste step
        decryption = ???
    
    return decryption
```

Det sidste vi mangler er også hoveddelen i opgaven: at invertere funktionen

$$ enc(e) = (e \cdot a + b)^{c} \mod p $$

Vi har altså brug for at finde ud af, hvordan vi går fra $$enc(e)$$ tilbage til $$e$$. Vi kan se, at inputtet først ganges med $$a$$, herefter lægges $$b$$ til, og så opløftes det hele i $$c$$. Alt det gøres modulo $$p$$. Hvis det ikke blev gjort modulo $$p$$ ville funktionen være enkel at invertere:

$$ enc(e) = (e \cdot a + b)^{c} $$

$$ \sqrt[c]{enc(e)} = e \cdot a + b $$

$$ \sqrt[c]{enc(e)} - b = e \cdot a $$

$$ \frac{\sqrt[c]{enc(e)} - b}{a} = e $$

Det er samme steps, vi nu skal igennem, men udfordringen ligger i, at alt gøres modulo $$p$$ - hvilket nok er årsagen til opgavens titel.

Vi skal altså finde ud af, hvordan vi får inverteret de tre operationer, der udføres:

1. Modulær multiplikation: $$x \cdot a \mod p$$
2. Modulær addition: $$x + b \mod p$$
3. Modulær eksponentiering: $$x^c \mod p$$

#### Modulær multiplikation

Vi arbejder her med heltal modulo $$p$$, og her er den modsatte operation af multiplikation ikke division, som vi normalt kender det. Det gælder altså *ikke* at

$$ y \equiv x \cdot a \mod p \quad \Leftrightarrow \quad \frac{y}{a} \equiv x \mod p $$

i hvert fald ikke, hvis vi forstår $$\frac{y}{a}$$ som almindelig division. Vi kan dog også forstå almindelig division som, at vi ganger med det inverse af et tal. Så

$$ \frac{a}{a} = a \cdot a^{-1} $$

og $$a^{-1}$$ er det tal, der giver $$1$$, når vi ganger det med $$a$$:

$$ a \cdot a^{-1} = 1 $$

Det er samme princip vi bruger i modulær aritmetik. Her vil (nogle) tal $$a$$ have en *modulær multiplikativ invers*, $$a^{-1}$$, som ligesom før er det tal, der sikrer at

$$ a \cdot a^{-1} \equiv 1 \mod p $$

For altså at komme fra $$x \cdot a \mod p$$ til $$x$$, skal vi finde $$a$$s modulære multiplikative invers modulo $$p$$ og gange med den, da

$$ x \cdot a \cdot a^{-1} \equiv x \cdot 1 \equiv x \mod p $$

Hvordan finder vi den? Til det kan vi bruge *Euklids udvidede algoritme*. Forklaringen bliver lidt teknisk og kan evt. skippes, men i Python er det meget nemt: Det er indbygget i `pow` funktionen, så for at finde $$a^{-1} \mod p$$ kan du bruge `pow(a, -1, p)`.

Teknisk forklaring: Euklids algoritme finder den største fælles divisor (`gcd` - greatest common divisor) for to tal, $$gcd(x, y)$$. Det er det største tal, der går op i både $$x$$ og $$y$$. Hvis det tal er $$1$$, er der altså ingen tal (udover $$1$$), der går op i begge tal, og så kaldes de *indbyrdes primiske* (co-prime). Bruger man Euklids *udvidede* algoritme får man samtidig de to tal $$u$$ og $$v$$, der gør at

$$ u \cdot x + v \cdot y = gcd(x, y) $$

Hvad kan vi bruge det til? Først og fremmest skal vi huske, at

$$ x \equiv y \mod p $$

betyder, at

$$ x + q \cdot p = y $$

for et eller andet $$q$$. Det vil altså sige, at når vi har

$$ a \cdot a^{-1} \equiv 1 \mod p$$

betyder det at

$$ a \cdot a^{-1} + q \cdot p = 1 $$

Hvis vi bruger Euklids udvidede algoritme til at finde $$gcd(a, p)$$ og hvis det viser sig at $$gcd(a, p) = 1$$, får vi altså som output præcis de to tal $$a^{-1}$$ og $$q$$, der får ligningen til at gå op (her er vi ligeglade med $$q$$). Det virker kun, hvis $$gcd(a, p) = 1$$ -- ellers er den inverse udefineret og findes ikke for det $$a$$.

I vores tilfælde er $$p$$ et primtal, og det er altså indbyrdes primisk med alle tal, der ikke indeholder $$p$$ som en faktor. Det gælder for alle tal $$a$$ i opgaven, så vi vil altid have $$gcd(a, p) = 1$$ og kan finde den inverse med Euklids udvidede algoritme (indbygget i Python's `pow` funktion).


#### Modulær addition

Dette er den simpleste operation at invertere, det er bare at trække fra, da $$x + b - b \equiv x \mod p$$.

#### Modulær eksponentiering

Den mest komplekse operation af de tre er modulær eksponentiering, men en stor del af den nødvendige forståelse blev gennemgået ved modulær multiplikation. Generelt gælder, at hvis vi har

$$ x^c \mod n $$

så kan vi invertere den operation ved at opløfte udtrykket i $$c$$s invers modulo $$\phi(n)$$, altså det tal $$d$$ som sikrer at

$$ c \cdot d \equiv 1 \mod \phi(n) $$

Hvis ovenstående gælder, og vi opløfter det oprindelige udtryk i $$d$$, får vi

$$ (x^c)^d \equiv x^{(c \cdot d)} \equiv x^1 \equiv x \mod n $$

Som vi så ved modulær multiplikation, er det et krav, at $$gcd(c, \phi(n)) = 1$$, ellers eksisterer denne inverse ikke. Måske du undrer dig over, hvor $$\phi(n)$$ pludselig kommer fra. Det forklares om lidt til de interesserede, men for et primtal gælder, at $$\phi(p) = p - 1$$. Så i vores tilfælde, hvor vi har

$$ x^c \mod p $$

kan denne operation inverteres ved at finde $$c$$s invers modulo $$\phi(p) = p - 1$$ (lad os kalde den $$d$$) og opløfte udtrykket i det tal, altså:

```python
d = pow(c, -1, p - 1)  # cs multiplikative invers modulo phi(p)
inverted = pow(x, d, p)
```
Skip til næste overskrift, hvis du er ligeglad med, hvorfor det virker - altså hvorfor lige præcis denne operation inverterer den oprindelige.

Teknisk forklaring: $$\phi$$ kaldes Eulers totientfunktion, og $$\phi(n)$$ returnerer antallet af positive heltal mindre end $$n$$, der er indbyrdes primiske med $$n$$. Hvis det er et primtal, $$p$$, er *alle* tal mindre end $$p$$ indbyrdes primiske med $$p$$, og derfor er $$\phi(p) = p - 1$$.

Vi skal om lidt bruge Fermats lille sætning. Den siger at

$$ a^p \equiv a \mod p $$

hvis $$p$$ er et primtal. Eller ækvivalent (ved at gange med $$a^{-1}$$ på begge sider) at

$$ a^{p - 1} \equiv 1 \mod p $$

Eulers sætning generaliserer dette og siger, at hvis $$gcd(a, \phi(n)) = 1$$ gælder

$$ a^{\phi(n)} \equiv 1 \mod n $$

Her er Fermats lille sætning det specialtilfælde, hvor $$n$$ er et primtal, da $$\phi(p) = p - 1$$.

Lad os prøve nu at bruge Euklids udvidede algoritme til at finde $$c$$s invers modulo $$\phi(p)$$. For at vi kan det, skal $$gcd(x, \phi(p)) = 1$$. Lad os lige tjekke, at det gælder i vores opgave. Her er

$$\phi(p) = p - 1 = 97953958723054470944201407781333999671402425802271290596631886639255617548502$$

Hvis vi faktoriserer det (f.eks. ved at slå det op på factordb.com), får vi primtalsfaktoriseringen

$$ p - 1 = 2 \cdot 48976979361527235472100703890666999835701212901135645298315943319627808774251 $$

Dvs. at $$gcd(c, p - 1) = 1$$ for alle $$c$$, der ikke kan skrives som

$$ x \cdot 2 + y \cdot 48976979361527235472100703890666999835701212901135645298315943319627808774251 $$

hvor $$x$$ og $$y$$ er positive heltal. Koden tjekker om `c % 2 == 0`, og hvis det er tilfældet trækker den 1 fra $$c$$. Det sikrer at $$gcd(c, p - 1) = 1$$ i alle andre tilfælde end $$c = 48976979361527235472100703890666999835701212901135645298315943319627808774251$$, som må siges at være en meget usandsynlig edge case.

Så vi ved altså at $$c$$ (næsten) altid har en invers modulo $$p - 1$$, og vi kan finde den med Euklids udvidede algoritme, der giver os $$d$$ og $$q$$ sådan at

$$ c \cdot d + q \cdot (p - 1) = 1 $$

Vi kan isolere $$c \cdot d - 1$$:

$$ c \cdot d + q \cdot (p - 1) = 1 \quad \Leftrightarrow \quad c \cdot d - 1 = q \cdot (p - 1) $$

Nu har vi, hvad vi skal bruge for at se, hvorfor det virker at $$(x^c)^d \equiv x \mod p$$:

$$ (x^c)^d \equiv x^{(c \cdot d)} \equiv x \cdot x^{(c \cdot d - 1)} \equiv x \cdot x^{q \cdot (p - 1)} \equiv x \cdot (x^{p - 1})^q \mod p $$

Her kan vi bruge Fermats lille sætning, der fortalte os at $$x^{p - 1} \equiv 1 \mod p$$, så vi får

$$ x \cdot (x^{p - 1})^q \equiv x \cdot (1)^q \equiv x \cdot 1 \equiv x \mod p $$

Det beviser, at $$(x^c)^d \equiv x \mod p$$, og derfor virker det at opløfte $$x^c \mod p$$ i $$c$$s invers modulo $$p - 1$$.

**Bonus info:** Du har nu også lært på et ret teknisk og matematisk plan, hvordan RSA fungerer!

Her vælges to primtal $$p$$ og $$q$$, og man finder $$n = p \cdot q$$. Herudover vælges et tal $$e$$, som sammen med $$n$$ udgør ens public key. Beskeden $$m$$ krypteres med $$c = m^e \mod n$$.

Vi har nu lært, hvordan denne operation inverteres, så man kan dekryptere $$c$$: man skal finde $$e$$s invers modulo $$\phi(n)$$. Det er ens private key, som benævnes $$d$$, og det gælder altså så at

$$ c^d \equiv (m^e)^d \equiv m \mod n $$

Årsagen og beviset er det samme som før, og sikkerheden i RSA ligger i, at ingen andre end du kender $$\phi(n)$$. Det er svært at udregne for store $$n$$, men hvis $$n = p \cdot q$$ gælder at $$\phi(n) = (p - 1) \cdot (q - 1)$$, hvilket er nemt at udregne. Så ingen andre end du må heller kende $$p$$ og $$q$$.

#### Opsamling

Vi har nu lært, hvordan vi inverterer alle tre operationer. Vi har altså funktionen

$$ enc(e) = (e \cdot a + b)^c \mod p $$

og vi kan nu prøve at isolere $$e$$, så vi ved, hvad vi skal gøre ved $$enc(e)$$ (som vi kender) for at komme tilbage til $$e$$.

Vi starter med at invertere eksponentieringen. Det ved vi nu, vi kan gøre ved at opløfte begge sider i $$c$$s invers modulo $$p - 1$$:

$$ enc(e)^{(c^{-1} \mod{p - 1})} \equiv e \cdot a + b \mod p $$

Vi kan nu trække $$b$$ fra på begge sider:

$$ enc(e)^{(c^{-1} \mod{p - 1})} - b \equiv e \cdot a \mod p $$

og til sidst gange med $$a$$s modulære invers:

$$ (enc(e)^{(c^{-1} \mod{p - 1})} - b) \cdot a^{-1} \equiv e \mod p $$

Nu har vi inverteret funktionen! I Python kode svarer de tre steps til
```python
invert_c = pow(decryption, pow(c, -1, p - 1), p)
invert_b = invert_c - b
invert_a = invert_b * pow(a, -1, p)
decryption = invert_a % p
```
som vi kan plotte ind i vores dekrypteringsfunktion

### Konklusion

Vi har nu fundet ud af at invertere krypteringsfunktionen og skrevet kode til at bruteforce passwordet. Vores endelige script til dekryptering er
```python
import random

p = 97953958723054470944201407781333999671402425802271290596631886639255617548503

def decrypt(ciphertext, pw):
    random.seed(pw)

    randints = [random.randint(2, 2**255) for _ in range(3 * 128)]
    
    decryption = ciphertext
    for _ in range(128):
        c = randints.pop()
        if c % 2 == 0:
            c -= 1
        b = randints.pop()
        a = randints.pop()

        invert_c = pow(decryption, pow(c, -1, p - 1), p)
        invert_b = invert_c - b
        invert_a = invert_b * pow(a, -1, p)
        decryption = invert_a % p
    
    return decryption

if __name__ == "__main__":
    ciphertext = 69494773765711558796303044899201719046500256450239245029456014825686379192778

    for i in range(10000):
        pw = str(i).zfill(4)
        decrypted = decrypt(ciphertext, pw)
        plaintext = int.to_bytes(decrypted, (decrypted.bit_length() + 7) // 8, 'big')
        
        if plaintext.startswith(b"DDC"):
            print(f"Password: {pw}")
            print(f"Flag: {plaintext.decode()}")
            break
```
Kører vi det, finder vi efter lidt tid passwordet `0403`, og vi kan dekryptere flaget: