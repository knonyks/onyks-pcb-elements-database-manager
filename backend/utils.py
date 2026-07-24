import re
import base64
import json
from typing import Optional, Dict, Any
import subprocess
import xml.etree.ElementTree as ET
import pyaltiumlib
import io
import os
from sqlalchemy import text

def repositoryGetFolderList(url, path, user, password):
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
            nameEntry = entry.find("name")
            name = nameEntry.text if nameEntry is not None else "unknown"
            _, ext = os.path.splitext(name)
            if ext.lower() == '.schlib':
                kind = 'schlib'
            elif ext.lower() == '.pcblib':
                kind = 'pcblib'
            items.append({
                "name":name,
                "type": kind
            })
        return items
    except Exception as e:
        return e

def repositoryGetPCBFileContent(url, path, user, password):
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




async def dbCreateOrUpdateElementViews(db_connection):

    try:
        result_tables = await db_connection.execute(text("SELECT DISTINCT name FROM private.tables"))
        tables = result_tables.fetchall()
        
        expected_views = []
        table_to_view_map = {} 
        for table_row in tables:
            table_name = table_row[0]
            view_name = f"view_elements_{table_name.lower().replace(' ', '_').replace('-', '_')}"
            expected_views.append(view_name)
            table_to_view_map[table_name] = view_name

        result_existing_views = await db_connection.execute(text("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'private' AND table_name LIKE 'view_elements_%'
        """))
        existing_views = [row[0] for row in result_existing_views.fetchall()]

        views_to_drop = set(existing_views) - set(expected_views)
        for old_view in views_to_drop:
            await db_connection.execute(text(f"DROP VIEW IF EXISTS private.{old_view} CASCADE"))

        result_suppliers = await db_connection.execute(text("SELECT name FROM private.suppliers"))
        suppliers = result_suppliers.fetchall()
        supplier_names = [supplier[0] for supplier in suppliers]
        
        supplier_columns = ""
        if supplier_names:
            for supplier_name in supplier_names:
                safe_supplier_name = supplier_name.lower().replace(' ', '_').replace('-', '_')
                supplier_columns += f",\n                (suppliers->>'{supplier_name}')::text AS supplier_{safe_supplier_name}"
        
        for table_name, view_name in table_to_view_map.items():
            
            await db_connection.execute(text(f"DROP VIEW IF EXISTS private.{view_name} CASCADE"))
            
            create_view_query = text(f"""
            CREATE VIEW private.{view_name} AS
            SELECT 
                uuid,
                part_name,
                manufacturer,
                description,
                value,
                availability,
                datasheet,
                library_ref,
                library_path,
                created_at
                {supplier_columns}
            FROM private.elements
            WHERE "table" = '{table_name}'
            ORDER BY created_at DESC
            """)
        
            await db_connection.execute(create_view_query)
        
        await db_connection.commit()
        return {"status": "success", "message": "Views updated and old ones cleaned up successfully"}
    
    except Exception as e:
        await db_connection.rollback()
        return {"status": "error", "message": str(e)}



# ### MANUFACTURER ###
# def manufacturer_name_validation(text: str) -> bool:
#     return supplier_name_validation(text)

# ### SUPPLIER ###
# def supplier_name_validation(text: str) -> bool:
#     if not isinstance(text, str):
#         return False
#     pattern = r'^(?!\s)(?:[^\W\d_]|\s|-){2,}(?<!\s)$'
#     return bool(re.match(pattern, text))