import os
import re

pairs = {
    'elaimet.html': 'animals.html',
    'kiehtovat-rakennukset.html': 'buildings.html',
    'kuvaprojekti-ajasta-v365.html': 'photo-project-time-v365.html',
    'luonto-ja-ymparisto.html': 'nature.html',
    'masters-2026.html': 'masters-2026.html',
    'mustavalkoinen-sarja.html': 'black-and-white-series.html',
    'raw.html': 'raw.html',
    'sisatilan-valo.html': 'interior-light.html',
    'still-life.html': 'still-life.html',
    'vari-ja-muoto.html': 'color-and-form.html',
    'index.html': 'index.html',
}

def get_desc(path):
    if not os.path.exists(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    m = re.search(r'^description:\s*(.*?)$', content, re.MULTILINE)
    return m.group(1) if m else None

for fi_file, en_file in pairs.items():
    fi_path = fi_file
    en_path = f'en/{en_file}'
    
    desc_fi = get_desc(fi_path)
    desc_en = get_desc(en_path)
    
    if not desc_fi and not desc_en:
        continue
        
    print(f"Updating {fi_file} and {en_path}")
    
    for path in [fi_path, en_path]:
        if not os.path.exists(path): continue
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_lines = []
        for line in content.split('\n'):
            if line.startswith('description:'):
                if desc_fi:
                    new_lines.append(f'description_fi: {desc_fi}')
                if desc_en:
                    new_lines.append(f'description_en: {desc_en}')
            else:
                new_lines.append(line)
                
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

