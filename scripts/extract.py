import os
import re

html_dir = "/Volumes/A26/Portfolio Home"
data_dir = os.path.join(html_dir, "_data")

os.makedirs(data_dir, exist_ok=True)

pattern = re.compile(
    r'<img[^>]*?src=["\']/assets/images/([^"\']+)["\'][^>]*?>\s*'
    r'<div\s+class=["\']project-info["\']>\s*'
    r'<p>(.*?)</p>\s*'
    r'<p>(.*?)</p>',
    re.DOTALL | re.IGNORECASE
)

processed_files = []

for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(html_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Could not read {filename}: {e}")
            continue
        
        matches = pattern.findall(content)
        if matches:
            yaml_filename = filename.replace(".html", ".yml")
            yaml_filepath = os.path.join(data_dir, yaml_filename)
            
            with open(yaml_filepath, 'w', encoding='utf-8') as yf:
                for match in matches:
                    kuva = match[0].strip()
                    otsikko = match[1].strip()
                    paikka = match[2].strip()
                    
                    yf.write(f"- kuva: {kuva}\n")
                    yf.write(f"  otsikko: {otsikko}\n")
                    yf.write(f"  paikka: {paikka}\n")
            
            processed_files.append(filename)

print(f"Processed files: {', '.join(processed_files)}")
