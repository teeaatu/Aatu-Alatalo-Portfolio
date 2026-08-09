import os
from PIL import Image, ImageDraw

def create_abstract_favicon():
    # Piirretään todella isona (2048x2048) ja skaalataan pieneksi, 
    # jotta saadaan pehmeät (anti-aliasoidut) reunat vektoreille.
    render_size = 2048
    size = 512
    
    # Base canvas
    base = Image.new('RGBA', (render_size, render_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    
    # Colors from the lockscreen
    color_red = "#D8141F"
    color_green = "#0A8540"
    color_yellow = "#F4C509"
    color_black = "#080808"

    # Background (Punainen, vihreä, musta diagonaaleja)
    # Tausta on punainen
    draw.rectangle([(0, 0), (render_size, render_size)], fill=color_red)
    
    # Musta diagonaali vasemmalta alhaalta ylös keskelle
    draw.polygon([(0, render_size), (render_size//2, 0), (0, 0)], fill=color_black)
    
    # Vihreä diagonaali oikealta ylhäältä alas vasemmalle
    draw.polygon([(render_size, 0), (render_size, render_size), (render_size//3, render_size)], fill=color_green)
    
    # Keltainen kolmio oikeaan alakulmaan
    draw.polygon([(render_size, render_size//2), (render_size, render_size), (render_size//1.5, render_size)], fill=color_yellow)

    # Kuvassa esiintyvä ikoninen kaksivärinen ympyrä keskelle hieman vasemmalle
    cx = int(render_size * 0.45)
    cy = int(render_size * 0.55)
    r = int(render_size * 0.3) # Säde

    # Ympyrän keltainen yläosa
    draw.chord([(cx - r, cy - r), (cx + r, cy + r)], 180, 360, fill=color_yellow)
    
    # Ympyrän vihreä alaosa
    draw.chord([(cx - r, cy - r), (cx + r, cy + r)], 0, 180, fill=color_green)
    
    # Musta raja ympyrän puolikkaiden väliin korostamaan designia
    draw.line([(cx - r, cy), (cx + r, cy)], fill=color_black, width=int(render_size*0.01))

    # Downscale for anti-aliasing
    base = base.resize((size, size), Image.Resampling.LANCZOS)
    
    # Luo pyöristetty maski (macOS-tyylinen squircle, säde 22.5%)
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    radius = int(size * 0.225)
    mask_draw.rounded_rectangle([(0,0), (size, size)], radius=radius, fill=255)
    
    # Lopullinen favicon-pohja (transparent)
    final_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    final_img.paste(base, (0, 0), mask)

    # Tallenna alkuperäiset (png ja ico) projektin kansioon
    final_img.save("assets/images/favicon-192x192.png", format="PNG", optimize=True)
    final_img.save("assets/images/favicon-512x512.png", format="PNG", optimize=True)
    
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    final_img.save("favicon.ico", format="ICO", sizes=icon_sizes)

    # Tallenna preview suoraan Gemini artifacts-kansioon, jotta voin näyttää sen käyttäjälle
    final_img.save("/Users/teeaatu/.gemini/antigravity-ide/brain/e1fa8744-8471-422e-8ca0-7b45b17977ba/abstract-favicon-preview.png", format="PNG")
    print("Abstrakti favicon luotu onnistuneesti!")

if __name__ == '__main__':
    create_abstract_favicon()
