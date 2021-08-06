---
layout: writeup
title: >-
    How far can you go in a cloud?
ctf: >-
    Hacky Holidays - SPACE RACE
points: 150
solves: 34
tags: 
    - cloud
    - aws
date: 2021-08-04
description: |-
    You have found a mysterious terminal in [this site that](http://flask-balancer-244a173-538fc99c60644733.elb.eu-west-1.amazonaws.com/) can convert HTML into PDFs. It seems to be hosted on a space cluster. Can you traverse through it and find all its secrets?

    ### Meta request forgery [75 points]
    We use all the newest cloud features. Have you tried ECS on AWS? Your mission is to find out the cluster ARN. Flag format: "arn:aws:ecs:...."

    ### Never modify a container directly [25 points]
    One of the developers of the application decided to use bash and load some interesting environment variables whenever bash starts. Can you find them?

    ### Role adventures [50 points]
    Task metadata can be very useful, using the information found in the previous challenge can you figure out a way to obtain the name of the private s3 bucket?
---
