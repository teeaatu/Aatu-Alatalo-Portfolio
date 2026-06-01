import re

css_path = '/Volumes/A26/Portfolio Home/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Fix the broken line left over by the greedy regex
css = css.replace(' to { transform: translateY(0); } }\n\n/* --- STAGGERED LOAD ANIMATION --- */', '\n/* --- STAGGERED LOAD ANIMATION --- */')

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS syntax fixed.")
