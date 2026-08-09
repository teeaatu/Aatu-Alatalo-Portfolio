import os
import re
import argparse

html_to_yml = {
    'vari-ja-muoto.html': 'vari-ja-muoto',
    'en/color-and-form.html': 'vari-ja-muoto',
    'luonto-ja-ymparisto.html': 'luonto-ja-ymparisto',
    'en/nature.html': 'luonto-ja-ymparisto',
    'masters-2026.html': 'masters-2026',
    'en/masters-2026.html': 'masters-2026',
    'mustavalkoinen-sarja.html': 'mustavalkoinen-sarja',
    'en/black-and-white-series.html': 'mustavalkoinen-sarja',
    'raw.html': 'raw',
    'en/raw.html': 'raw',
    'sisatilan-valo.html': 'sisatilan-valo',
    'en/interior-light.html': 'sisatilan-valo',
    'Potret.html': 'Potret',
    'en/portraits.html': 'Potret',
    'elaimet.html': 'elaimet',
    'en/animals.html': 'elaimet',
    'kiehtovat-rakennukset.html': 'kiehtovat-rakennukset',
    'en/buildings.html': 'kiehtovat-rakennukset',
    'still-life.html': 'still-life',
    'en/still-life.html': 'still-life',
    'kuvaprojekti-ajasta-v365.html': 'kuvaprojekti_ajasta_v365',
    'en/photo-project-time-v365.html': 'kuvaprojekti_ajasta_v365'
}

loop_template = """    {{% for item in site.data['{dataset}'] %}}
        {{% if forloop.index <= 2 %}}
            {{% assign is_lazy = false %}}
        {{% else %}}
            {{% assign is_lazy = true %}}
        {{% endif %}}
        {{% include category-item.html item=item lazy_load=is_lazy %}}
    {{% endfor %}}"""

def replace_liquid_loop(content, dataset, new_loop_str):
    """
    Etsii dynaamisesti oikean Liquid-luupin huomioiden sisäkkäiset {% for %} ja {% endfor %} -tagit.
    Tämä estää esimerkiksi layout- tai sub-luuppien rikkoutumisen vahingossa.
    """
    start_pattern = r'\{%\s*for\s+item\s+in\s+site\.data(?:\[[\'"]' + re.escape(dataset) + r'[\'"]\]|\.' + re.escape(dataset) + r')\s*%\}'
    start_match = re.search(start_pattern, content)
    
    if not start_match:
        return content, 0
        
    start_idx = start_match.start()
    depth = 0
    tag_pattern = re.compile(r'\{%\s*(for|endfor)\b[^%]*%\}')
    
    pos = start_idx
    while True:
        match = tag_pattern.search(content, pos)
        if not match:
            break
        
        tag_type = match.group(1)
        if tag_type == 'for':
            depth += 1
        elif tag_type == 'endfor':
            depth -= 1
            
        pos = match.end()
        
        if depth == 0:
            end_idx = match.end()
            new_content = content[:start_idx] + new_loop_str + content[end_idx:]
            return new_content, 1
            
    return content, 0

def main():
    parser = argparse.ArgumentParser(description="Päivittää kategoriat käyttämään uutta category-item.html komponenttia.")
    parser.add_argument('--dry-run', action='store_true', help="Näytä vain tiedostot joita päivitettäisiin, tallentamatta muutoksia.")
    args = parser.parse_args()

    for html_file, dataset in html_to_yml.items():
        if not os.path.exists(html_file):
            print(f"[OHITETTU] Tiedostoa ei löydy: {html_file}")
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_loop = loop_template.format(dataset=dataset)
        new_content, num_subs = replace_liquid_loop(content, dataset, new_loop)
        
        if num_subs > 0:
            if args.dry_run:
                print(f"[DRY-RUN] Päivitettäisiin luuppi tiedostossa: {html_file}")
            else:
                if content.startswith('---') and not new_content.startswith('---'):
                    print(f"[VIRHE] Front matter katosi tiedostosta {html_file}. Ohitetaan turvallisuussyistä.")
                    continue
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"[PÄIVITETTY] Tiedosto: {html_file}")
        else:
            print(f"[EI MUUTOKSIA] Oikeaa luuppia ei löytynyt: {html_file}")

if __name__ == "__main__":
    main()
