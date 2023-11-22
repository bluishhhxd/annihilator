import os
import hashlib
from collections import defaultdict
import time
from colorama import init, Fore

init(autoreset=True)

def print_message(message, color=Fore.RESET):
    print(f"{color}{message}{Fore.RESET}")

def print_red(text):
    print_message(text, Fore.RED)

def print_green(text):
    print_message(text, Fore.GREEN)

def print_yellow(text):
    print_message(text, Fore.YELLOW)

def print_cyan(text):
    print_message(text, Fore.CYAN)

def print_magenta(text):
    print_message(text, Fore.MAGENTA)

def print_BLUE(text):
    print_message(text, Fore.BLUE)

def compute_hash(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)
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
    print_magenta("\n\nWelcome to project ANNIHILATE.\n"
          "It is specifically designed to delete duplicate files from your Pc/laptop.\n"
          "Enjoy your free space :)\n\n\n"
          "1.) Scan: Scans for duplicate files in the provided directory path.\n"
          "2.) Quit: Quits the program")

    while True:
        button = input("\nType your choice:\n").replace(" ", '')
        if button.lower() == 'scan':
            while True:
                directory_to_scan = input("\nEnter the directory path to scan for duplicate files: ")

                if directory_to_scan.capitalize() == "Quit":
                    print_cyan("\n\nOkay, Thank you for using Annihilator.\n\n\n")
                    break
                elif directory_to_scan == "":
                    print_red("\nTry again, Directory path can't be empty.")
                elif not os.path.isdir(directory_to_scan):
                    print_red("\nPlease enter a valid directory path.")
                else:
                    duplicate_files = find_duplicate_files(directory_to_scan)

                    if not duplicate_files:
                        print_yellow("\nScanning...")
                        time.sleep(2)
                        print_green("No duplicate files were found.")
                        other_duplication = input("\nDo you want to scan for duplicate files in other directories (yes/no)?\n").strip().lower()
                        if other_duplication == 'yes':
                            continue
                        elif other_duplication == 'no':
                            print_cyan('\nOkay, Thank you for using Annihilator.\n\n\n')
                            break
                    else:
                        print_yellow("\nScanning...")
                        time.sleep(4)
                        print_cyan("\nDuplicate files found:")
                        for files in duplicate_files:
                            for file_path in files:
                                print_message(file_path, Fore.YELLOW)

                        confirmation = input("\nDo you want to delete these duplicate files (yes/no)?\n").strip().lower()

                        if confirmation == 'yes':
                            print_yellow("\nFile deletion in process...")
                            time.sleep(5)
                            delete_duplicates(duplicate_files)
                            print_green("Duplicate files were successfully deleted.")
                            another_duplication = input("\nDo you want to find other duplicate files in your system (yes/no)?\n").strip().lower()
                            if another_duplication == 'yes':
                                continue
                            elif another_duplication == 'no':
                                print_cyan('\nOkay, Thank you for using Annihilator.\n\n\n')
                                break
                        elif confirmation == 'no':
                            other_duplication = input("\nDo you want to find other duplicate files in your system (yes/no)?\n").strip().lower()
                            if other_duplication == 'yes':
                                continue
                            elif other_duplication == 'no':
                                print_cyan('\nOkay, Thank you for using Annihilator.\n\n\n')
                                break
                            
        elif button.lower() == 'quit':
            print_cyan("\nThank you for using Annihilator.\n\n\n")
            break
        elif button == '':
            print_red("\nYou can't leave it empty\nIf you wish to exit the program type" + ' "quit".')
            continue
        else:
            print_red("\nInvalid option, Try again.")
            continue
        break 
