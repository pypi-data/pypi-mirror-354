import urllib.request
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


class geth2content(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_h2 = False
        self.h2_content = ""

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.in_h2 = True

    def handle_endtag(self, tag):
        if tag == "h2":
            self.in_h2 = False

    def handle_data(self, data):
        if self.in_h2:
            self.h2_content += data


def problem_title(number):
    with urllib.request.urlopen(
        f"https://projecteuler.net/problem={number}"
    ) as response:
        html = response.read().decode("utf-8")

    parsr = geth2content()
    parsr.feed(html)

    return parsr.h2_content.strip()
