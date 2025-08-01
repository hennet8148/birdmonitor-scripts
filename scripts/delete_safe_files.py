import os

# Filenames generated by compare_backup_hashes.py
FILES_TO_DELETE = [
    "safe_to_delete_csv.txt",
    "safe_to_delete_wav.txt"
]

def delete_files_from_list(file_list_path):
    if not os.path.exists(file_list_path):
        print(f"File list not found: {file_list_path}")
        return

    with open(file_list_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    deleted_count = 0
    for filepath in lines:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                deleted_count += 1
            else:
                print(f"Not found (skipped): {filepath}")
        except Exception as e:
            print(f"Failed to delete {filepath}: {e}")

    print(f"✔️ Deleted {deleted_count} files from list: {file_list_path}")

if __name__ == "__main__":
    for filelist in FILES_TO_DELETE:
        delete_files_from_list(filelist)

