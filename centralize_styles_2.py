import re
import os

with open("assets/css/style.css", "r") as f:
    content = f.read()

# Separate the file into the existing :root and the rest
root_match = re.search(r':root\s*\{([^}]*)\}', content)
if root_match:
    existing_root_content = root_match.group(1)
    # find existing variables in root
    existing_vars = re.findall(r'(--[a-zA-Z0-9-]+):\s*([^;]+);', existing_root_content)
    var_dict = {v.strip(): k for k, v in existing_vars}
else:
    existing_root_content = ""
    var_dict = {}

rest_of_content = content[root_match.end():] if root_match else content

new_vars = {}

def get_var_name_for_value(val):
    val = re.sub(r'\s+', ' ', val).strip()
    if val in var_dict:
        return f"var({var_dict[val]})"
    if val in new_vars:
        return f"var({new_vars[val]})"
    
    # Create new var
    if val.startswith('#'):
        var_name = f"--color-hex-{val[1:].lower()}"
    elif val.startswith('rgb'):
        var_name = f"--color-rgb-{len(new_vars)}"
    else:
        var_name = f"--font-{len(new_vars)}"
        
    new_vars[val] = var_name
    return f"var({var_name})"

def replacer(match):
    val = match.group(0)
    return get_var_name_for_value(val)

def font_replacer(match):
    prefix = match.group(1)
    val = match.group(2)
    return f"{prefix}{get_var_name_for_value(val)}"

rest_of_content = re.sub(r'#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b', replacer, rest_of_content)
rest_of_content = re.sub(r'rgba?\([^)]+\)', replacer, rest_of_content)
rest_of_content = re.sub(r'(font-family:\s*)([^;!}]+)', font_replacer, rest_of_content)

new_root_content = existing_root_content + "\n  /* Auto-centralized styles */\n"
for val, name in new_vars.items():
    new_root_content += f"  {name}: {val};\n"

final_content = content[:root_match.start()] + ":root {" + new_root_content + "}" + rest_of_content

with open("assets/css/style.css", "w") as f:
    f.write(final_content)

print(f"Added {len(new_vars)} variables.")
