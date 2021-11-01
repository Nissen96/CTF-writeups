---
layout: writeup
title: Cloudsourcing
ctf: Killer Queen CTF
points: 196
solves: 228
tags: 
    - crypto
date: 2021-11-01
description: |-
    Sourced in the cloud.
flag: kqctf{y0uv3_6r4du473d_fr0m_r54_m1ddl3_5ch00l_abe7e79e244a9686efc0}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

We are given an RSA public key and a base64 ciphertext. We can start by reading the public key, either with an online tool or locally with

<pre 
    class="command-line" 
    data-prompt="kali@kali $" 
    data-output="2-22"
><code class="language-bash">openssl rsa -text -in key.pub -pubin
RSA Public-Key: (2048 bit)
Modulus:
    00:cd:37:fb:dd:54:2b:82:c8:e1:e5:a4:69:70:4d:
    70:6a:ca:44:3b:90:78:f1:98:23:21:f6:72:96:80:
    b3:47:97:02:d9:17:35:7b:e6:30:bc:8f:f6:84:d3:
    ee:6a:07:8b:82:68:ce:aa:4e:85:2c:ed:dd:c5:ad:
    a4:7a:6c:c7:d8:40:46:fa:7e:d1:1e:5c:48:7b:8c:
    fa:86:86:d7:0a:45:cc:e1:27:78:3b:b3:6f:1e:59:
    1e:6d:ee:54:2e:83:af:a4:9c:6c:e5:fe:cb:07:8c:
    cd:7d:f9:78:f4:c2:d5:46:61:89:39:62:37:dc:b5:
    4f:8b:ce:95:42:0e:77:53:99:d5:09:44:e7:76:6a:
    96:26:c9:e3:7f:4e:9a:78:d2:5b:d2:1b:45:03:5a:
    32:ed:e0:3d:19:a6:8d:c8:16:42:ee:b7:9c:53:ea:
    63:e4:22:66:9e:58:ad:c5:a4:9a:2c:b4:da:86:2e:
    e6:95:6f:76:8f:82:c3:9c:39:c8:38:38:44:b7:1a:
    a6:58:0d:ec:30:ba:0c:18:6c:25:bd:ed:7e:71:77:
    78:fa:bd:68:be:19:01:5a:69:01:47:9f:e5:a7:fa:
    76:29:02:ec:a5:eb:79:1f:30:d9:80:09:6f:43:30:
    34:0b:0d:aa:e8:1d:a6:b7:7d:e1:81:56:fb:25:f4:
    fc:59
Exponent: 65537 (0x10001)</code>
</pre>

This is seemingly secure, as we are dealing with a public key of 2048 bits, likely generated from two primes of 1024 bits each. If that is the case, we cannot factor it manually.

But! Many very large primes are stored with their factorization in the factordb database, and this is likely what the title refers to. We can try converting the modulus to a number ourselves and looking it up, but I already have downloaded the tool `RsaCtfTool` from here:
https://github.com/Ganapati/RsaCtfTool
which can do all the work for us

We run this with
<pre 
    class="command-line" 
    data-prompt="kali@kali $" 
    data-output=""
><code class="language-bash">./RsaCtfTool --publickey key.pub --private</code>
</pre>

which tries to extract a private key from a given public key using different methods. One of these is looking it up in factordb, which works, and we get the private key:

```
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAzTf73VQrgsjh5aRpcE1waspEO5B48ZgjIfZyloCzR5cC2Rc1
e+YwvI/2hNPuageLgmjOqk6FLO3dxa2kemzH2EBG+n7RHlxIe4z6hobXCkXM4Sd4
O7NvHlkebe5ULoOvpJxs5f7LB4zNffl49MLVRmGJOWI33LVPi86VQg53U5nVCUTn
dmqWJsnjf06aeNJb0htFA1oy7eA9GaaNyBZC7recU+pj5CJmnlitxaSaLLTahi7m
lW92j4LDnDnIODhEtxqmWA3sMLoMGGwlve1+cXd4+r1ovhkBWmkBR5/lp/p2KQLs
pet5HzDZgAlvQzA0Cw2q6B2mt33hgVb7JfT8WQIDAQABAoIBADrihoWyoi2L4K3Z
KFwODGTIFx4UTW/dXK9hHO4sjcTMAwgxzan4miFxGaZxfWa1NYW89xgNIc+LjWgs
dBag4hMeFn/IJc8VYcL55+T0Cf4rmyc8ARb4XLkTj1Sx3zvdk2ejbufr3WwULd6o
19k7kqD4Wby6fxb4e5O9OjzTE9BLvr1NpHN1QRUupSUX3kv/mhtO3gQrRrkAT1L2
Ais+piqHmSrtX6YAnjood9oW2qy6oyBWvA11ipY9ZqfpI2G5Qc9WtViH/Erz2/3S
wFf0J9pgn+iAPbhcGwVh6U/cF+BcQZGse9GaY5Us4SJaQmM0ZdKiYbhKTRGBkudH
60sqeDUCgYEA0mwnrjcDpoc5Kv7qMB4AQCwP6LKnaG5q8Tc86JzYaPEnfUzl4trO
TruiSXmsok8RM/OLdAiIYiazz3GWgxFVNGtv+cEk4AKQnu2iRg5kP4wKBzqhYCnT
gMMMnt2UQfUrPOX7WDHaqQaOxkF06GJeHY7/RMswdOlXWx3w4oo2LJMCgYEA+atH
z0eS+0wzV4lubfpNl/6gi6KJxnpoPJtDt2vJBAa24fbS6ox9bx+Riki/CkpWiGDs
mb2ha1j5580kzDLfJjt1rncCd1iJy+S8zXmX0I1lkmhCnGKjsDDP4nqGmWoHyc9U
HxBYPWd2RtKNcBVDLImxr9IGe74GArU0Q2TmcuMCgYAvtwDEe4sjXvRysH1QTe1G
n/c3kBNwFeHAMwNnx/E20sBepGpYp78ykU+6k5G2+HDxM9/CfxDWGOqbNqmnrO2C
Rn6MxuRiu5Ipx78NXcQTuOCpRP1E/hcM0q3w9FPjJQIZ/BijpiJsQ6VqhXtKGsw2
ra9q3Rxu1l7NtZti825XawKBgHMG2LTE8xDYUKc56Ci/M1SduXXb0sIgzzltB0vQ
WvKB7Ww5/X6Wb4vs7W7aiTnCeg+nKBrE5UPB4JFNUHDL10eUCWnx5q75mbLYlavN
I4awPmWvp1DJmUSpmH1tmenAkgoGfWk6bI0Nx85lX0iOYz53yeeJSfdk2vwQZB3Q
tOOlAoGBAM83orP3tq+o57yvX/v36APtNW7ja7fMnSnmZRuWyJDqCJMNvGRlGObt
hfLludqNeJ4BSJ1nZNqbIvukk8J7DDukrGE5WxP+L1UmuIcTLgOeW7heMEUFbuVG
SpUX47+QBmx6Q8mHa97x/sGidZMlOEBG38bhvfdMgX0pW8zO+Oll
-----END RSA PRIVATE KEY-----
```

This is all we need to decrypt the ciphertext. We can again either use an online tool, or we can base64 decode the ciphertext and decrypt it with `openssl` again:

<pre 
    class="command-line" 
    data-prompt="kali@kali $" 
    data-output=""
><code class="language-bash">base64 -d mystery.b64 > mystery.txt
openssl rsautl -decrypt -inkey key.private -in mystery.txt</code>
</pre>
which gives us the flag.