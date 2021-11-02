---
layout: writeup
title: She's A Killed Queen
ctf: Killer Queen CTF
points: 290
solves: 86
tags: 
    - forensics
date: 2021-11-01
description: |-
    My picture has been corrupted. Can you fix it?

    [queen.png](/assets/CTFs/2021/Killer-Queen-CTF/queen.png)
flag: kqctf{SHES_A_KILLED_QUEEN_BY_THE_GUILLOTINE_RANDOMCHRSIADHFKILIHASDKFHQIFPXKRL}
---
<details>
    <summary>tl;dr</summary>
    Image has width and height 0. Bruteforce widths and heights until IHDR CRC is correct. Open image in <code>stegsolve</code> and find hidden code in LSB plane. Code is Mary Stuart Code - decode to get flag.
</details>

***

## Corrupted PNG

We are given a PNG image that is corrupted in some way.

### Problem Detection

We can detect *how* it is corrupted in quite a few ways:

#### Exiftool

We start by inspecting the metadata with `exiftool`:
<pre 
    class="command-line"
    data-user="kali"
    data-host="kali"
    data-output="2-22"
><code class="language-bash">exiftool queen.png
ExifTool Version Number         : 12.32
File Name                       : queen.png
Directory                       : .
File Size                       : 2.0 MiB
File Modification Date/Time     : 2021:11:01 17:57:01-04:00
File Access Date/Time           : 2021:11:01 17:57:02-04:00
File Inode Change Date/Time     : 2021:11:01 17:57:01-04:00
File Permissions                : -rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 0
Image Height                    : 0
Bit Depth                       : 8
Color Type                      : RGB with Alpha
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
SRGB Rendering                  : Perceptual
Image Size                      : 0x0
Megapixels                      : 0.000000</code>
</pre>
We see the image has a width and height of 0 -- this is certainly a problem and likely the issue.

#### pngcheck

A more specific tool to PNGs is `pngcheck`:
<pre 
    class="command-line"
    data-user="kali"
    data-host="kali"
    data-output="2-3"
><code class="language-bash">pngcheck queen.png
queen.png  invalid IHDR image dimensions (0x0)
ERROR: queen.png</code>
</pre>
This shows the same header issue.

#### PCRT

Another great tool for checking and repairing PNGs is [PCRT](https://github.com/sherlly/PCRT). We can try this out as well:
<pre 
    class="command-line"
    data-user="kali"
    data-host="kali"
    data-output="2-18"
><code class="language-bash">python2 ~/tools/PCRT/PCRT.py -i queen.png

         ____   ____ ____ _____ 
        |  _ \ / ___|  _ \_   _|
        | |_) | |   | |_) || |  
        |  __/| |___|  _ < | |  
        |_|    \____|_| \_\|_|  

        PNG Check & Repair Tool 

Project address: https://github.com/sherlly/PCRT
Author: sherlly
Version: 1.1

[Finished] Correct PNG header
[Detected] Error IHDR CRC found! (offset: 0x1D)
chunk crc: 0DB3F6C0
correct crc: 3B8B7C12</code>
</pre>
We again see there is an issue with the IHDR. The CRC in the header does not match the header contents. PCRT doesn't detect an issue with the header itself (it even says "Correct PNG header") but thinks the issue is just in the CRC, and can correct this. But we know there is an issue with the width and height, so the problem likely isn't with the CRC, but with those fields. Instead of fixing the CRC based on the contents, we should likely fix the contents based on the CRC in this case.

#### Manual Detection

The final and most general method I want to mention is a manual detection based on the PNG specification. We start by reviewing how the PNG IHDR should actually be formatted at [PNG Specification](http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html):
```
The IHDR chunk must appear FIRST. It contains:

   Width:              4 bytes
   Height:             4 bytes
   Bit depth:          1 byte
   Color type:         1 byte
   Compression method: 1 byte
   Filter method:      1 byte
   Interlace method:   1 byte
```
Let's check the actual IHDR. We can use `xdd queen.png | less`, or we can use [bgrep](https://github.com/rsharo/bgrep) to match "IHDR" plus the next 17 bytes (header data + CRC):
<pre 
    class="command-line"
    data-user="kali"
    data-host="kali"
    data-output="2-3"
><code class="language-bash">bgrep '"IHDR"??*17' queen.png 
000000c: 4948 4452 0000 0000 0000 0000 0806 0000  IHDR............
000001c: 000d b3f6 c0                             .....</code>
</pre>
Parsing this according to the specs, the fields in the header contain:
```
Width:              00 00 00 00 = 0 px
Height:             00 00 00 00 = 0 px
Bit depth:                   08 = 8 bits per sample
Color type:                  06 = 6 (RGBA)
Compression method:          00 = 0 (deflate/inflate)
Filter method:               00 = 0 (adaptive filtering)
Interlace method:            00 = 0 (no interlace)
CRC:                0D B3 F6 C0
```
So manually, we also found the image have a width and height of 0, which is wrong. This is a bit more tedious but can be necessary for files with no good automated tools or if the file is corrupted in a way where the tools can no longer detect the file type.

### PNG Correction

We now know the issue (or at least one issue) that we want to fix: finding the correct image width and height. There are again multiple ways of fixing this issue:

#### Bruteforce

Assuming the CRC is not corrupted too, we can use this to restore the image and height through bruteforce. We simply try all possibilities within a sensible range and check whether the corresponding CRC matches the one in the file (0x0DB3F6C0).

We write a script that:

1. runs through various widths and heights
2. creates an IHDR based on these
3. computes the CRC of the IHDR

When the CRC matches, we likely have the correct width and height. The image likely isn't very large, so we can just try values up to e.g. 2000:
```python
import binascii

for w in range(1500):
    for h in range(1500):
        width = w.to_bytes(4, byteorder='big')
        height = h.to_bytes(4, byteorder='big')
        ihdr = b"\x49\x48\x44\x52" + width + height + b"\x08\x06\x00\x00\x00"
        if binascii.crc32(ihdr) == 0x0DB3F6C0:
            print(width, height)
```
We quickly get the output `b'\x00\x00\x04\xb0' b'\x00\x00\x02\xa3'` (so 1200x675) and we can insert those as the width and height in the image using a hex editor such as `hexedit`:

![Queen Hexedit]({{ site.baseurl }}/assets/CTFs/2021/Killer-Queen-CTF/queen-hexedit.png)

The image is now fixed and can be opened.

#### Analysis

Instead of bruteforcing the possible widths and heights, we can do a more precise analysis. This method isn't based on the IHDR CRC and would work even if that was corrupted as well.

In a PNG image, the actual data is compressed and split in chunks, each of type IDAT. If we can extract all the data from the IDAT chunks and decompress, then we can factor the resulting size to figure out all possible dimension combinations.

This [blog post](https://pyokagan.name/blog/2019-10-14-png/) has a great explanation of how to do all this. Below is a slightly trimmed down version of their script to get the total data size:
```python
import zlib
import struct

def read_chunk(f):
    chunk_length, chunk_type = struct.unpack(">I4s", f.read(8))
    chunk_data = f.read(chunk_length)
    f.read(4)  # Discard CRC
    return chunk_type, chunk_data

with open("queen.png", "rb") as f:
    signature = b"\x89PNG\r\n\x1a\n"
    f.read(len(signature))

    # Extract IDAT chunks
    chunks = []
    while True:
        chunk_type, chunk_data = read_chunk(f)
        chunks.append((chunk_type, chunk_data))
        if chunk_type == b"IEND":
            break

# Combine and decompress IDAT chunks
IDAT_data = b"".join(
    chunk_data for chunk_type, chunk_data in chunks if chunk_type == b"IDAT"
)
IDAT_data = zlib.decompress(IDAT_data)
print(f"Data bytes: {len(IDAT_data)}")
```
The script just extracts the data from all IDAT chunks, concatenates them, and decompresses the result. Running this, we get the output
```
Data bytes: 3240675
```
Factoring this results in $$3240675 = 3 \cdot 3 \cdot 3 \cdot 5 \cdot 5 \cdot 4801$$. We previously saw the color type byte was set to 6, which means the samples are RGB values with an alpha channel. We also saw the bit depth was 8, so each color value is a single byte. This means every pixel is 4 bytes large. So the size we found should be $$(width \cdot 4) \cdot height$$ right? Almost! If we look in chapter [2.3. Image Layout](http://www.libpng.org/pub/png/spec/1.2/PNG-DataRep.html#DR.Image-layout) in the specs, we see in the last line:

> An additional "filter-type" byte is added to the beginning of every scanline (see Filtering). The filter-type byte is not considered part of the image data, but it is included in the datastream sent to the compression step. 

A *scanline* is just what the spec calls each row. So really, the total size is $$3240675 = (1 + width \cdot 4) \cdot height$$. Looking back at the factors, we now must take a guess on which factors makes up the $$height$$, and which makes up $$1 + width \cdot 4$$. A good guess in this case would probably be $$1 + width \cdot 4 = 4801$$, meaning $$width = \frac{4801 - 1}{4} = 1200$$. This seems like a sensible width. The height is then the remaining product: $$height = 3 \cdot 3 \cdot 3 \cdot 5 \cdot 5 = 675$$. Trying this out, we see the CRC now matches and the image can be opened.

If it was NOT correct, then we would have to try other combinations of factors, e.g. $$(1 + width \cdot 4) = 5 \cdot 4801$$ resulting in a width of 6001 and heigh of 135. The possible combinations can also quickly be bruteforced with a small script. But 1200x675 seems reasonable and was also correct.

## Steganography

We can now open the image, which we see is a painting of a queen -- unsurprisingly:
![Queen](https://i.imgur.com/rW91umj.png)
There is no immediate flag here, so we aren't done yet, there must be some data hiding in the image. The easy way to check this is to open the image with `stegsolve` and look through the different channels and planes. In all three RGB channels we find another image hidden in the least significant bit plane:
![LSB Plane in stegsolve](https://imgur.com/7YOlrp4.png)
This seems like some symbol substitution cipher:
![Cipher](https://imgur.com/HCiWjPf.png)

## Cipher

Googling a bit for "symbol ciphers" it is possible to find the same symbols in some images. Since the challenge has been about a queen, it also wouldn't be a dumb idea to google "queen cipher" -- and doing so, the correct cipher comes up as the first result. It is called the "Mary Stuart Cipher", apparently invented and used by Mary Queen of Scots in the 1500s. It can be decoded with [this tool](https://www.dcode.fr/mary-stuart-code), resulting in the flag: