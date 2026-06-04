import re
import os

with open("assets/css/style.css", "r") as f:
    content = f.read()

# Define the variables to add
variables = {}
counter = 1

def add_var(value, prefix):
    global counter
    # Normalize spaces in rgba
    value = re.sub(r'\s+', ' ', value).strip()
    
    # Check if we already have this value
    for var_name, var_value in variables.items():
        if var_value == value:
            return f"var({var_name})"
            
    # Existing variables in :root block we should not duplicate
    # We will just generate new ones for unhandled ones
    var_name = f"--{prefix}-{counter}"
    variables[var_name] = value
    counter += 1
    return f"var({var_name})"

# Don't touch existing :root block for extraction
root_match = re.search(r':root\s*{([^}]*)}', content)
existing_root = root_match.group(1) if root_match else ""

# Pre-defined variables to not replace if they are exactly the same maybe?
# Actually, the task is to convert ALL hardcoded hex/RGB colors and fonts into global CSS variables.
# It is fine if we just extract all hex/rgba/rgb/fonts, create variables for them, and inject them into :root.
# Let's just use regex to replace inline hex, rgb, rgba, and font-family.

def color_replacer(match):
    val = match.group(0)
    # Don't replace if it's already a var
    return add_var(val, "color")

def font_replacer(match):
    val = match.group(1)
    return f"font-family: {add_var(val, 'font')}"

# Temporary replace existing var(...) so we don't touch them
var_store = {}
def hide_var(match):
    k = f"__VAR_{len(var_store)}__"
    var_store[k] = match.group(0)
    return k

content = re.sub(r'var\([^)]+\)', hide_var, content)

# Now find hex colors. # followed by 3, 4, 6, or 8 hex digits. 
# Lookaround to ensure it's not part of a URL or something
content = re.sub(r'#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b', color_replacer, content)

# Find rgb/rgba
content = re.sub(r'rgba?\([^)]+\)', color_replacer, content)

# Find font-family
content = re.sub(r'font-family:\s*([^;!}]+)', font_replacer, content)

# Restore vars
for k, v in var_store.items():
    content = content.replace(k, v)

# Now, we need to inject the new variables into the :root block
new_vars_str = "\n".join([f"  {k}: {v};" for k, v in variables.items()])

if root_match:
    new_root = f":root {{{existing_root}\n  /* Auto-generated variables */\n{new_vars_str}\n}}"
    content = content.replace(root_match.group(0), new_root)
else:
    content = f":root {{\n{new_vars_str}\n}}\n\n" + content

with open("assets/css/style.css.new", "w") as f:
    f.write(content)

print(f"Added {len(variables)} variables.")
