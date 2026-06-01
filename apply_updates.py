import os
import re

css_path = '/Volumes/A26/Portfolio Home/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Colors
css = css.replace('--accent-color: #ff0000;', '--accent-color: #c5a059;')
css = css.replace('--text-main: rgba(252, 248, 227, 0.85); /* Muutettu: 85% kirkkaus kaikelle perustekstille */', '--text-main: #d9d9d9;')
css = css.replace('#fcf8e3', '#f2f2f2')
css = css.replace('252, 248, 227', '242, 242, 242')
css = css.replace('var(--text-main: rgba(252, 248, 227, 0.85))', 'var(--text-main: #d9d9d9)') # just in case

# 2. Typography
css = css.replace('font-size: 32px; font-weight: 300; letter-spacing: 6px;', 'font-size: clamp(32px, 4vw, 48px); font-weight: 300; letter-spacing: 6px;')
css = css.replace('.contact-title { font-size: clamp(24px, 5vw, 32px);', '.contact-title { font-size: clamp(24px, 4vw, 40px);')

# 3. Mobile margins
if '@media (max-width: 1024px)' in css:
    # Add .image-section { margin-bottom: 80px; } inside the first media query
    css = css.replace('.intro-grid { grid-template-columns: 1fr; gap: 30px }', '.intro-grid { grid-template-columns: 1fr; gap: 30px }\n  .image-section { margin-bottom: 80px; }')

# 4. Fade-in for main
css = css + '\n\n/* Main Fade In */\nmain { animation: mainFadeIn 0.8s ease-out forwards; }\n@keyframes mainFadeIn { from { opacity: 0; } to { opacity: 1; } }\n'

# 5. Page Navigation spacing
css = css.replace('margin: 0 auto 100px auto;\n  padding: 40px 50px 0;', 'margin: 140px auto 100px auto;\n  padding: 40px 50px 0;')
css = css.replace('padding: 30px 20px 0;\n    margin-bottom: 60px;', 'margin-top: 80px;\n    margin-bottom: 60px;\n    padding: 30px 20px 0;')

# 6. Wave effect
css = css.replace('transform: translateX(10px); color: #f2f2f2;', 'transform: translateX(6px); color: #f2f2f2;')
css = css.replace('aside.trigger-wave nav a:nth-child(1)', '/* Slower stagger */\naside.trigger-wave nav a:nth-child(1)')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# Update default.html
html_path = '/Volumes/A26/Portfolio Home/_layouts/default.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add loader subtitle and style
loader_old = '<div id="loader"><h1>Aatu Alatalo</h1></div>'
loader_new = '''<div id="loader">
  <div style="display: flex; flex-direction: column; align-items: center;">
    <h1>Aatu Alatalo</h1>
    <p style="opacity: 0; animation: introSubtitle 1s ease 0.6s forwards; color: #c5a059; font-size: 11px; letter-spacing: 4px; text-transform: uppercase; margin-top: 10px; font-weight: 300; text-align: center;">Hasselblad Masters 2026 Finalist</p>
  </div>
</div>
<style>@keyframes introSubtitle { to { opacity: 0.8; } }</style>'''
html = html.replace(loader_old, loader_new)

# Add backdrop blur to mobile header menu open
html = html.replace("body.classList.toggle('menu-open');", "body.classList.toggle('menu-open');") # Keep as is, blur is already handled in css or can be added to css

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# Update page_nav.html
nav_path = '/Volumes/A26/Portfolio Home/_includes/page_nav.html'
nav_new = '''{% assign is_category = false %}
{% for cat in site.data.categories %}
  {% if cat.id == page.active_nav %}
    {% assign is_category = true %}
    {% assign current_index = forloop.index0 %}
  {% endif %}
{% endfor %}

{% if is_category %}
  {% assign prev_index = current_index | minus: 1 %}
  {% assign next_index = current_index | plus: 1 %}
  
  {% assign total_cats = site.data.categories.size %}
  
  {% if prev_index < 0 %}
    {% assign prev_index = total_cats | minus: 1 %}
  {% endif %}
  
  {% if next_index >= total_cats %}
    {% assign next_index = 0 %}
  {% endif %}

  {% assign prev_cat = site.data.categories[prev_index] %}
  {% assign next_cat = site.data.categories[next_index] %}

  <div class="page-navigation">
    {% if page.lang == 'en' %}
      <a href="{{ prev_cat.en_url }}" class="nav-prev"><span class="nav-arrow">&larr;</span> Previous</a>
      <a href="{{ next_cat.en_url }}" class="nav-next">Next <span class="nav-arrow">&rarr;</span></a>
    {% else %}
      <a href="{{ prev_cat.fi_url }}" class="nav-prev"><span class="nav-arrow">&larr;</span> Edellinen</a>
      <a href="{{ next_cat.fi_url }}" class="nav-next">Seuraava <span class="nav-arrow">&rarr;</span></a>
    {% endif %}
  </div>
{% endif %}'''

with open(nav_path, 'w', encoding='utf-8') as f:
    f.write(nav_new)

# Update About pages
about_fi = '/Volumes/A26/Portfolio Home/about.html'
with open(about_fi, 'r', encoding='utf-8') as f:
    afi = f.read()

cta_fi = '''

<div class="about-cta" style="margin-top: 100px; padding-top: 40px; border-top: 1px solid #1a1a1a; text-align: center;">
  <a href="/masters-2026.html" style="display: inline-block; color: #f2f2f2; text-decoration: none; font-size: 14px; letter-spacing: 3px; text-transform: uppercase; transition: color 0.3s ease;">
    Palaa galleriaan <span style="font-size: 18px; line-height: 1; vertical-align: middle; margin-left: 8px;">&rarr;</span>
  </a>
</div>
'''
if 'about-cta' not in afi:
    afi = afi.replace('</div>\n</div>\n', '</div>\n</div>\n' + cta_fi)
    with open(about_fi, 'w', encoding='utf-8') as f:
        f.write(afi)

about_en = '/Volumes/A26/Portfolio Home/en/about.html'
with open(about_en, 'r', encoding='utf-8') as f:
    aen = f.read()

cta_en = '''

<div class="about-cta" style="margin-top: 100px; padding-top: 40px; border-top: 1px solid #1a1a1a; text-align: center;">
  <a href="/en/masters-2026.html" style="display: inline-block; color: #f2f2f2; text-decoration: none; font-size: 14px; letter-spacing: 3px; text-transform: uppercase; transition: color 0.3s ease;">
    Explore Portfolio <span style="font-size: 18px; line-height: 1; vertical-align: middle; margin-left: 8px;">&rarr;</span>
  </a>
</div>
'''
if 'about-cta' not in aen:
    aen = aen.replace('</div>\n</div>\n', '</div>\n</div>\n' + cta_en)
    with open(about_en, 'w', encoding='utf-8') as f:
        f.write(aen)

print("Updates applied successfully.")
