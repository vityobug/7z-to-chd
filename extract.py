#!/usr/bin/env python3

import os
import py7zr
import shutil
import subprocess
import glob

input_path = "/input"
output_path = "/output"


def convert_to_chd(source_dir_or_file):
    """Convert disc images in a directory (or a single file) to CHD."""
    if os.path.isfile(source_dir_or_file):
        files_to_check = [source_dir_or_file]
        search_dir = os.path.dirname(source_dir_or_file)
    else:
        files_to_check = glob.glob(
            os.path.join(source_dir_or_file, "**", "*"), recursive=True
        )
        search_dir = source_dir_or_file

    converted = False
    for f in files_to_check:
        ext = os.path.splitext(f)[1].lower()
        if ext not in (".cue", ".iso", ".gdi", ".img"):
            continue
        # Skip .iso if a matching .cue exists (cue takes priority)
        if ext == ".iso" and os.path.exists(os.path.splitext(f)[0] + ".cue"):
            print(f"  Skipping {os.path.basename(f)} (matching .cue found)")
            continue
        base = os.path.splitext(os.path.basename(f))[0]
        chd_out = os.path.join(output_path, base + ".chd")
        print(f"  Converting: {os.path.basename(f)} -> {base}.chd")
        result = subprocess.run(["chdman", "createcd", "-i", f, "-o", chd_out])
        if result.returncode == 0:
            converted = True
        else:
            print(f"  WARNING: chdman failed for {os.path.basename(f)}")
    return converted


os.makedirs(output_path, exist_ok=True)

input_files = os.listdir(input_path)
seven_zip_files = [f for f in input_files if f.lower().endswith(".7z")]
loose_images = [
    f
    for f in input_files
    if os.path.splitext(f)[1].lower() in (".iso", ".cue", ".gdi", ".img", ".bin")
]

# --- Handle .7z archives ---
if seven_zip_files:
    print(f"Found {len(seven_zip_files)} .7z archive(s) to process.")
    for i, file in enumerate(seven_zip_files, 1):
        print(f"\n[{i}/{len(seven_zip_files)}] Extracting {file}...")
        extract_dir = os.path.join(output_path, os.path.splitext(file)[0])
        os.makedirs(extract_dir, exist_ok=True)
        with py7zr.SevenZipFile(os.path.join(input_path, file), "r") as archive:
            archive.extractall(extract_dir)
        print(f"  Extracted to {extract_dir}")
        convert_to_chd(extract_dir)
        # Cleanup extracted dir (keep only .chd)
        shutil.rmtree(extract_dir)
        print(f"  Cleaned up {extract_dir}")

# --- Handle loose disc images ---
if loose_images:
    print(f"\nFound {len(loose_images)} loose disc image(s) to process.")
    for f in loose_images:
        full_path = os.path.join(input_path, f)
        ext = os.path.splitext(f)[1].lower()
        if ext == ".bin":
            continue  # .bin files are handled via their .cue
        convert_to_chd(full_path)

if not seven_zip_files and not loose_images:
    print("No .7z archives or disc images found in /input.")

print("\nDone!")
