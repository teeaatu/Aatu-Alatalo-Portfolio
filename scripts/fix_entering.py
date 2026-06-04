import re

css_path = '/Volumes/A26/Portfolio Home/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Add missing is-entering
if '.page-transition-overlay.is-entering' not in css:
    css += '\n.page-transition-overlay.is-entering {\n  transform: translateY(0);\n}\n'

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS is-entering added.")
