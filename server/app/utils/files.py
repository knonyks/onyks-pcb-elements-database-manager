import os
import pyaltiumlib

def findAllFiles(path, ext):
    foundFiles = []
    ext = ext.lstrip('.')
    
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith(f'.{ext.lower()}'):
                full_path = os.path.join(root, file)
                foundFiles.append(full_path)
    
    return foundFiles

def listFilesWithType(path):
    result = []
    if str(path).lower().endswith('.schlib'):
        schlib_file = pyaltiumlib.read(str(path))
        symbols = schlib_file.list_parts()
        result = [[i, 'symbol'] for i in symbols]
    elif str(path).lower().endswith('.pcblib'):
        pcblib_file = pyaltiumlib.read(str(path))
        footprints = pcblib_file.list_parts()
        result = [[i, 'footprint'] for i in footprints]
    else:
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                result.append([entry, "folder"])
            else:
                ext = os.path.splitext(entry)[1][1:]
                if ext == 'PcbLib':
                    ext = 'pcblib'
                elif ext == 'SchLib':
                    ext = 'schlib'
                else:
                    ext = 'file'
                if ext:
                    result.append([entry, ext])
    return result