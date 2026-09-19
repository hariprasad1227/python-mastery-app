"""
Package Python Mastery into a clean zip distribution.
Excludes node_modules, .next, __pycache__, and test caches.
"""

import os
import zipfile

SOURCE_DIR = r"C:\Users\gumma\.gemini\antigravity\scratch\python-mastery"
OUTPUT_ZIP = r"C:\Users\gumma\.gemini\antigravity\scratch\python-mastery.zip"

EXCLUDE_DIRS = {
    "node_modules",
    ".next",
    "__pycache__",
    ".pytest_cache",
    ".git"
}

EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo"
}

def create_zip():
    print(f"Packaging project from {SOURCE_DIR} to {OUTPUT_ZIP}...")
    total_files = 0
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(SOURCE_DIR):
            # Prune excluded directories in-place
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in EXCLUDE_EXTENSIONS:
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, SOURCE_DIR)
                zipf.write(full_path, arcname=os.path.join("python-mastery", rel_path))
                total_files += 1

    zip_size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"Successfully packaged {total_files} files into {OUTPUT_ZIP} ({zip_size_mb:.2f} MB)")

if __name__ == "__main__":
    create_zip()
