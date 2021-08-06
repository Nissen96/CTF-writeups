---
layout: writeup
title: Quantum Snacks
ctf: >-
    Hacky Holidays - SPACE RACE
points: 150
solves: 274
tags: 
    - quantum
date: 2021-08-04
description: |-
    Computers speak the language of binary (zeros and ones), and every computer program is basically just applying logic gates (e.g NOT, OR, AND, XOR etc) to these bit to get a desired outcome. The important point here is to remember that a bit is a single variable that can have one of 2 values, either zero or one).

    Quantum computers speak a very different language. Instead of a bit we have a qubit (quantum bit), which can be represented as a two-dimensional vector. Classical bit 0 is equivalent to the qubit `(1  0)`, and the classical bit 1 is equivalent to the qubit `(0  1)`, but there are many other qubit states that do not have a classical equivalence, which means that qubits can store much more information than classical bits. The goal of this challenge is to understand this concept better.

    To change the state of a (q)bit we apply logic gates to it. In quantum computing logic gates are represented as matrices, and the outcome of this operation can be calculated by multiplying the logic gate (a matrix) with the initial qubit state (a vector). Mathematically it looks like this:
    ```
    (a  b)(x)   (ax + by)
    (c  d)(y) = (cx + dy)
    ```
    In this challenge we limit ourselves to three 1-qubit logic gates:
    ```
    X = (0  1)      Z = (1  0)     H = 1/sqrt(2) (1  1)
        (1  0)          (0 -1)                   (1 -1)
    ```
    Note: in practice there are more logic gates that result in an infinite possible quantum states. Because we are only considering 3 specific logic gates then the number of states is finite.

    ### How many states? [50 points]
    Considering only these 3 logic gates, and starting in the `(1  0)` state, how many states can the qubit have?
    
    Hint: Start applying the logic gates in random order. Drawing the result in x-y coordinates will greatly help you understand the result.

    ### Make a circuit [50 points]
    Provide a circuit (a series of operations) that transforms the state `(1  0)` to the state `(-1 0)`, only using the `H` and `X` operations. A possible (wrong) answer is `HHXHXHXH`.

    ### Short circuit [50 points]
    Same as question 2 but now provide the shortest circuit possible (minimal number of gates). You are allowed to use `H`, `X`, and `Z`.
---
