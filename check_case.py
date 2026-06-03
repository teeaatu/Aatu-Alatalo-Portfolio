import os, glob
import yaml

image_dir = 'assets/images'
actual_files = os.listdir(image_dir)
missing = []

for filepath in glob.glob('_data/*.yml'):
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
            if not isinstance(data, list):
                continue
            for item in data:
                if 'kuva' in item:
                    img = item['kuva']
                    if img not in actual_files:
                        missing.append(f"{filepath}: {img}")
                if 'images' in item:
                    for sub in item['images']:
                        if 'kuva' in sub:
                            img = sub['kuva']
                            if img not in actual_files:
                                missing.append(f"{filepath} (nested): {img}")
        except Exception as e:
            pass

for m in missing:
    print(m)
