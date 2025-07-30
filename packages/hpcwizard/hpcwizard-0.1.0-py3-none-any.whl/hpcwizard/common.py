# ruff: noqa: D100

def escape_chars(s:str, chars:str, esc:str="\\") -> str:
    """Escape special characters in a string."""

    x: dict[str, str | int | None] = {}
    for char in chars:
        x[char] = f"{esc}{char}"

    return s.translate(str.maketrans(x))
