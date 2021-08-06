---
layout: writeup
title: Power Snacks
ctf: >-
    Hacky Holidays - SPACE RACE
points: 115
solves: 44
tags: 
    - ppc
    - misc
date: 2021-08-04
description: |-
    Are you the very best PowerShell user? Try this challenge to get better acquainted with PowerShell's functionality. You need to come up with commands that result in a specific output. You can check your output by piping the result to the "Check" function. Example:
    ```
    Get-Content words | dosomething | Check
    ```

    ### 42 [25 points]
    Write a script that writes out all numbers (1 per line) from 1 to 1337, inclusive. However, if the number is divisible by 42, instead, print the string "Life, the universe, and everything". Example excerpt given below:
    ```
    ..
    40
    41
    Life, the universe, and everything
    43
    ..
    ```

    ### Scrabble [30 points]
    You're playing scrabble with your friends. You have the letters "iydhlao". Which are the words you can form? First sort them by increasing size, then alphabetically. Only include words of two letters and more. Make use of the dictionary file "dictionary" in /workdir. Example excerpt given below for different letters:
    ```
    ..
    pad
    pea
    aped
    deaf
    ..
    ```

    ### TSV [30 points]
    In the tab-separated file "passwords.tsv" you get an overview of often-used passwords. Can you give us an overview of the number of passwords per category? Sort the result by descending count. Example excerpt given below:
    ```
    Name     Count
    ----     -----
    ..          ..
    nerdy       30
    animal      19
    ..          .. 
    ```

    ### Names [30 points]
    Given the passwords file, supply a list of passwords from the 'names' category ordered first by ascending password length, then alphabetically. Example excerpt given below:
    ```
    ..
    scott
    steve
    albert
    alexis
    ..
    ```
---
