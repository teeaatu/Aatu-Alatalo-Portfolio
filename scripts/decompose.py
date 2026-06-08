import os

base_dir = "/Volumes/A26/Portfolio Home"
default_html_path = os.path.join(base_dir, "_layouts/default.html")

with open(default_html_path, "r", encoding="utf-8") as f:
    content = f.read()

head_block = """  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <title>{{ page.title | default: "Aatu Alatalo | Valokuvaaja & Hasselblad Masters 2026 Finalist" }}</title>
  {% if page.lang == 'fi' %}
    {% assign main_desc = page.description_fi | default: page.description | default: 'Aatu Alatalo on oululainen valokuvaaja ja Hasselblad Masters 2026 -finalisti. Taiteellinen valokuvaportfolio: potretit, maisemat ja projektit. | Photographer and Hasselblad Masters Finalist.' %}
  {% else %}
    {% assign main_desc = page.description_en | default: page.description | default: 'Aatu Alatalo is an Oulu-based photographer and a Hasselblad Masters 2026 finalist. Artistic photography portfolio.' %}
  {% endif %}
  <meta name="description" content="{{ main_desc }}">
  <meta name="keywords" content="Aatu Alatalo, valokuvaaja Oulu, Hasselblad Masters 2026, Project 21, suomalainen valokuvaus, photography portfolio Finland">
  
  <meta property="og:title" content="{{ page.title | default: 'Aatu Alatalo | Photography Archive' }}">
  {% if page.lang == 'fi' %}
    {% assign og_desc = page.description_fi | default: page.description | default: 'Hasselblad Masters 2026 -finalisti - Tutustu Aatu Alatalon valokuva-arkistoon ja visuaaliseen matkaan.' %}
  {% else %}
    {% assign og_desc = page.description_en | default: page.description | default: 'Hasselblad Masters 2026 Finalist - Explore the visual journey and photographic archives of Aatu Alatalo.' %}
  {% endif %}
  <meta property="og:description" content="{{ og_desc }}">
  <meta property="og:image" content="{{ site.url }}{{ '/assets/images/PROJECT%2021%20FINALIST.jpg' | relative_url }}">
  <meta property="og:url" content="{{ site.url }}{{ page.url }}">
  <meta property="og:type" content="website">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{{ page.title | default: 'Aatu Alatalo | Photography Archive' }}">
  <meta name="twitter:description" content="{{ og_desc }}">
  <meta name="twitter:image" content="{{ site.url }}{{ '/assets/images/PROJECT%2021%20FINALIST.jpg' | relative_url }}">

  <link rel="canonical" href="{{ site.url }}{{ page.url | replace:'index.html','' }}">

  {% if page.url == '/' or page.url == '/index.html' or page.url == '/about.html' %}
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Aatu Alatalo",
    "jobTitle": "Photographer",
    "url": "https://aatualatalo.com",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "Oulu",
      "addressRegion": "North Ostrobothnia",
      "addressCountry": "FI"
    },
    "award": "Hasselblad Masters 2026 Finalist (Project//21)",
    "sameAs": [
      "https://www.instagram.com/teeaatu/"
    ]
  }
  </script>
  {% endif %}

  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', {
      'analytics_storage': 'denied'
    });
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-XNF1FLBJH6"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XNF1FLBJH6');
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="https://unpkg.com/photoswipe@5.4.3/dist/photoswipe.css">

  <link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}?v={{ site.time | date: '%s' }}">"""

loader_block = """<div id="loader">
  <div class="loader-content">
    <h1>Aatu Alatalo</h1>
    <p class="loader-subtitle">Hasselblad Masters 2026 Finalist</p>
  </div>
</div>"""

cookie_banner_block = """<div id="cookie-banner">
  <p>{{ site.data.t.cookie_text[lang] }}</p>
  <div class="cookie-buttons">
    <button class="cookie-btn accept" id="accept-cookies">{{ site.data.t.cookie_accept[lang] }}</button>
    <button class="cookie-btn" id="decline-cookies">{{ site.data.t.cookie_decline[lang] }}</button>
  </div>
</div>"""

mobile_header_block = """<header class="mobile-header" id="mobileHeader">
  <div class="lang-switcher-clean">
    <a href="{% if page.translation_url %}{{ page.translation_url }}{% else %}{% if page.lang == 'fi' %}/en/{% else %}/{% endif %}{% endif %}" class="{% if page.lang == 'fi' %}active{% endif %}">FI</a>
    <span class="separator">/</span>
    <a href="{% if page.translation_url %}{{ page.translation_url }}{% else %}{% if page.lang == 'en' %}/{% else %}/en/{% endif %}{% endif %}" class="{% if page.lang == 'en' %}active{% endif %}">EN</a>
  </div>
  <a href="{{ '/' | relative_url }}" class="mobile-logo no-decoration">Aatu Alatalo</a>
  <button class="menu-toggle" id="menuToggle" aria-label="Avaa valikko">
    <div class="hamburger"></div>
  </button>
</header>"""

sidebar_block = """<aside id="sidebar">
  <a href="{{ '/' | relative_url }}" class="logo no-decoration">Aatu<br>Alatalo</a>
  <nav>
    <a href="{% if page.lang == 'en' %}/en/{% else %}/{% endif %}" class="{% if page.active_nav == 'index' %}active{% endif %}">{{ site.data.t.overview[lang] }}</a>
    
    <a href="{% if page.lang == 'en' %}/en/masters-2026.html{% else %}/masters-2026.html{% endif %}" class="masters-nav-item {% if page.active_nav == 'masters-2026' %}active{% endif %}">
      Hasselblad Masters 2026
      <span>Finalist / Project//21</span>
    </a>

    <a href="{% if page.lang == 'en' %}/en/raw.html{% else %}/raw.html{% endif %}" class="{% if page.active_nav == 'raw' %}active{% endif %}">{{ site.data.t.portraits[lang] }}</a>
    <a href="{% if page.lang == 'en' %}/en/black-and-white-series.html{% else %}/mustavalkoinen-sarja.html{% endif %}" class="{% if page.active_nav == 'mustavalkoinen-sarja' %}active{% endif %}">{{ site.data.t.monochrome[lang] }}</a>
    <a href="{% if page.lang == 'en' %}/en/interior-light.html{% else %}/sisatilan-valo.html{% endif %}" class="{% if page.active_nav == 'sisatilan-valo' %}active{% endif %}">{{ site.data.t.interior[lang] }}</a>
    <a href="{% if page.lang == 'en' %}/en/buildings.html{% else %}/kiehtovat-rakennukset.html{% endif %}" class="{% if page.active_nav == 'kiehtovat-rakennukset' %}active{% endif %}">{{ site.data.t.buildings[lang] }}</a>
    <a href="{% if page.lang == 'en' %}/en/nature.html{% else %}/luonto-ja-ymparisto.html{% endif %}" class="{% if page.active_nav == 'luonto-ja-ymparisto' %}active{% endif %}">{{ site.data.t.nature[lang] }}</a>
    <a href="{% if page.lang == 'en' %}/en/still-life.html{% else %}/still-life.html{% endif %}" class="{% if page.active_nav == 'still-life' %}active{% endif %}">{{ site.data.t.still_life[lang] }}</a>
    <a href="{% if page.lang == 'en' %}/en/animals.html{% else %}/elaimet.html{% endif %}" class="{% if page.active_nav == 'elaimet' %}active{% endif %}">{{ site.data.t.animals[lang] }}</a>
    <a href="{% if page.lang == 'en' %}/en/color-and-form.html{% else %}/vari-ja-muoto.html{% endif %}" class="{% if page.active_nav == 'vari-ja-muoto' %}active{% endif %}">{{ site.data.t.color_and_form[lang] }}</a>
    <a href="{% if page.lang == 'en' %}/en/photo-project-time-v365.html{% else %}/kuvaprojekti-ajasta-v365.html{% endif %}" class="{% if page.active_nav == 'kuvaprojekti-ajasta-v365' %}active{% endif %}">{{ site.data.t.v365[lang] }}</a>
  </nav>

  <div class="info-nav">
    <nav class="info-nav-links">
      <a href="{% if page.lang == 'en' %}/en/about.html{% else %}/about.html{% endif %}" class="{% if page.active_nav == 'about' %}active{% endif %}">{{ site.data.t.about[lang] }}</a>
      <a href="#contact" id="contactBtn">{{ site.data.t.contact[lang] }}</a>
    </nav>
    <div class="lang-switcher-clean desktop-lang-switcher">
      <a href="{% if page.translation_url %}{{ page.translation_url }}{% else %}{% if page.lang == 'fi' %}/en/{% else %}/{% endif %}{% endif %}" class="{% if page.lang == 'fi' %}active{% endif %}">FI</a>
      <span class="separator">/</span>
      <a href="{% if page.translation_url %}{{ page.translation_url }}{% else %}{% if page.lang == 'en' %}/{% else %}/en/{% endif %}{% endif %}" class="{% if page.lang == 'en' %}active{% endif %}">EN</a>
    </div>
  </div>

</aside>"""

footer_block = """<footer class="contact-section" id="contact">
    <div class="contact-wrapper">
        <div class="contact-title">Contact</div>
        <div class="contact-info">
          <p>Aatu Alatalo</p>
          <p><a href="mailto:info@aatualatalo.com">info@aatualatalo.com</a></p>
          <p>Oulu, Finland</p>
          <p class="copyright">COPYRIGHT 2026 AATU ALATALO</p>
        </div>
    </div>
  </footer>"""

back_to_top_block = """<button class="back-to-top" id="backToTop" aria-label="Takaisin ylös">
    <svg viewBox="0 0 55 55">
        <circle class="progress-bg" cx="27.5" cy="27.5" r="25"></circle>
        <circle class="progress-bar" id="progressBar" cx="27.5" cy="27.5" r="25"></circle>
    </svg>
    &uarr;
</button>"""

replacements = [
    (head_block, "  {% include head.html %}", "head.html"),
    (loader_block, "{% include loader.html %}", "loader.html"),
    (cookie_banner_block, "{% include cookie-banner.html %}", "cookie-banner.html"),
    (mobile_header_block, "{% include mobile-header.html %}", "mobile-header.html"),
    (sidebar_block, "{% include sidebar.html %}", "sidebar.html"),
    (footer_block, "{% include footer.html %}", "footer.html"),
    (back_to_top_block, "{% include back-to-top.html %}", "back-to-top.html")
]

successes = 0
for old_str, new_str, filename in replacements:
    if old_str in content:
        content = content.replace(old_str, new_str)
        # Check if _includes directory exists
        includes_dir = os.path.join(base_dir, "_includes")
        if not os.path.exists(includes_dir):
            os.makedirs(includes_dir)
        with open(os.path.join(includes_dir, filename), "w", encoding="utf-8") as inc:
            inc.write(old_str.strip() + "\\n")
        successes += 1
        print(f"Successfully decomposed {filename}")
    else:
        print(f"Could not find block for {filename} in _layouts/default.html")

if successes > 0:
    with open(default_html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated default.html with {successes} replacements.")
else:
    print("No blocks matched.")
