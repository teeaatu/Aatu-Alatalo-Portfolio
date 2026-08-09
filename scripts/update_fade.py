html_path = '/Volumes/A26/Portfolio Home/_layouts/default.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace timeout 600 -> 400
html = html.replace("setTimeout(() => {\n            transitionOverlay.classList.remove('is-leaving');\n          }, 600);",
                    "setTimeout(() => {\n            transitionOverlay.classList.remove('is-leaving');\n          }, 400);")

# Replace timeout 500 -> 200
html = html.replace("setTimeout(() => {\n            window.location.href = href;\n          }, 500);",
                    "setTimeout(() => {\n            window.location.href = href;\n          }, 200);")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

css_path = '/Volumes/A26/Portfolio Home/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

import re
css = re.sub(r'/\* --- CROSS-BROWSER PAGE TRANSITION OVERLAY --- \*/[\s\S]*$', '', css)

new_css = """/* --- CROSS-BROWSER PAGE TRANSITION OVERLAY --- */
.page-transition-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: var(--bg-color);
  z-index: 99999;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s ease-out;
}

.page-transition-overlay.is-active {
  opacity: 1;
}

.page-transition-overlay.is-leaving {
  opacity: 0;
  transition: opacity 0.4s ease-in;
}

/* Base fade for main content */
main {
  opacity: 0;
  animation: contentFadeIn 0.5s ease-out 0.1s forwards;
}

@keyframes contentFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.page-transition-overlay.is-entering {
  opacity: 1;
}
"""

css += new_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Fade transition updated.")
