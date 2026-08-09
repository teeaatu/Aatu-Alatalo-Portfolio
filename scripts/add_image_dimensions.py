import os
import re
import urllib.request
import io
from PIL import Image

# Välimuisti kuvien mitoille
dim_cache = {}

def get_image_dimensions(img_val):
    if img_val in dim_cache:
        return dim_cache[img_val]
        
    if img_val.startswith('http://') or img_val.startswith('https://'):
        print(f"Haetaan etäkuvan mitat: {img_val}...")
        try:
            req = urllib.request.Request(img_val, headers={'User-Agent': 'AntigravityPerformanceOptimizer/1.0'})
            with urllib.request.urlopen(req, timeout=15) as response:
                img_data = response.read()
                with Image.open(io.BytesIO(img_data)) as img:
                    w, h = img.size
                    dim_cache[img_val] = (w, h)
                    print(f"  -> Mitat: {w}x{h}")
                    return w, h
        except Exception as e:
            print(f"Virhe haettaessa etäkuvaa {img_val}: {e}")
            return None, None
    else:
        # Paikallinen kuva
        local_path = os.path.join("assets/images", img_val)
        if os.path.exists(local_path):
            try:
                with Image.open(local_path) as img:
                    w, h = img.size
                    dim_cache[img_val] = (w, h)
                    return w, h
            except Exception as e:
                print(f"Virhe luettaessa paikallista kuvaa {local_path}: {e}")
                return None, None
        else:
            # Etsitään myös ilman polkua jos annettu suhteellisena
            base_name = os.path.basename(img_val)
            fallback_path = os.path.join("assets/images", base_name)
            if os.path.exists(fallback_path):
                try:
                    with Image.open(fallback_path) as img:
                        w, h = img.size
                        dim_cache[img_val] = (w, h)
                        return w, h
                except Exception as e:
                    pass
            print(f"Paikallista kuvaa ei löydy: {local_path}")
            return None, None

def update_yaml_file(filepath):
    print(f"\nPäivitetään tiedosto: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.splitlines()
    new_lines = []
    i = 0
    updated_count = 0
    
    while i < len(lines):
        line = lines[i]
        
        if line.strip().startswith('#'):
            new_lines.append(line)
            i += 1
            continue
            
        # Etsitään kuva-kenttää
        match = re.match(r'^(\s*)(-\s*)?kuva:\s*["\']?([^"\']+)["\']?', line)
        if match:
            indent_spaces = match.group(1)
            has_dash = match.group(2)
            img_val = match.group(3).strip()
            
            # Määritetään sisennyksen pituus
            if has_dash:
                indent = indent_spaces + '  '
            else:
                indent = indent_spaces
                
            width, height = get_image_dimensions(img_val)
            
            new_lines.append(line)
            if width and height:
                new_lines.append(f"{indent}width: {width}")
                new_lines.append(f"{indent}height: {height}")
                updated_count += 1
            else:
                # Jos mittoja ei saatu, säilytetään vanhat jos ne olivat olemassa
                pass
                
            # Ohitetaan mahdolliset vanhat leveys- ja korkeusrivit heti kuva-rivin alla
            i += 1
            while i < len(lines):
                next_line = lines[i]
                if re.match(r'^\s*(width|height):', next_line):
                    # Jos mittoja ei saatu, mutta tiedostossa oli jo mitat, pidetään ne
                    if not (width and height):
                        new_lines.append(next_line)
                    i += 1
                else:
                    break
            continue
        else:
            new_lines.append(line)
            i += 1
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines) + '\n')
        
    print(f"Tiedosto päivitetty! Lisätty/päivitetty {updated_count} kuvan mitat.")

def main():
    data_dir = "_data"
    if not os.path.exists(data_dir):
        print(f"Virhe: Kansiota {data_dir} ei löydy.")
        return
        
    # Päivitetään kaikki YML-tiedostot _data -kansiosta
    for filename in os.listdir(data_dir):
        if filename.endswith(('.yml', '.yaml')) and not filename.startswith('.'):
            # Ohitetaan categories.yml koska se sisältää vain kategoriatietoja ilman kuva-kenttiä
            if filename == 'categories.yml':
                continue
            update_yaml_file(os.path.join(data_dir, filename))

if __name__ == "__main__":
    main()
