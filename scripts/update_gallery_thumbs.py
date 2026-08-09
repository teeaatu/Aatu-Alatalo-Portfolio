import os
import glob
import json
import base64
from io import BytesIO
from PIL import Image, ImageFilter

# --- ASETUKSET ---
SOURCE_DIR = 'assets/images'
THUMB_DIR = 'assets/thumbnails'
DATA_DIR = '_data'
LQIP_FILE = os.path.join(DATA_DIR, 'lqip.json')

# Mobiiliversion parametrit
MOBILE_WIDTH = 800
MOBILE_QUALITY = 70

# Työpöytäversion parametrit (Crisp Retina)
DESKTOP_WIDTH = 1600
DESKTOP_QUALITY = 75

# LQIP (Base64) parametrit
LQIP_WIDTH = 20
LQIP_QUALITY = 40

# Ladataan olemassa oleva LQIP-data (jottei ylikirjoiteta kuvia joita ei ehkä juuri nyt prosessoida)
lqip_data = {}
if os.path.exists(LQIP_FILE):
    try:
        with open(LQIP_FILE, 'r', encoding='utf-8') as f:
            lqip_data = json.load(f)
    except Exception as e:
        print(f"Varoitus: Ei voitu lukea vanhaa lqip.json -tiedostoa: {e}")

def process_image(filepath):
    filename = os.path.basename(filepath)
    base_name = os.path.splitext(filename)[0]
    
    mobile_path = os.path.join(THUMB_DIR, f"{base_name}_mobile.webp")
    desktop_path = os.path.join(THUMB_DIR, f"{base_name}_desktop.webp")
    
    # Tarkistetaan onko LQIP olemassa
    has_lqip = base_name in lqip_data
    
    if os.path.exists(mobile_path) and os.path.exists(desktop_path) and has_lqip:
        print(f"Ohitetaan {filename} - Pikkukuvat ja LQIP on jo luotu.")
        return

    try:
        with Image.open(filepath) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # ==========================================
            # 1. MOBIILIVERSIO (_mobile.webp)
            # ==========================================
            if not os.path.exists(mobile_path):
                if img.width > MOBILE_WIDTH:
                    m_height = int((MOBILE_WIDTH / img.width) * img.height)
                    img_mobile = img.resize((MOBILE_WIDTH, m_height), Image.Resampling.LANCZOS)
                else:
                    img_mobile = img.copy()
                img_mobile.save(mobile_path, 'webp', quality=MOBILE_QUALITY, method=6)
            
            # ==========================================
            # 2. TYÖPÖYTÄVERSIO (_desktop.webp)
            # ==========================================
            if not os.path.exists(desktop_path):
                if img.width > DESKTOP_WIDTH:
                    d_height = int((DESKTOP_WIDTH / img.width) * img.height)
                    img_desktop = img.resize((DESKTOP_WIDTH, d_height), Image.Resampling.LANCZOS)
                else:
                    img_desktop = img.copy()
                img_desktop = img_desktop.filter(ImageFilter.UnsharpMask(radius=1.2, percent=70, threshold=3))
                img_desktop.save(desktop_path, 'webp', quality=DESKTOP_QUALITY, method=6)
                
            # ==========================================
            # 3. LQIP BASE64 MIKROKUVA
            # ==========================================
            if not has_lqip:
                lqip_height = int((LQIP_WIDTH / img.width) * img.height)
                img_lqip = img.resize((LQIP_WIDTH, max(1, lqip_height)), Image.Resampling.LANCZOS)
                
                buffered = BytesIO()
                img_lqip.save(buffered, format="JPEG", quality=LQIP_QUALITY)
                img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                
                # Tallennetaan datarakenteeseen
                lqip_data[base_name] = f"data:image/jpeg;base64,{img_str}"
            
            print(f"✓ Prosessoitu: {filename} -> _mobile, _desktop, LQIP")

    except Exception as e:
        print(f"✗ Virhe prosessoitaessa kuvaa {filename}: {e}")

def main():
    print("====================================================")
    print("Aloitetaan kuvien prosessointi (Mobiili, Desktop & LQIP)...")
    print("====================================================")
    
    os.makedirs(THUMB_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    
    extensions = ('*.jpg', '*.jpeg', '*.png', '*.webp')
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(SOURCE_DIR, ext)))
        files.extend(glob.glob(os.path.join(SOURCE_DIR, ext.upper())))
        
    if not files:
        print(f"Ei löydetty alkuperäisiä kuvia kansiosta {SOURCE_DIR}.")
        return
        
    for filepath in files:
        process_image(filepath)
        
    # Tallennetaan päivitetty LQIP-sanakirja json-tiedostoon
    with open(LQIP_FILE, 'w', encoding='utf-8') as f:
        json.dump(lqip_data, f, ensure_ascii=False, indent=2)
        
    print(f"Kaikki kuvat prosessoitu! LQIP-data tallennettu tiedostoon: {LQIP_FILE}")

if __name__ == "__main__":
    main()