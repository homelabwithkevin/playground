# Claude Promopt: For each file in the path, get the date taken via exif because they are photos, create a folder if needed for each month, then move the photo

import os
import shutil
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

path = r"C:\example"

def get_date_taken(image_path):
    """Extract date taken from EXIF data."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()

        if exif_data is None:
            return None

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "DateTime":
                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Error reading EXIF from {image_path}: {e}")

    return None

def organize_photos(source_path):
    """Organize photos into monthly folders based on EXIF date."""
    source_dir = Path(source_path)

    if not source_dir.exists():
        print(f"Path does not exist: {source_path}")
        return

    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"}

    for file_path in source_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            date_taken = get_date_taken(file_path)

            if date_taken:
                month_folder = date_taken.strftime("%Y-%m")
                dest_folder = source_dir / month_folder

                dest_folder.mkdir(exist_ok=True)
                dest_path = dest_folder / file_path.name

                shutil.move(str(file_path), str(dest_path))
                print(f"Moved: {file_path.name} -> {month_folder}/")
            else:
                print(f"No date found in EXIF: {file_path.name}")

if __name__ == "__main__":
    organize_photos(path)
