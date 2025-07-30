# doc_utils/file_utils.py

import os
import re
import zipfile
from datetime import datetime


def collect_files(scan_dirs, extensions, exclude_dirs=None, exclude_files=None):
    """
    Recursively collect files with given extensions from scan_dirs, excluding symlinks, exclude_dirs, and exclude_files.
    Returns a list of normalized file paths.
    """
    exclude_dirs = set(os.path.abspath(os.path.normpath(d)) for d in (exclude_dirs or []))
    exclude_files = set(os.path.abspath(os.path.normpath(f)) for f in (exclude_files or []))
    found_files = []
    for base_dir in scan_dirs:
        for root, dirs, files in os.walk(base_dir):
            abs_root = os.path.abspath(root)
            # Exclude directories by absolute path
            dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d)) and os.path.abspath(os.path.join(root, d)) not in exclude_dirs]
            for f in files:
                file_path = os.path.normpath(os.path.join(root, f))
                abs_file_path = os.path.abspath(file_path)
                if os.path.islink(file_path):
                    continue
                if abs_file_path in exclude_files:
                    continue
                if os.path.splitext(f)[1].lower() in extensions:
                    found_files.append(file_path)
    return list(dict.fromkeys(found_files))


def write_manifest_and_archive(unused_files, archive_dir, manifest_prefix, archive_prefix, archive=False):
    """
    Write a manifest of unused files and optionally archive and delete them.
    Returns the manifest path and (if archive=True) the archive path.
    """
    if not unused_files:
        print("No unused files found. No manifest or ZIP archive created.")
        return None, None
    now = datetime.now()
    datetime_str = now.strftime('%Y-%m-%d_%H%M%S')
    output_file = f'{manifest_prefix}-{datetime_str}.txt'
    os.makedirs(archive_dir, exist_ok=True)
    manifest_path = os.path.join(archive_dir, output_file)
    with open(manifest_path, 'w') as f:
        for file in unused_files:
            print(file)
            f.write(file + '\n')
    archive_path = None
    if archive:
        archive_path = os.path.join(archive_dir, f"{archive_prefix}-{datetime_str}.zip")
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in unused_files:
                arcname = os.path.relpath(file)
                print(f"Archiving: {file} -> {archive_path} ({arcname})")
                zipf.write(file, arcname)
                os.remove(file)
    return manifest_path, archive_path
