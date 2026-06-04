import re

css_path = '/Volumes/A26/Portfolio Home/assets/css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace View Transitions logic
old_vt = '''/* --- VIEW TRANSITIONS API --- */
@view-transition {
  navigation: auto;
}
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.5s;
}'''

new_vt = '''/* --- VIEW TRANSITIONS API --- */
@view-transition {
  navigation: auto;
}
::view-transition-old(root) {
  animation: 0.3s cubic-bezier(0.4, 0, 1, 1) both fade-out;
}
::view-transition-new(root) {
  animation: 0.5s cubic-bezier(0, 0, 0.2, 1) 0.1s both fade-in,
             0.5s cubic-bezier(0.22, 1, 0.36, 1) 0.1s both slide-up;
}

@keyframes fade-out { to { opacity: 0; } }
@keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
@keyframes slide-up { from { transform: translateY(15px); } to { transform: translateY(0); } }'''

if old_vt in css:
    css = css.replace(old_vt, new_vt)


# Replace Main Fade In
old_fade = '''/* Main Fade In */
main { animation: mainFadeIn 0.8s ease-out forwards; }
@keyframes mainFadeIn { from { opacity: 0; } to { opacity: 1; } }'''

new_fade = '''/* Main Fade In */
main { animation: mainFadeIn 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards; }
@keyframes mainFadeIn { 
  from { opacity: 0; transform: translateY(15px); } 
  to { opacity: 1; transform: translateY(0); } 
}'''

if old_fade in css:
    css = css.replace(old_fade, new_fade)


with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Transitions updated!")
