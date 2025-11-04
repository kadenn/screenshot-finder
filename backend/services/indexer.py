"""Indexer service to scan and index screenshots."""
import os
from pathlib import Path
from typing import List
from PIL import Image
from services.gpt5_service import analyze_image
from models import get_screenshot_by_filename, insert_screenshot, get_all_screenshots, delete_screenshot

SCREENSHOTS_DIR = "../screenshots"
SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def get_image_files() -> List[Path]:
    """Get all image files from the screenshots directory."""
    screenshots_path = Path(SCREENSHOTS_DIR)
    if not screenshots_path.exists():
        screenshots_path.mkdir(parents=True, exist_ok=True)
        return []
    
    image_files = []
    for file_path in screenshots_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_FORMATS:
            image_files.append(file_path)
    
    return image_files


def scan_and_index():
    """Scan the screenshots directory and index new images."""
    print("🔍 Scanning screenshots directory...")
    
    image_files = get_image_files()
    print(f"📁 Found {len(image_files)} image files")
    
    if not image_files:
        print("⚠️  No screenshots found. Add images to /screenshots folder.")
        return
    
    # Get existing screenshots from DB
    existing_screenshots = get_all_screenshots()
    existing_filenames = {s['filename'] for s in existing_screenshots}
    
    # Check for deleted files
    current_filenames = {f.name for f in image_files}
    deleted_filenames = existing_filenames - current_filenames
    
    for deleted_filename in deleted_filenames:
        print(f"🗑️  Removing deleted file from DB: {deleted_filename}")
        delete_screenshot(deleted_filename)
    
    # Index new files
    new_files = [f for f in image_files if f.name not in existing_filenames]
    
    if not new_files:
        print("✅ All screenshots are already indexed")
        return
    
    print(f"🆕 Found {len(new_files)} new screenshots to index")
    
    for i, image_file in enumerate(new_files, 1):
        try:
            print(f"📸 [{i}/{len(new_files)}] Analyzing {image_file.name}...")
            
            # Analyze image with GPT-5
            metadata = analyze_image(str(image_file))
            
            # Add image dimensions to metadata
            with Image.open(image_file) as img:
                metadata['size'] = f"{img.width}x{img.height}"
                metadata['format'] = img.format.lower() if img.format else 'unknown'
            
            # Insert into database
            insert_screenshot(
                filename=image_file.name,
                filepath=str(image_file),
                metadata=metadata
            )
            
            print(f"✅ Indexed: {image_file.name}")
            
        except Exception as e:
            print(f"❌ Error indexing {image_file.name}: {str(e)}")
    
    print(f"🎉 Indexing complete! Total screenshots in database: {len(existing_screenshots) + len(new_files) - len(deleted_filenames)}")

