import re

with open('_layouts/default.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace main description
old_main = """<meta name="description" content="{{ page.description | default: 'Aatu Alatalo on oululainen valokuvaaja ja Hasselblad Masters 2026 -finalisti. Taiteellinen valokuvaportfolio: potretit, maisemat ja projektit. | Photographer and Hasselblad Masters Finalist.' }}">"""
new_main = """{% if page.lang == 'fi' %}
    {% assign main_desc = page.description_fi | default: page.description | default: 'Aatu Alatalo on oululainen valokuvaaja ja Hasselblad Masters 2026 -finalisti. Taiteellinen valokuvaportfolio: potretit, maisemat ja projektit. | Photographer and Hasselblad Masters Finalist.' %}
  {% else %}
    {% assign main_desc = page.description_en | default: page.description | default: 'Aatu Alatalo is an Oulu-based photographer and a Hasselblad Masters 2026 finalist. Artistic photography portfolio.' %}
  {% endif %}
  <meta name="description" content="{{ main_desc }}">"""

content = content.replace(old_main, new_main)

# Replace og:description and twitter:description
old_og = """<meta property="og:description" content="{{ page.description | default: 'Hasselblad Masters 2026 Finalist - Explore the visual journey and photographic archives of Aatu Alatalo.' }}">"""
new_og = """{% if page.lang == 'fi' %}
    {% assign og_desc = page.description_fi | default: page.description | default: 'Hasselblad Masters 2026 -finalisti - Tutustu Aatu Alatalon valokuva-arkistoon ja visuaaliseen matkaan.' %}
  {% else %}
    {% assign og_desc = page.description_en | default: page.description | default: 'Hasselblad Masters 2026 Finalist - Explore the visual journey and photographic archives of Aatu Alatalo.' %}
  {% endif %}
  <meta property="og:description" content="{{ og_desc }}">"""

content = content.replace(old_og, new_og)

old_twitter = """<meta name="twitter:description" content="{{ page.description | default: 'Hasselblad Masters 2026 Finalist - Explore the visual journey and photographic archives of Aatu Alatalo.' }}">"""
new_twitter = """<meta name="twitter:description" content="{{ og_desc }}">"""

content = content.replace(old_twitter, new_twitter)

with open('_layouts/default.html', 'w', encoding='utf-8') as f:
    f.write(content)
