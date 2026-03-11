import re
import base64
import json
from typing import Optional, Dict, Any

def is_supplier_name_valid(text: str) -> bool:
    if not isinstance(text, str):
        return False
    pattern = r'^(?!\s)(?:[^\W\d_]|\s|-){2,}(?<!\s)$'
    return bool(re.match(pattern, text))

def is_manufacturer_name_valid(text: str) -> bool:
    return is_supplier_name_valid(text)

def encode_cursor(cursor_dict) -> str:
    encoded_bytes = base64.urlsafe_b64encode(json.dumps(cursor_dict).encode())
    return encoded_bytes.decode('utf-8')

def decode_cursor(cursor_str: Optional[str]) -> Optional[Dict[str, Any]]:
    if not cursor_str:
        return None
    try:
        decoded_bytes = base64.urlsafe_b64decode(cursor_str.encode('utf-8'))
        return json.loads(decoded_bytes.decode('utf-8'))
    except Exception:
        return None