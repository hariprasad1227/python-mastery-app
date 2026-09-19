import os
import zipfile
import shutil

source_dir = r"C:\Users\gumma\.gemini\antigravity\scratch\python-mastery"
zip_path = r"C:\Users\gumma\.gemini\antigravity\scratch\python-mastery.zip"
downloads_path = r"C:\Users\gumma\Downloads\python-mastery.zip"

exclude_dirs = {"node_modules", ".next", ".pytest_cache", "__pycache__", ".git"}
exclude_files = {".DS_Store", "desktop.ini"}

print(f"Creating zip from {source_dir}...")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file in exclude_files:
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, source_dir)
            try:
                zipf.write(full_path, rel_path)
            except Exception as e:
                print(f"Skipping {rel_path}: {e}")

print(f"Zip created at {zip_path}, copying to {downloads_path}...")
shutil.copy2(zip_path, downloads_path)
size_mb = os.path.getsize(downloads_path) / (1024 * 1024)
print(f"SUCCESS! Archive copied to {downloads_path} ({size_mb:.2f} MB)")
