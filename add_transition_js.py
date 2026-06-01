import re

html_path = '/Volumes/A26/Portfolio Home/_layouts/default.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add overlay div right after body
if 'id="pageTransitionOverlay"' not in html:
    html = html.replace('<body id="body" class="{% if page.active_nav == \'index\' %}index-page{% endif %}">', 
                        '<body id="body" class="{% if page.active_nav == \'index\' %}index-page{% endif %}">\n\n<div class="page-transition-overlay is-active" id="pageTransitionOverlay"></div>')

# Add JS logic before </body>
js_code = """
  // --- CROSS-BROWSER PAGE TRANSITION ---
  const transitionOverlay = document.getElementById('pageTransitionOverlay');
  if (transitionOverlay) {
    window.addEventListener('pageshow', (e) => {
      // Small delay to ensure render
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          transitionOverlay.classList.add('is-leaving');
          transitionOverlay.classList.remove('is-active');
          setTimeout(() => {
            transitionOverlay.classList.remove('is-leaving');
          }, 600);
        });
      });
    });

    document.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', function(e) {
        if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
        
        const href = this.getAttribute('href');
        // Exclude anchors, mailto, tel, target_blank and data-fancybox/photoswipe elements
        if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:') || this.getAttribute('target') === '_blank' || this.classList.contains('gallery-img')) {
          return;
        }

        const isLocal = this.hostname === window.location.hostname;
        if (isLocal) {
          e.preventDefault();
          transitionOverlay.classList.add('is-entering');
          setTimeout(() => {
            window.location.href = href;
          }, 500); // Navigate slightly before animation finishes for smoother feel
        }
      });
    });
  }
</script>
</body>
"""

if 'CROSS-BROWSER PAGE TRANSITION' not in html:
    html = html.replace('</script>\n</body>', js_code)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("JS added to default.html.")
