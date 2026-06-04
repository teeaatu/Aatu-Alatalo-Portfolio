import re

css_path = '/Volumes/A26/Portfolio Home/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Make sure View Transitions API is removed
css = re.sub(r'/\* --- VIEW TRANSITIONS API --- \*/[\s\S]*?@keyframes slide-up \{ [^\}]+\}', '', css)

# Make sure old fade in is removed
css = re.sub(r'/\* Main Fade In \*/[\s\S]*?@keyframes mainFadeIn \{ [^\}]+\}', '', css)

# Append the new custom transition styles
new_css = """
/* --- CROSS-BROWSER PAGE TRANSITION OVERLAY --- */
.page-transition-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: var(--bg-color);
  z-index: 99999;
  pointer-events: none;
  transform: translateY(100%);
  transition: transform 0.6s cubic-bezier(0.85, 0, 0.15, 1);
}

.page-transition-overlay.is-active {
  transform: translateY(0);
}

.page-transition-overlay.is-leaving {
  transform: translateY(-100%);
}

/* Base fade for main content */
main {
  opacity: 0;
  animation: contentFadeIn 0.8s ease-out 0.3s forwards;
}

@keyframes contentFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
"""

if "CROSS-BROWSER PAGE TRANSITION OVERLAY" not in css:
    css += new_css

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS added.")
