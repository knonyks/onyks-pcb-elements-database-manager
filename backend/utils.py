import re
import base64
import json
from typing import Optional, Dict, Any
import subprocess
import xml.etree.ElementTree as ET
import pyaltiumlib
import io


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
    




### SKONCZONE 100%
def svn_get_folder_list(url, path, user, password):
    if path:
        full_url = f"{url.rstrip('/')}/{path.strip('/')}"
    else:
        full_url = url
    command = ["svn", "list", "--xml", "--non-interactive", full_url]
    if user and password:
        command.extend([
            "--username", user, 
            "--password", password, 
            "--trust-server-cert",
            "--no-auth-cache"
        ])
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        root = ET.fromstring(result.stdout)
        items = []
        for entry in root.findall(".//entry"):
            kind = entry.get("kind")
            name_elem = entry.find("name")
            name = name_elem.text if name_elem is not None else "unknown"
            items.append({
                "name":name,
                "type": "folder" if kind == "dir" else "file"
            })
        return items
    except Exception as e:
        return e

def svn_get_altium_content(url, path, user, password):
    if path:
        full_url = f"{url.rstrip('/')}/{path.strip('/')}"
    else:
        full_url = url
    command = ["svn", "cat", full_url]
    if user and password:
        command.extend([
            "--username", user, 
            "--password", password, 
            "--trust-server-cert",
            "--no-auth-cache"
        ])
    try:
        result = subprocess.run(command, capture_output=True, check=True)
    except Exception as e:
        print(f"Unexpected execution error: {e}")
        raise e
    libfile_obj = io.BytesIO(result.stdout)

    schlib_pcblib_name = str(path).split('/')[-1].lower()
    elements = []

    if schlib_pcblib_name.endswith('.schlib'):
        schlib_file = pyaltiumlib.read(schlib_pcblib_name, libfile_obj)
        symbols = schlib_file.list_parts()
        elements = [{"name": i, "type": 'symbol'} for i in symbols]
        
    elif schlib_pcblib_name.endswith('.pcblib'):
        pcblib_file = pyaltiumlib.read(schlib_pcblib_name, libfile_obj)
        footprints = pcblib_file.list_parts()
        elements = [{"name": i, "type": 'footprint'} for i in footprints]
    return elements