import re
import base64
import json
from typing import Optional, Dict, Any
import subprocess
import xml.etree.ElementTree as ET
import pyaltiumlib
import io

### REPOSITORY ###
def repository_get_folder_list(url, path, user, password):
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

def repository_get_pcb_file_content(url, path, user, password):
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

### MANUFACTURER ###
def manufacturer_name_validation(text: str) -> bool:
    return supplier_name_validation(text)

### SUPPLIER ###
def supplier_name_validation(text: str) -> bool:
    if not isinstance(text, str):
        return False
    pattern = r'^(?!\s)(?:[^\W\d_]|\s|-){2,}(?<!\s)$'
    return bool(re.match(pattern, text))