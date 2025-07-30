import argparse
import random
import urllib.request
import urllib.error

from . import latex
from . import html


def format_content(content, number):
    result = f"\u001b[36;1m{html.problem_title(number)}\n\u001b[0m"
    result += f"\u001b[36;2mProblem {number}\u001b[0m\n\n"
    content = content.strip()
    content = html.strip_html(content)
    content = latex.latexizer(content)
    result += content
    return result


def fetch_problem(number):
    url = f"https://projecteuler.net/minimal={number}"
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode("utf-8")
            print(format_content(content, number))
    except urllib.error.HTTPError as e:
        print(f"Error: Could not fetch problem {number} (HTTP {e.code})")
    except urllib.error.URLError as e:
        print(f"Error: Failed to reach server: {e.reason}")


def main():
    parser = argparse.ArgumentParser(
        prog="pefetch",
        description="Project Euler Problem Fetcher",
        epilog="For more information see \u001b[34;1mhttps://github.com/StanFromIreland/pefetch\u001b[0m",
    )
    parser.add_argument("problem_number", help="problem number, type r for random")
    parser.add_argument(
        "--link", "-l", help="print link to problem", action="store_true"
    )
    args = parser.parse_args()

    if args.problem_number == "r":
        args.problem_number = random.randint(1, 950)

    fetch_problem(args.problem_number)

    if args.link:
        print(
            f"\n\u001b[34;1mhttps://projecteuler.net/problem={args.problem_number}\n\u001b[0m"
        )
