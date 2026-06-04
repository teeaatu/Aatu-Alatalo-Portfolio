import os
import glob
import re

missing = []
image_dir = 'assets/images'
data_dir = '_data'

# Check _data/*.yml
for filepath in glob.glob('_data/*.yml'):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            match = re.search(r'kuva:\s*"?([^"\n\r]+)"?', line)
            if match:
                img = match.group(1).strip()
                img_path = os.path.join(image_dir, img)
                if not os.path.exists(img_path):
                    missing.append(f"{filepath} [Line {i}]: {img_path}")

# Check HTML files
for filepath in glob.glob('**/*.html', recursive=True):
    if filepath.startswith('_site/') or filepath.startswith('vendor/'):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            # Check src="..."
            src_matches = re.findall(r'src=["\']([^"\']+)["\']', line)
            for m in src_matches:
                if m.startswith('http') or m.startswith('//') or '{{' in m:
                    continue
                rel_path = m.lstrip('/')
                if not os.path.exists(rel_path):
                    missing.append(f"{filepath} [Line {i}]: {m} (not found as {rel_path})")

            # Check href="..."
            href_matches = re.findall(r'href=["\']([^"\']+)["\']', line)
            for m in href_matches:
                if m.startswith('http') or m.startswith('//') or '{{' in m or m.startswith('#'):
                    continue
                rel_path = m.lstrip('/')
                # we only care about images for now, or missing html? The prompt says "missing media assets, and incorrect image path references... broken relative links"
                # let's report all broken links
                if not os.path.exists(rel_path) and not os.path.exists(rel_path + '.html') and not rel_path == "":
                    missing.append(f"{filepath} [Line {i}]: {m} (not found as {rel_path})")

# Check markdown files
for filepath in glob.glob('**/*.md', recursive=True):
    if filepath.startswith('_site/') or filepath.startswith('vendor/'):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            matches = re.findall(r'!\[.*?\]\((.*?)\)', line)
            for m in matches:
                if m.startswith('http') or m.startswith('//') or '{{' in m:
                    continue
                rel_path = m.lstrip('/')
                if not os.path.exists(rel_path):
                    missing.append(f"{filepath} [Line {i}]: {m} (not found as {rel_path})")

if missing:
    for m in missing:
        print(m)
else:
    print("No missing links or assets found.")
