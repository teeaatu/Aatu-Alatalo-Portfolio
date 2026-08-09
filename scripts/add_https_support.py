import os
import glob

base_dir = '/Volumes/A26/Portfolio Home'

# Etsi HTML-tiedostot juuresta, en-kansiosta ja _includes-kansiosta (etusivun ruudukkoa varten)
html_files = (
    glob.glob(os.path.join(base_dir, '*.html')) + 
    glob.glob(os.path.join(base_dir, 'en', '*.html')) +
    glob.glob(os.path.join(base_dir, '_includes', '*.html'))
)

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    old_item = 'src="/assets/images/{{ item.kuva }}"'
    new_item = '{% if item.kuva contains "http" %}src="{{ item.kuva }}"{% else %}src="/assets/images/{{ item.kuva }}"{% endif %}'
    
    old_img_item = 'src="/assets/images/{{ img_item.kuva }}"'
    new_img_item = '{% if img_item.kuva contains "http" %}src="{{ img_item.kuva }}"{% else %}src="/assets/images/{{ img_item.kuva }}"{% endif %}'

    updated_content = content.replace(old_item, new_item).replace(old_img_item, new_img_item)

    if content != updated_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Päivitetty: {os.path.relpath(filepath, base_dir)}")

print("Kaikki galleriat tukevat nyt https-osoitteita!")