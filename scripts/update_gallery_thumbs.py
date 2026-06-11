import os
import glob

base_dir = '/Volumes/A26/Portfolio Home'

# Etsi kaikki HTML-tiedostot juuresta ja en-kansiosta
html_files = glob.glob(os.path.join(base_dir, '*.html')) + glob.glob(os.path.join(base_dir, 'en', '*.html'))

liquid_logic = """    {% assign filename_no_ext = item.kuva | split: '/' | last | split: '.' | first %}
    {% assign thumb_filename = filename_no_ext | append: '.webp' %}
    {% if item.kuva contains 'http' %}
      {% assign p_thumb = item.kuva | split: '/' | slice: 0, 3 | join: '/' | append: '/thumbs/' | append: thumb_filename %}
      {% assign full_img_url = item.kuva %}
    {% else %}
      {% assign p_thumb = '/assets/thumbnails/' | append: thumb_filename %}
      {% assign full_img_url = '/assets/images/' | append: item.kuva %}
    {% endif %}
    <section class="image-section\""""

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tarkistetaan onko tiedostossa normaali gallerialooppi ja ettei sitä ole vielä päivitetty
    if '<section class="image-section"' in content and '{% for item in site.data' in content and '{% assign thumb_filename' not in content:
        
        # Lisätään Liquid-logiikka juuri ennen <section> tagia
        content = content.replace('    <section class="image-section"', liquid_logic)
        
        # Vaihdetaan img-tagi lataamaan pikkukuva, mutta säästetään iso kuva Lightboxille
        old_img_1 = '<img {% if item.kuva contains \'http\' %}src="{{ item.kuva }}"{% else %}src="/assets/images/{{ item.kuva }}"{% endif %}'
        old_img_2 = '<img {% if item.kuva contains "http" %}src="{{ item.kuva }}"{% else %}src="/assets/images/{{ item.kuva }}"{% endif %}'
        new_img = '<img src="{{ p_thumb }}" data-pswp-src="{{ full_img_url }}" onerror="this.onerror=null;this.src=\'{{ full_img_url }}\';"'
        
        content = content.replace(old_img_1, new_img).replace(old_img_2, new_img)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Päivitetty galleria: {os.path.relpath(filepath, base_dir)}")

print("Kaikki yksittäiset galleriasivut tukevat nyt pikkukuvia!")