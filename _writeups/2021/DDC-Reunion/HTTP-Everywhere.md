---
layout: writeup
title: HTTP Everywhere
ctf: DDC Reunion
points: 20
solves: 
tags: 
    - forensics
    - network
date: 2021-10-04
description: |-
    Run `wget http://everywhere.hkn/trace.pcapng` to find a trace file with lots of unencrypted traffic.
    
    Can you increase this metric on localhost?
---
<details> 
    <summary>tl;dr</summary>
    Inspect SMTP packets to find an e-mail sharing a key pair to run HTTPS locally.
    Use the private key to decrypt HTTPS data sent over localhost.
    Flag is in the decrypted HTTP response data.
</details>

***

## Introduction

We start by downloading the [packet capture](/assets/CTFs/2021/DDC-Reunion/trace.pcapng) and open it in Wireshark to inspect the captured traffic:
![Wireshark overview](/assets/CTFs/2021/DDC-Reunion/wireshark-overview.png)

## Recon

The file contains many frames (3990) sent between a main client (172.21.78.63) and multiple other parties, using different protocols.

### Overview

To get an overview of the message types, we can inspect the protocol hierarchy under "Statistics -> Protocol Hierarchy":

![Wireshark protocols](/assets/CTFs/2021/DDC-Reunion/wireshark-protocols.png)

We see some UDP traffic, including standard DNS requests, but most packets have been sent with TCP and most of this is unencrypted HTTP data. We also see some SMTP traffic, used for e-mails, and some encrypted TLS packets. Both the HTTP and SMTP data seem interesting and we explore those further.

### HTTP

We start by applying the filter `http` to inspect the web requests:

![Wireshark HTTP data](/assets/CTFs/2021/DDC-Reunion/wireshark-http.png)

We see the client has visited many interesting websites, including docs on "SSL howto" and searches for "fair-trade ssl certificates", "does it actually matter if i use tls?", and "free ssl certificates online oh boy" (last search on search.disney.com :smile:). Clearly a very security-minded individual...

Following these requests, most of the rest are basically just meme sites and lots of requests for JPEGs, GIFs, MP4, etc. Some of these could potentially be interesting (and can be extracted under "File -> Export Objects -> HTTP..."), but seems to just be some bored guy browsing the internet. Instead, we continue the recon by checking the mail requests.

### SMTP

To inspect the mail traffic, we filter on `smtp`:

![Wireshark SMTP data](/assets/CTFs/2021/DDC-Reunion/wireshark-smtp.png)

We see a single email sent using SMTP, and we can right-click any of the packets and choose "Follow -> TCP Stream" to see the entire communication. Focusing on just the message itself, we have:

    From: Till S. Eksbert <tills@eksbert.com>
    To: Bob Allis <usdlxoropgytikkivl@ianvvn.com>
    Subject: There you go, EZPZ :-)
    Message-Id: <E1mFY0L-00004c-On@mail.man.com>
    Date: Mon, 16 Aug 2021 08:29:57 +0000

    Hey Bob,

    You can just use these keys to run HTTPS locally, no biggie:

    -----BEGIN CERTIFICATE-----
    MIIDbTCCAlWgAwIBAgIUSafSO6wmpOhCZdEJNzDAj9L+WB8wDQYJKoZIhvcNAQEL
    BQAwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
    GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAgFw0yMTA4MTUwNzAwNDFaGA8yMTIx
    MDcyMjA3MDA0MVowRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUx
    ITAfBgNVBAoMGEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDCCASIwDQYJKoZIhvcN
    AQEBBQADggEPADCCAQoCggEBAMas0MHwkMgg977ef20CI6QpyuKe3CyQu4VKtalk
    ZEF+fQnaG2VXqZSPfFQuGxinYJ1ANRdzfyfemmzDjvHU3tV9B2eTNZqYXGtoiig/
    OcWdPX6kFScYoYh9JasbKjl15U7OUqe1OtR2fmK5PbynQ2H8JquSDtTIRn2Wq3dU
    yxoArr7TB9VCi+v5Ocj9ZNvHiHgq9vbKiBtsJDBPLP08QoWQ4Qo6RFq8RTucmdhy
    /zKx4fnR3U19h7fi4zW28KyYzCsSuh4whBSeDNZq56WZ7ykgJmqMVMIKlNNDoigc
    wrW5r2ACSjw0jeanxzyVXHqKvioIrAuYbJqZOIQaZRIKmE8CAwEAAaNTMFEwHQYD
    VR0OBBYEFKyzXYUDAOUv9Nyvahha/EO5//skMB8GA1UdIwQYMBaAFKyzXYUDAOUv
    9Nyvahha/EO5//skMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEB
    ALZ/EjOkssUOXqI8pcyRI2ezTHPjzThBY0oWZ4OGmUrdMSzHDWXJXffbWFYAFtia
    7KT1n8dHiq1wF6MLxsxvLKLgMrkSsVyXwD37aSDJxWbNGCAXj/J/AjUiMYpBxxmQ
    L7JnxSzrQXBTNBJss4/p0Y213hQ5CiKDivO/44mTNiUOPoOAjA4tFbXgnT4n8eEM
    5CWo9wGpwr3i1sYbKd341Kmm2joAMpraz64Rjn4t6l8HqUrO4qLghZyrHX9insXa
    hZNoFdd6kCmOFOjkjRmY3tZ2cqOTd4ksqJT8bmqzn8q6zDAR8H1E0e18V/kV3bQd
    MPeT7b/yEZwOsV3Lq7KDL4A=
    -----END CERTIFICATE-----


    -----BEGIN PRIVATE KEY-----
    MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDGrNDB8JDIIPe+
    3n9tAiOkKcrintwskLuFSrWpZGRBfn0J2htlV6mUj3xULhsYp2CdQDUXc38n3pps
    w47x1N7VfQdnkzWamFxraIooPznFnT1+pBUnGKGIfSWrGyo5deVOzlKntTrUdn5i
    uT28p0Nh/Carkg7UyEZ9lqt3VMsaAK6+0wfVQovr+TnI/WTbx4h4Kvb2yogbbCQw
    Tyz9PEKFkOEKOkRavEU7nJnYcv8yseH50d1NfYe34uM1tvCsmMwrEroeMIQUngzW
    auelme8pICZqjFTCCpTTQ6IoHMK1ua9gAko8NI3mp8c8lVx6ir4qCKwLmGyamTiE
    GmUSCphPAgMBAAECggEBAJnIGq6Drw25twqe3rNZ/IyNbOWNYY99WCkMcyDy/EdV
    ySNfF+WRvUmo5uuh5Idox3fwwyer1rjdrVqS5Ip74yAM7zZU1CEd3iuld4s/pVA5
    LehgyZ7BigdEF2wiUsS3ZQ9i1MfLmAXs0ldIW2kzbwzhSG11WNWLUETV41My5yLw
    FmAu55P3s7YRltXJpzppcDkPyU5Ja7Qfbf9nSHhE604Y5V7enNo4TWKF9Rgoi30I
    zq68OnsgwUfyUgJ8Yff6bSVJrLKGuPkxN99ht8F81Ry40Qi6EaeVVb3bQDOdRxc4
    Mmc2G7o7k95sKqBZGqKZEYX7E7ZPJvcnLDEYqTPhC8ECgYEA8XpDY+07ubRsvmFK
    4rf97IBfFAKkoPHW5heA1afeTVVVXuWVFdYF6QRUS3to1scNB+cmBIIk9X3WdrWD
    adro8Xt9BjWaoUcQtCTFo+paJCKsH1HhQYKGKf6n++MjRT7q1dG1T0JoavdfT99b
    ghtD1rfWUhlt9DxWNPJmk17VcTsCgYEA0p+S3wl/snSQk0Sm2xl9QI1/FjIbCGaw
    zlpDVyJE3lznO+/mKYIP6F+37+bsLu7ASUKeZZNLBjZlmJpziNDRIqvBYB10rq7R
    XkMjjZiq3f4GoWQbs5kbtJMJ4BaPLS528478BPIrqqfnpgL5r8LGlJtvEAR6/G8l
    kNR+b33yA/0CgYEAk6Nh8oWIH6lNVzTa+TTvHhr6hpx7FR/nePRjw72H8BY9RPDv
    LtOU93u7Ig9I8Q/wSqWrm9QKTsHqTtf5ic3a4FHVBefeK77sWoelAuv0wuUkAV4p
    b8kiyCg3gozD8sFeCO7XgKckeknWT1pLc4fB+VSax8VecZY2StbtmirAKyMCgYBg
    PMuGH7f6WWqJ789xwzbI3R5ZjPFvKETXNMUaNi1TkQ2TBG2dP7F3Eu1fr5rxYuP3
    VXo8nU2lfAt16/Soagl1FxeXjD35ZyWBNZo0I7LHFj//VFeX+3h+TMUxX/1xvo5Z
    gVbEB8dOBcRBxZBC7/N+iXr4zaNIXpzCjWVsGhcQHQKBgQDMagp2As2KBSXreEgA
    uAMiEzzsGxbD5LPt6vNvhywD3Qkq5FE8M3m3I75NLIUOadmoNzYAmMwvqDEk54vF
    6p0zq8nMCVSIeC1OzHMBeTn19NfNsYE05S1Cc7rba2wAENLlaAsuKmuX3MMQYPrn
    8y1Aix4HDUGVPFakPrKXq31olQ==
    -----END PRIVATE KEY-----


    It just works. 

    Best regards,
    Till S. Eksbert

So apparently, the client is called Till S. Eksbert (which he obviously is - a TLS expert :smile:) and has sent a cleartext mail to Bob with a public and private key to run HTTPS locally. The private key can potentially allow us to decrypt some HTTPS data, so we copy it to a file.

### TLS

It is now time to look more into the encrypted HTTPS data, which we can't yet read. The challenge text mentions all the unencrypted data and asks us "Can you increase this metric on localhost?", so we are seemingly supposed to decrypt some encrypted data sent on localhost. We can find all encrypted TLS packets sent on localhost by applying the filter `tls && ip.addr == 127.0.0.1`. Here we find just a single TLS communication stream with the initial setup and handshake, followed by a few packets of application data:

![Wireshark TLS Stream](/assets/CTFs/2021/DDC-Reunion/wireshark-tls.png)

## Exploit

We have now done all the necessary recon work and are ready to combine it all. We have found a private certificate in a mail, which was meant for running HTTPS locally, and we have found an encrypted TLS stream on localhost. This stream has likely been encrypted with the public key sent in the e-mail, and we can try decrypting it with the corresponding private key.

Wireshark handles this decryption for us if we provide the key file. We do this under "Edit -> Preferences -> RSA Keys -> Add new keyfile...", where we upload the private key we saved earlier:

![Wireshark RSA Key Upload](/assets/CTFs/2021/DDC-Reunion/wireshark-key.png)

Now click "OK" and click "Reload this file" in the top bar to update the file. Wireshark will try to use the key file to decrypt all TLS traffic and will automatically show the decrypted packets if it succeeds. Looking at the previously encrypted localhost data, we see Wireshark has successfully decrypted the data for us:

![Wireshark Decrypted Data](/assets/CTFs/2021/DDC-Reunion/wireshark-decrypted.png)

We can now see the traffic was actually HTTPS, and we can inspect the underlying HTTP data. This is simply a request to `/`, followed by a `200 OK` response with the following data `text/html` data:

![Wireshark HTTP response](/assets/CTFs/2021/DDC-Reunion/wireshark-https.png)

We got our flag!

    HKN{fj2-pS-KIo7Z}