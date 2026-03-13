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

HASH_CHUNK_SIZE_BYTES = 65536
PREFIX_HASH_BYTES = 4 * 1024 * 1024  # 4MB prefix for quick candidate grouping

def _safe_getsize(file_path):
    try:
        return os.path.getsize(file_path), None
    except (OSError, FileNotFoundError, PermissionError) as e:
        return None, e

def compute_hash(file_path, *, max_bytes=None):
    hasher = hashlib.md5()
    read_so_far = 0
    with open(file_path, 'rb') as file:
        while True:
            to_read = HASH_CHUNK_SIZE_BYTES
            if max_bytes is not None:
                remaining = max_bytes - read_so_far
                if remaining <= 0:
                    break
                to_read = min(to_read, remaining)

            data = file.read(to_read)
            if not data:
                break
            hasher.update(data)
            read_so_far += len(data)

    return hasher.hexdigest()


def find_duplicate_files(directory_to_scan):
    skipped = []  # list[tuple[path, error_str]]

    # First pass: group files by size (cheap) so we only hash plausible duplicates.
    files_by_size = defaultdict(list)
    for root, dirs, files in os.walk(directory_to_scan, followlinks=False):
        # Avoid scanning symlinked dirs/junctions where it can create loops.
        try:
            dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
        except OSError:
            # If we can't inspect links here, keep default behavior but continue.
            pass

        for filename in files:
            file_path = os.path.join(root, filename)
            size, err = _safe_getsize(file_path)
            if err is not None:
                skipped.append((file_path, str(err)))
                continue
            files_by_size[size].append(file_path)

    candidate_paths = []
    for size, paths in files_by_size.items():
        if len(paths) > 1:
            candidate_paths.extend(paths)

    if not candidate_paths:
        return [], skipped

    # Second pass: quick prefix-hash for candidate grouping (then full hash confirm).
    prefix_groups = defaultdict(list)
    for file_path in candidate_paths:
        try:
            prefix_hash = compute_hash(file_path, max_bytes=PREFIX_HASH_BYTES)
        except (OSError, FileNotFoundError, PermissionError) as e:
            skipped.append((file_path, str(e)))
            continue
        prefix_groups[prefix_hash].append(file_path)

    file_hashes = defaultdict(list)
    for paths in prefix_groups.values():
        if len(paths) <= 1:
            continue
        for file_path in paths:
            try:
                full_hash = compute_hash(file_path)
            except (OSError, FileNotFoundError, PermissionError) as e:
                skipped.append((file_path, str(e)))
                continue
            file_hashes[full_hash].append(file_path)

    duplicate_files = [paths for paths in file_hashes.values() if len(paths) > 1]
    return duplicate_files, skipped


def delete_duplicates(duplicate_files):
    deleted = []
    failed = []  # list[tuple[path, error_str]]

    for files in duplicate_files:
        if not files:
            continue
        kept = files[0]
        print_cyan(f"\nKeeping: {kept}")
        for file_path in files[1:]:
            try:
                if not os.path.exists(file_path):
                    failed.append((file_path, "File not found"))
                    continue
                os.remove(file_path)
                deleted.append(file_path)
                print(f"Deleted: {file_path}")
            except OSError as e:
                failed.append((file_path, str(e)))
                print(f"Error deleting {file_path}: {e}")

    return deleted, failed


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
                directory_to_scan = input("\nEnter the directory path to scan for duplicate files: ").strip()
                directory_to_scan_lower = directory_to_scan.lower()

                if directory_to_scan_lower == "quit":
                    print_cyan("\n\nOkay, Thank you for using Annihilator.\n\n\n")
                    break
                elif directory_to_scan == "":
                    print_red("\nTry again, Directory path can't be empty.")
                elif not os.path.isdir(directory_to_scan):
                    print_red("\nPlease enter a valid directory path.")
                else:
                    duplicate_files, skipped = find_duplicate_files(directory_to_scan)

                    if not duplicate_files:
                        print_yellow("\nScanning...")
                        time.sleep(2)
                        print_green("No duplicate files were found.")
                        if skipped:
                            print_yellow(f"\nSkipped {len(skipped)} file(s) due to access/errors.")
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

                        if skipped:
                            print_yellow(f"\nSkipped {len(skipped)} file(s) due to access/errors.")

                        confirmation = input("\nDo you want to delete these duplicate files (yes/no)?\n").strip().lower()

                        if confirmation == 'yes':
                            print_yellow("\nFile deletion in process...")
                            time.sleep(5)
                            deleted, failed = delete_duplicates(duplicate_files)
                            if failed:
                                print_yellow(f"\nFinished with {len(failed)} deletion failure(s).")
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
