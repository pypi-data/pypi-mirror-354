Project Euler Fetch (*pefetch*)
===============================

A CLI utility for accessing [Project Euler](https://projecteuler.net) problems
from your terminal. Currently, in development, trying to somehow render LATEX,
with no dependencies!

## Installation

```
pip install pefetch
```

## Usage

```
usage: pefetch [-h] [--link] problem_number

Project Euler Problem Fetcher

positional arguments:
  problem_number  problem number, type r for random

options:
  -h, --help      show this help message and exit
  --link, -l      print link to problem
```

As an example, problem 1:

```
$ pefetch 1
Multiples of 3 or 5
Problem 1

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
Find the sum of all the multiples of 3 or 5 below 1000.

```

![](example.png)

## Contributing

There are a lot of issues, performance (~1 second due to the 2 requests), rendering,
colors in non-dark terminals, images etc.
Feel free to contribute if you feel like it.
