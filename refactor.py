import os
from bs4 import BeautifulSoup

directory = '/Volumes/A26/Portfolio Home/'
files_to_process = [
    'index.html',
    'raw.html',
    'mustavalkoinen-sarja.html',
    'sisatilan-valo.html',
    'kiehtovat-rakennukset.html',
    'luonto-ja-ymparisto.html',
    'still-life.html',
    'elaimet.html',
    'kirjaston-ihmeet.html',
    'kuvaprojekti-ajasta-v365.html',
    'masters-2026.html',
    'about.html'
]

for filename in files_to_process:
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Extract title
    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else ''
    title = title.replace('"', '\\"') # escape quotes
    
    # 2. Extract meta description
    meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = meta_desc_tag['content'].strip() if meta_desc_tag and 'content' in meta_desc_tag.attrs else ''
    description = description.replace('"', '\\"') # escape quotes
    
    # 3. Extract unique content
    main_tag = soup.find('main')
    if not main_tag:
        print(f"No <main> tag found in {filename}")
        continue
        
    # Remove mobile-header
    mobile_headers = main_tag.find_all('div', class_='mobile-header')
    for mh in mobile_headers:
        mh.decompose()
        
    # Remove footer
    footers = main_tag.find_all('footer', class_='contact-section')
    for ft in footers:
        ft.decompose()
        
    # Extract inner HTML of main
    unique_content = "".join([str(child) for child in main_tag.contents]).strip()
    
    # 4. Replace content
    active_nav = filename.rsplit('.', 1)[0]
    
    front_matter = f"""---
layout: default
title: "{title}"
description: "{description}"
active_nav: "{active_nav}"
---

{unique_content}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        
    print(f"Processed {filename}")
