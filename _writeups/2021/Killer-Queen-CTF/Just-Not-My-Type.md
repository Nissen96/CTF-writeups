---
layout: writeup
title: Just Not My Type
ctf: Killer Queen CTF
points: 153
solves: 440
tags: 
    - web
date: 2021-11-01
description: |-
    I really don't think we're compatible.
flag: flag{no_way!_i_took_the_flag_out_of_the_source_before_giving_it_to_you_how_is_this_possible}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

We get a link to a website with a simple password form.
We also get the source code of the website:
```php
<h1>I just don't think we're compatible</h1>

<?php
$FLAG = "shhhh you don't get to see this locally";

if ($_SERVER['REQUEST_METHOD'] === "POST") 
{
    $password = $_POST["password"];
    if (strcasecmp($password, $FLAG) == 0) 
    {
        echo $FLAG;
    } 
    else 
    {
        echo "That's the wrong password!";
    }
}
?>

<form method="POST">
    Password
    <input type="password" name="password">
    <input type="submit">
</form>
```

To ever get the flag we clearly need to send a POST request with a `password` field. We want the result of `strcasesmp($password, $FLAG)` to be true. Let's examine what `strcasecmp` does.

The function takes in two strings and compares them in a case-insensitive way. If the strings match, a 0 is returned - else a negative or positive values is returned, depending on whether string1 is less than or greater than string2.

Based on the title and the "I just don't think we're compatible", we are definitely looking at exploiting some of PHP's type juggling. If we can somehow pass something in with the wrong type, then PHP will likely just produce a warning and give no output - and since the comparison is done with `==` and not `===`, then `no output == 0` will like evaluate to `true`.

What can we pass in that would be incompatible? In a HTTP request handled by PHP, we can always pass in an empty array by using `password[]=`.

Doing that in this case works - we get a warning followed by the flag.

This was btw patched in later PHP versions.