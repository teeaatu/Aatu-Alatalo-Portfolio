import os
import re

base_dir = '/Volumes/A26/Portfolio Home'

mappings = {
    'about.html': 'about.html',
    'index.html': 'index.html',
    'elaimet.html': 'animals.html',
    'kiehtovat-rakennukset.html': 'buildings.html',
    'kirjaston-ihmeet.html': 'library-wonders.html',
    'kuvaprojekti-ajasta-v365.html': 'photo-project-time-v365.html',
    'luonto-ja-ymparisto.html': 'nature.html',
    'masters-2026.html': 'masters-2026.html',
    'mustavalkoinen-sarja.html': 'black-and-white-series.html',
    'Potret.html': 'portraits.html',
    'raw.html': 'raw.html',
    'sisatilan-valo.html': 'interior-light.html',
    'still-life.html': 'still-life.html'
}

def update_file(filepath, trans_url):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'translation_url:' in content:
        content = re.sub(r'translation_url:.*?\n', f'translation_url: {trans_url}\n', content)
    else:
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = parts[1].rstrip() + f'\ntranslation_url: {trans_url}\n'
            content = f"---{front_matter}---{parts[2]}"
        else:
            print(f"No front matter found in {filepath}")
            return
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath} with {trans_url}")

for fi_file, en_file in mappings.items():
    fi_path = os.path.join(base_dir, fi_file)
    en_path = os.path.join(base_dir, 'en', en_file)
    
    update_file(fi_path, f"/en/{en_file}")
    update_file(en_path, f"/{fi_file}")
