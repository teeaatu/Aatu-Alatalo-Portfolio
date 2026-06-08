import os
import re

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
}

loop_template = """    {{% for item in site.data['{dataset}'] %}}
    {{% if item.alt_text != blank %}}
      {{% assign alt_content = item.alt_text %}}
    {{% else %}}
      {{% comment %}} Fallback: Clean up the filename to use as alt text {{% endcomment %}}
      {{% assign filename = item.kuva | split: '/' | last | split: '.' | first %}}
      {{% assign alt_content = filename | replace: '-', ' ' | replace: '_', ' ' | capitalize %}}
    {{% endif %}}
    <section class="image-section" data-series="{{% if item.series %}}{{{{ item.series }}}}{{% else %}}general{{% endif %}}">
        <div class="image-wrapper">
            <img {{% if item.kuva contains 'http' %}}src="{{{{ item.kuva }}}}"{{% else %}}src="/assets/images/{{{{ item.kuva }}}}"{{% endif %}} alt="{{{{ alt_content }}}}" class="gallery-img" {{% if forloop.first %}}loading="eager" fetchpriority="high"{{% else %}}loading="lazy"{{% endif %}}>
            <div class="project-info">
                <p>{{% if page.lang == 'en' %}}{{{{ item.otsikko | split: ' / ' | first }}}}{{% else %}}{{{{ item.otsikko | split: ' / ' | last }}}}{{% endif %}}</p>
                <p>{{{{ item.paikka }}}}</p>
            </div>
        </div>
    </section>
    {{% endfor %}}"""

for html_file, dataset in html_to_yml.items():
    if not os.path.exists(html_file):
        print(f"Skipping {html_file}, not found.")
        continue
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace all <section class="image-section">...</section> that are adjacent or separated by whitespace.
    # Wait, some pages have other <section>s? Only image-section.
    
    # Find all <section class="image-section"> blocks
    pattern = re.compile(r'(<section class="image-section".*?</section>\s*)+', re.DOTALL)
    
    def replacer(match):
        return loop_template.format(dataset=dataset) + '\n'
    
    new_content, num_subs = pattern.subn(replacer, content)
    
    # Check if Potret.html needs front matter
    if html_file == 'Potret.html' and not new_content.startswith('---'):
        new_content = "---\nlayout: null\n---\n" + new_content

    if num_subs > 0:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {html_file}")
    else:
        print(f"No match found in {html_file}")
