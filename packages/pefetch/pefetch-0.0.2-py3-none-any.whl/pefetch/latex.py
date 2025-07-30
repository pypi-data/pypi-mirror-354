import re

SUPERSCRIPT_MAP = str.maketrans(
    "0123456789+-=()qwertyuiopasdfghjklzxcvbnm",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾qʷᵉʳᵗʸᵘᶦᵒᵖᵃˢᵈᶠᵍʰʲᵏˡᶻˣᶜᵛᵇⁿᵐ",
)
SUBSCRIPT_MAP = str.maketrans("0123456789+-=()nxuiophjkl", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₙₓᵤᵢₒₚₕⱼₖₗ")

URL_PATTERN = re.compile(r"https?://[^\s\]\)]+|www\.[^\s\]\)]+", re.IGNORECASE)


def latexizer(string):
    # Pull URLs so we dont mess them up as subscript
    url_placeholders = []

    def _url_replacer(match):
        url_placeholders.append(match.group(0))
        return f"<<URL{len(url_placeholders) - 1}>>"

    string = URL_PATTERN.sub(_url_replacer, string)

    # Highlighting
    string = string.replace("$$", "$")
    OPENING_DLLR = True
    result = []
    for char in string:
        if char == "$":
            result.append("\u001b[37;1m" if OPENING_DLLR else "\u001b[0m")
            OPENING_DLLR = not OPENING_DLLR
        else:
            result.append(char)
    string = "".join(result)

    # Step 3: Symbol replacements
    replacements = {
        "\\dots": "...",
        "\\cdots": "...",
        "\\}": "}",
        "\\{": "{",
        "\\,": ",",
        "\\%": "%",
        "&\\colon": ":",
        "\\displaystyle": "",
        "\\begin{align}": "",
        "\\end{align}": "",
        "\\\\": "",
        "&=": "=",
        "\\times": "*",
        "\\cdot": "•",
        "\\sum": "Σ",
        "\\bmod": "mod",
        "\\triangle": "△",
        "\\varphi": "φ",
        "\\gcd": "gcd",
        "\\lcd": "lcd",
        "\\lt": "<",
        "\\le": "≤",
        "\\gt": ">",
        "\\ge": "≥",
        "\\to": "→",
        "\\ne": "≠",
    }
    for key, value in replacements.items():
        string = string.replace(key, value)

    # Superscript
    string = re.sub(
        r"\^(\{([^}]+)}|(\S))",
        lambda m: (m.group(2) or m.group(3)).translate(SUPERSCRIPT_MAP),
        string,
    )
    # Subscript
    string = re.sub(
        r"_(\{([^}]+)}|(\S))",
        lambda m: (m.group(2) or m.group(3)).translate(SUBSCRIPT_MAP),
        string,
    )

    # Fractions
    def _frac_replacer(match):
        numerator = match.group(1).strip()
        denominator = match.group(2).strip()
        return f"{numerator}/{denominator}"

    string = re.sub(r"\\(?:d?frac)\{([^}]+)}\{([^}]+)}", _frac_replacer, string)

    # Restore URLs
    for i, url in enumerate(url_placeholders):
        string = string.replace(f"<<URL{i}>>", url)

    return string
