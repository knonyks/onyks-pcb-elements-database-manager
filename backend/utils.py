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

class Repository:

    @staticmethod
    def getFolderList(url, path):
        if path:
            full_url = f"{url.rstrip('/')}/{path.strip('/')}"
        else:
            full_url = url
        command = ["svn", "list", "--xml", "--non-interactive", full_url]

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
        
    @staticmethod
    def getPcbContent(url, path):
        if path:
            full_url = f"{url.rstrip('/')}/{path.strip('/')}"
        else:
            full_url = url
        command = ["svn", "cat", full_url]

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
    
    result_tables = await db_connection.execute(text("SELECT DISTINCT id, name FROM private.tables"))
    tables = result_tables.fetchall()
    
    expected_views = []
    table_to_view_map = {} 
    
    for table_row in tables:
        table_id = table_row[0]
        table_name = table_row[1]
        
        safe_table_name = table_name.lower().replace(' ', '_').replace('-', '_')
        view_name = f"table_{table_id}_{safe_table_name}"
        
        expected_views.append(view_name)
        table_to_view_map[table_name] = view_name

    result_existing_views = await db_connection.execute(text("""
        SELECT table_name 
        FROM information_schema.views 
        WHERE table_schema = 'public' AND table_name LIKE 'table_%'
    """))
    existing_views = [row[0] for row in result_existing_views.fetchall()]

    views_to_drop = set(existing_views) - set(expected_views)
    for old_view in views_to_drop:
        await db_connection.execute(text(f"DROP VIEW IF EXISTS public.{old_view} CASCADE"))

    result_suppliers = await db_connection.execute(text("SELECT id, name FROM private.suppliers"))
    suppliers = result_suppliers.fetchall()
    
    supplier_columns = ""
    if suppliers:
        for supplier_row in suppliers:
            supplier_id = supplier_row[0]
            supplier_name = supplier_row[1]
            
            safe_supplier_name = supplier_name.lower().replace(' ', '_').replace('-', '_')
            
            supplier_columns += f",\n                (suppliers->>'{supplier_id}')::text AS supplier_{supplier_id}_{safe_supplier_name}"
    
    for table_name, view_name in table_to_view_map.items():
        
        await db_connection.execute(text(f"DROP VIEW IF EXISTS public.{view_name} CASCADE"))
        
        safe_table_name_query = table_name.replace("'", "''")
        
        create_view_query = text(f"""
        CREATE VIEW public.{view_name} AS
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
            footprint_reference_1,
            footprint_path_1,
            footprint_reference_2,
            footprint_path_2,
            footprint_reference_3,
            footprint_path_3,
            created_at
            {supplier_columns}
        FROM private.elements
        WHERE "table" = '{safe_table_name_query}'
        ORDER BY created_at DESC
        """)
    
        await db_connection.execute(create_view_query)

    await db_connection.commit()
    
    return {"status": "success", "message": "Views updated and old ones cleaned up successfully"}