import os
import hashlib

BASE_MAIN = "/Users/chuck/BirdMonitor/data"
BASE_BACKUP1 = "/Volumes/ShopOne/BirdMonitor"
BASE_BACKUP2 = "/Volumes/ShopTwo/BirdMonitor"

SUBDIRS = [
    "processed_csv",
    "processed_wav",
    "processed_csv_s2",
    "processed_wav_s2"
]

def compute_hash(filepath):
    """Compute SHA1 hash of a file (if needed)."""
    sha1 = hashlib.sha1()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha1.update(chunk)
        return sha1.hexdigest()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def get_file_info(directory):
    """Return dict: filename -> (size, mtime, optional hash)"""
    info = {}
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return info
    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):
            try:
                stat = os.stat(full_path)
                info[filename] = {
                    "size": stat.st_size,
                    "mtime": stat.st_mtime,
                    "path": full_path
                }
            except Exception as e:
                print(f"Stat error on {full_path}: {e}")
    return info

def compare_and_write_safe_files(subdir):
    print(f"\n🔍 Checking directory: {subdir}")

    main = get_file_info(os.path.join(BASE_MAIN, subdir))
    b1   = get_file_info(os.path.join(BASE_BACKUP1, subdir))
    b2   = get_file_info(os.path.join(BASE_BACKUP2, subdir))

    safe_to_delete = []

    for filename, m_info in main.items():
        b1_info = b1.get(filename)
        b2_info = b2.get(filename)

        if not b1_info or not b2_info:
            continue  # skip: not present in both backups

        if (m_info["size"] == b1_info["size"] == b2_info["size"] and
            abs(m_info["mtime"] - b1_info["mtime"]) < 2 and
            abs(m_info["mtime"] - b2_info["mtime"]) < 2):
            # Size and time match — assume safe
            safe_to_delete.append(m_info["path"])
        else:
            # Conflict — double-check by hash
            h_main = compute_hash(m_info["path"])
            h_b1 = compute_hash(b1_info["path"]) if b1_info else None
            h_b2 = compute_hash(b2_info["path"]) if b2_info else None
            if h_main and h_main == h_b1 == h_b2:
                safe_to_delete.append(m_info["path"])

    out_file = f"safe_to_delete_{subdir.replace('processed_', '')}.txt"
    with open(out_file, "w") as f:
        for path in safe_to_delete:
            f.write(path + "\n")

    print(f"✅ {len(safe_to_delete)} safe to delete in {subdir}. → {out_file}")

if __name__ == "__main__":
    for subdir in SUBDIRS:
        compare_and_write_safe_files(subdir)

