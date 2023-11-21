import os
import hashlib
from collections import defaultdict
import time


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
        for file_path in files[1:]:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")


if __name__ == "__main__":
    print("\n\nWelcome to project ANNIHILATE.\nIt is specifically designed to delete duplicate files from your Pc/laptop.\nEnjoy your free space :)\n\n\n1.) Scan: Scans for duplicate files in the provided directory path.\n2.) Quit: Quits the program")
    while True: 
        button = input("\nType your choice:\n").replace(" ",'')
        if button.lower() == 'scan':
            pass
        elif button.lower() == 'quit':
            print("\nThank you for using our Annihilator.\n\n\n")
            break
        elif button == '':
            print("\nYou can't leave it empty\nIf you wish to exit the program type" + ' "quit".')
            continue
        else:
            print("\nInvalid option, Try again.")
            continue
        while True:
            directory_to_scan = input("\nEnter the directory path to scan for duplicate files: ")

            if directory_to_scan.capitalize() == "Quit" :
                print("\n\nOkay, Thank you for using our Annihilator.\n\n\n")
                break
            elif directory_to_scan == "" :
                print("\nTry again, Directory path can't be empty.")
            elif not os.path.isdir(directory_to_scan):
                print("\nPlease enter a valid directory path.")
            else:
                duplicate_files = find_duplicate_files(directory_to_scan)

                if not duplicate_files:
                    print("\nScanning...")
                    time.sleep(2)
                    print("No duplicate files were found.")
                else:
                    print("\nScanning...")
                    time.sleep(4)
                    print("\nDuplicate files found:")
                    for files in duplicate_files:
                        for file_path in files:
                            print(file_path)

                    confirmation = input("\nDo you want to delete these duplicate files (yes/no)?\n").strip().lower()

                    if confirmation == 'yes':
                        print("\nFile deletion in process...")
                        time.sleep(5)
                        delete_duplicates(duplicate_files)
                        print("Duplicate files were successfully deleted.")
                        another_duplication = input("\nDo you want to find other duplicate files in your system (yes/no)?\n").strip().lower()
                        if another_duplication == 'yes':
                            continue
                        elif another_duplication == 'no':
                            print('\nOkay, Thank you for using our Annihilator.\n\n\n')
                            break
                    elif confirmation == 'no':
                        print("\nOkay, Thank you for using our Annihilator.\n\n\n")
                        break
        break
