import os
import glob
from PIL import Image, ImageFilter

# --- ASETUKSET ---
SOURCE_DIR = 'assets/images'
THUMB_DIR = 'assets/thumbnails'

# Mobiiliversion parametrit
MOBILE_WIDTH = 800
MOBILE_QUALITY = 75

# Työpöytäversion parametrit (Crisp Retina)
DESKTOP_WIDTH = 1600
DESKTOP_QUALITY = 85

def process_image(filepath):
    filename = os.path.basename(filepath)
    base_name = os.path.splitext(filename)[0]
    
    mobile_path = os.path.join(THUMB_DIR, f"{base_name}_mobile.webp")
    desktop_path = os.path.join(THUMB_DIR, f"{base_name}_desktop.webp")
    
    # Jos molemmat pikkukuvat ovat jo olemassa, voidaan ohittaa päivityksen nopeuttamiseksi.
    # (Poista nämä kaksi riviä, jos haluat pakottaa kaikkien kuvien uudelleengeneroinnin)
    if os.path.exists(mobile_path) and os.path.exists(desktop_path):
        print(f"Ohitetaan {filename} - Pikkukuvat on jo luotu.")
        return

    try:
        with Image.open(filepath) as img:
            # Muunnetaan RGB-muotoon vääristymien estämiseksi WebP-pakkauksessa
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # ==========================================
            # 1. MOBIILIVERSIO (_mobile.webp)
            # ==========================================
            if img.width > MOBILE_WIDTH:
                m_height = int((MOBILE_WIDTH / img.width) * img.height)
                img_mobile = img.resize((MOBILE_WIDTH, m_height), Image.Resampling.LANCZOS)
            else:
                img_mobile = img.copy()
                
            img_mobile.save(mobile_path, 'webp', quality=MOBILE_QUALITY, method=6)
            
            # ==========================================
            # 2. TYÖPÖYTÄVERSIO (_desktop.webp)
            # ==========================================
            if img.width > DESKTOP_WIDTH:
                d_height = int((DESKTOP_WIDTH / img.width) * img.height)
                img_desktop = img.resize((DESKTOP_WIDTH, d_height), Image.Resampling.LANCZOS)
            else:
                img_desktop = img.copy()
                
            # Kevyt Unsharp Mask -terävöitys isoille näytöille
            # Takaa "crisp" ulkoasun laimentamatta värejä
            img_desktop = img_desktop.filter(ImageFilter.UnsharpMask(radius=1.2, percent=70, threshold=3))
            
            img_desktop.save(desktop_path, 'webp', quality=DESKTOP_QUALITY, method=6)
            
            print(f"✓ Prosessoitu: {filename} -> _mobile ja _desktop")
            
            # ==========================================
            # 3. CLOUDFLARE R2 API SYNKRONOINTI (Valinnainen)
            # ==========================================
            # Jos siirrät kuvat suoraan Pythonilla R2-pilveen, voit tehdä sen tässä:
            # upload_to_r2(mobile_path, f"thumbs/{base_name}_mobile.webp")
            # upload_to_r2(desktop_path, f"thumbs/{base_name}_desktop.webp")

    except Exception as e:
        print(f"✗ Virhe prosessoitaessa kuvaa {filename}: {e}")

def main():
    print("====================================================")
    print("Aloitetaan Dual-Thumbnail prosessointi (Mobiili & Desktop)...")
    print("====================================================")
    
    os.makedirs(THUMB_DIR, exist_ok=True)
    
    # Etsitään alkuperäiset kuvat
    extensions = ('*.jpg', '*.jpeg', '*.png', '*.webp')
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(SOURCE_DIR, ext)))
        files.extend(glob.glob(os.path.join(SOURCE_DIR, ext.upper()))) # Huomioi myös isot tiedostopäätteet
        
    if not files:
        print(f"Ei löydetty alkuperäisiä kuvia kansiosta {SOURCE_DIR}.")
        return
        
    for filepath in files:
        process_image(filepath)
        
    print("Kaikki kuvat prosessoitu onnistuneesti!")

if __name__ == "__main__":
    main()