#!/usr/bin/env python3
import base64
from Crypto.Util.Padding import pad, unpad
from pwn import xor

def text_to_blocks(text):
    return [text[i:i+16] for i in range(0,len(text),16)]


plain = pad(b"CryptogangFTW", 16)
L, R = plain[:8], plain[8:]

cipher = base64.b64decode("Z0htZlMgBi56am5tbnN7bA==")
S, T = cipher[:8], cipher[8:]

C1 = xor(S, L, R)
C2 = xor(T, L)

with open("encrypted-conversation.txt", "r") as f:
    messages = f.read().split("\n")[:-1]

for message in messages:
    person, encoded_cipher = message.split("> ")
    decrypted = b""
    for block in text_to_blocks(base64.b64decode(encoded_cipher)):
        left = xor(block[8:], C2)
        right = xor(block[:8], C1, left)
        decrypted += left + right
    print(f"{person}> {unpad(decrypted, 16).decode()}")
