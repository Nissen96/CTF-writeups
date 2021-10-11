#!/usr/bin/env python3

import json
from copy import deepcopy
from functools import reduce

def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]

def xor_list(ls):
    return reduce(lambda i, j: i ^ j, ls)


def recover_keystream(key, public):
    st = set(key)
    keystream = []
    for v0, v1 in public:
        if v0 in st:
            keystream.append(0)
        elif v1 in st:
            keystream.append(1)
        else:
            assert False, "Failed to recover the keystream"
    return keystream


def bytes_to_bits(inp):
    res = []
    for v in inp:
        res.extend(list(map(int, format(v, '08b'))))
    return res


def bits_to_bytes(inp):
    res = []
    for i in range(0, len(inp), 8):
        res.append(int(''.join(map(str, inp[i:i+8])), 2))
    return bytes(res)


with open("output.txt") as fin:
    enc, public = fin.read().split("\n")[:-1]
enc = bytes_to_bits(bytes.fromhex(enc))
public = json.loads(public)

ln = len(enc)
pb = deepcopy(public)

key = []
k = 0
for i in range(ln):
    for pos, (a, b) in enumerate(pb):
        if a == k:
            key.append(b)
            break
        elif b == k:
            key.append(a)
            break
    del pb[pos]
    k = xor_list(key[-ln // 3:])

keystream = recover_keystream(key, public)
flag = bits_to_bytes(xor(enc, keystream))
print(flag.decode())
