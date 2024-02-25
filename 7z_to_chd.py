#!/usr/bin/env python3

import os
import py7zr
import shutil
import shlex

# Ask the user for the path containing the .7z archives to extract
archive_path = input("Enter the path containing the .7z archives to extract: ")

# Ask the user for the path where the extracted files should be placed
extracted_path = input("Enter the path where the extracted files should be placed: ")

# List all files in the archive directory
files = os.listdir(archive_path)

# Filter .7z files
seven_zip_files = [file for file in files if file.endswith(".7z")]

total_archives = len(seven_zip_files)
processed_archives = 0

# Extract each .7z file into its own directory
for file in seven_zip_files:
    processed_archives += 1
    print(f"Processing archive {processed_archives}/{total_archives}")
    
    # Create directory for extracted contents
    extracted_directory = os.path.splitext(file)[0]  # Remove .7z extension
    extracted_full_path = os.path.join(extracted_path, extracted_directory)
    os.makedirs(extracted_full_path, exist_ok=True)

    # Extract .7z file
    with py7zr.SevenZipFile(os.path.join(archive_path, file), 'r') as archive:
        archive.extractall(extracted_full_path)

    print(f"Extracted {file} to {extracted_full_path}")

    # Run tochd command
    command = f"tochd -t 6 '{extracted_full_path}'"
    os.system(command)

# Move .chd files into a single directory
chd_directory = os.path.join(extracted_path, "chd_files")
os.makedirs(chd_directory, exist_ok=True)

for root, dirs, files in os.walk(extracted_path):
    for file in files:
        if file.endswith(".chd"):
            destination = os.path.join(chd_directory, file)
            if os.path.exists(destination):
                # Rename file if it already exists in the destination directory
                base_name, ext = os.path.splitext(file)
                count = 1
                while os.path.exists(destination):
                    new_name = f"{base_name}_{count}{ext}"
                    destination = os.path.join(chd_directory, new_name)
                    count += 1
            shutil.move(os.path.join(root, file), destination)

# Delete extracted files directories
for root, dirs, files in os.walk(extracted_path, topdown=False):
    for directory in dirs:
        directory_path = os.path.join(root, directory)
        if not any(file.endswith(".chd") for file in os.listdir(directory_path)):
            shutil.rmtree(directory_path)

print("Extraction, file moving, and cleanup complete.")
