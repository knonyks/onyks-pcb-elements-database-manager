import os

import os

def findAllFiles(path, ext):
    foundFiles = []
    ext = ext.lstrip('.')
    
    for root, _, files in os.walk(path):
        for file in files:
            if file.lower().endswith(f'.{ext.lower()}'):
                full_path = os.path.join(root, file)
                foundFiles.append(full_path)
    
    return foundFiles