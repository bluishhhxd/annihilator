import os
import hashlib
from collections import defaultdict


def compute_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read the file in 64KB chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()


def find_duplicate_files(directory_to_scan):
    file_hashes = defaultdict(list)

    for root, dirs, files in os.walk(directory_to_scan):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hash = compute_hash(file_path)
            file_hashes[file_hash].append(file_path)

    duplicate_files = [files for files in file_hashes.values() if len(files) > 1]
    return duplicate_files


def delete_duplicates(duplicate_files):
    for files in duplicate_files:
        # Keep the first file, delete the rest
        for file_path in files[1:]:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")


if __name__ == "__main__":
    directory_to_scan = input("Enter the directory path to scan: ")

    if not os.path.isdir(directory_to_scan):
        print("Invalid directory path.")
    else:
        duplicate_files = find_duplicate_files(directory_to_scan)

        if not duplicate_files:
            print("No duplicate files found.")
        else:
            print("Duplicate files found:")
            for files in duplicate_files:
                for file_path in files:
                    print(file_path)

            confirmation = input("Delete duplicates? (yes/no): ").strip().lower()

            if confirmation == 'yes':
                delete_duplicates(duplicate_files)
                print("Duplicates deleted.")
            else:
                print("Duplicates not deleted.")
