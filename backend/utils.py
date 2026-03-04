import re

def is_string_valid(text: str) -> bool:
    if not isinstance(text, str):
        return False
    pattern = r'^(?!\s+$)([^\W\d_]|\s|-){2,}$'
    return bool(re.match(pattern, text))