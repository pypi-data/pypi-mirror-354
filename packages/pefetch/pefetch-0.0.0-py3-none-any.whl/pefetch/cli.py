import argparse
import random
import urllib.request
import urllib.error
from html.parser import HTMLParser


class Stripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.current_href = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.current_href = "https://projecteuler.net/" + href.lstrip("/")

    def handle_endtag(self, tag):
        if tag == "a" and self.current_href:
            self.current_href = None

    def handle_data(self, data):
        if self.current_href:
            self.result.append(f"{data} [\u001b[34;1m{self.current_href}\u001b[0m]")
        else:
            self.result.append(data)

    def get_text(self):
        return "".join(self.result)


def strip_html(html):
    parser = Stripper()
    parser.feed(html)
    return parser.get_text()


def latexizer(string):
    string = string.replace("$$", "$")
    OPENING_DLLR = True
    result = []
    for char in string:
        if char == "$":
            if OPENING_DLLR:
                result.append("\u001b[37;1m")
            else:
                result.append("\u001b[0m")
            OPENING_DLLR = not OPENING_DLLR
        else:
            result.append(char)

    string = "".join(result)
    string = string.replace("\\dots", "...")
    string = string.replace("\\cdots", "...")
    string = string.replace("\\times", "*")

    string = string.replace("\\lt", "<")
    string = string.replace("\\le", "≤")
    string = string.replace("\\gt", ">")
    string = string.replace("\\ge", "≥")

    string = string.replace("\\to", "→")
    string = string.replace("\\ne", "≠")
    return string


def format_content(content, number):
    result = f"\033[1m\u001b[36;1mProject Euler Problem {number}\n\u001b[0m"
    content = content.strip()
    content = strip_html(content)
    content = latexizer(content)
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
            f"\n\u001b[34;1mhttps://projecteuler.net/problem={args.problem}\n\u001b[0m"
        )
