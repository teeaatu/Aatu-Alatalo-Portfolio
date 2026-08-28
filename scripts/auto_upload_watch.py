#!/usr/bin/env python3
"""
Portfolio Auto-Uploader & Drop Folder Watcher
---------------------------------------------
1. Seuraa kansiota ~/Pictures/Portfolio-Uploads (tai käsittelee annetun tiedoston)
2. Muuntaa Capture One JPEG:in täydellisellä sRGB-värintoistolla WebP-muotoon
3. Lisää erittäin hienovaraisen 15% terävöityksen (enhance(1.15))
4. Tallentaa paikallisen .webp-tiedoston tarkastelua varten
5. Luo automaattisesti desktop & mobile pikkukuvat (thumbs)
6. Lataa master- ja pikkukuvat Cloudflare R2 -bucketiin
7. Kopioi valmiin R2-osoitteen suoraan Macin leikepöydälle (Cmd+V)
8. Lähettää Mac-ilmoituksen ruudulle
"""

import os
import io
import sys
import time
import subprocess
import argparse
from pathlib import Path
from PIL import Image, ImageEnhance, ImageCms
from dotenv import load_dotenv

# Etsitään .env tiedosto projektin juuresta
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

R2_ENDPOINT_URL = os.environ.get('R2_ENDPOINT_URL')
R2_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME')
PUBLIC_CDN_BASE = "https://media.aatualatalo.com/Photographs"

DEFAULT_WATCH_DIR = PROJECT_ROOT / "Portfolio-Uploads"
ORIGINALS_DIR = DEFAULT_WATCH_DIR / "originals"

def get_s3_client():
    import boto3
    return boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name='auto'
    )

def convert_to_srgb(img):
    """Säilyttää värit oikeina muuntamalla sRGB-avaruuteen."""
    icc_profile = img.info.get('icc_profile')
    if icc_profile:
        try:
            io_handle = io.BytesIO(icc_profile)
            src_profile = ImageCms.ImageCmsProfile(io_handle)
            dst_profile = ImageCms.createProfile('sRGB')
            img = ImageCms.profileToProfile(img, src_profile, dst_profile)
        except Exception as e:
            print(f"  [Varoitus] ICC-muunnos: {e}")
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
    return img

def copy_to_clipboard(text):
    """Kopioi tekstin Macin leikepöydälle (pbcopy)."""
    try:
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE, close_fds=True)
        p.communicate(input=text.encode('utf-8'))
    except Exception as e:
        print(f"  [Virhe] Leikepöydälle kopiointi epäonnistui: {e}")

def send_notification(title, subtitle, message):
    """Näyttää natiivin macOS-ilmoituksen."""
    try:
        apple_script = f'''display notification "{message}" with title "{title}" subtitle "{subtitle}" sound name "Glass"'''
        subprocess.run(['osascript', '-e', apple_script], check=False)
    except Exception:
        pass

def process_and_upload(file_path: Path, s3=None):
    if not file_path.exists() or file_path.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.tif', '.tiff'):
        return None

    if s3 is None:
        s3 = get_s3_client()

    base_name = file_path.stem
    print(f"\n📸 Käsitellään kuva: {file_path.name}")

    # 1. Avataan ja muunnetaan värit
    with Image.open(file_path) as raw_img:
        img = convert_to_srgb(raw_img)
        width, height = img.size

        # 2. Hienovarainen 15% terävöitys
        enhancer = ImageEnhance.Sharpness(img)
        sharpened_img = enhancer.enhance(1.15)

        # 3. Älykäs WebP-tallennus (tavoiteikkuna 200–500 KB, dynaaminen laadunhaku)
        master_webp_path = file_path.parent / f"{base_name}.webp"
        
        best_data = None
        best_quality = 94
        best_size_kb = 0
        
        # Etsitään optimaalinen laatu väliltä 96 -> 76
        for q in range(96, 74, -2):
            buf = io.BytesIO()
            sharpened_img.save(buf, format='WEBP', quality=q, method=6)
            size_kb = len(buf.getvalue()) / 1024
            
            # Jos koko mahtuu max 500 KB rajaan
            if size_kb <= 500:
                best_data = buf.getvalue()
                best_quality = q
                best_size_kb = size_kb
                # Jos koko on vähintään 200 KB tai ollaan jo huippulaadussa, tämä on paras mahdollinen laatu
                if size_kb >= 200 or q >= 94:
                    break
                    
        if best_data:
            with open(master_webp_path, 'wb') as f_out:
                f_out.write(best_data)
            print(f"  ✓ Paikallinen WebP luotu: {master_webp_path.name} ({width}x{height}px, {int(best_size_kb)} KB, laatu {best_quality})")

        # 4. Generoidaan pikkukuvat muistiin
        # Desktop thumb (max 1600px, korkealuokkainen laatu 88 ilman porrastumista)
        desktop_img = sharpened_img.copy()
        desktop_img.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        desktop_io = io.BytesIO()
        desktop_img.save(desktop_io, format='WEBP', quality=88, method=6)
        desktop_io.seek(0)

        # Desktop AVIF thumb (sama resoluutio 1600px, quality 70 — ~26% pienempi kuin WebP)
        desktop_avif_io = io.BytesIO()
        desktop_img.save(desktop_avif_io, format='AVIF', quality=70)
        desktop_avif_io.seek(0)

        # Mobile thumb (max 600px, laatu 82) — vain WebP, AVIF ei tuo merkittavaa hyotya
        mobile_img = sharpened_img.copy()
        mobile_img.thumbnail((600, 600), Image.Resampling.LANCZOS)
        mobile_io = io.BytesIO()
        mobile_img.save(mobile_io, format='WEBP', quality=82, method=6)
        mobile_io.seek(0)

    # 5. Ladataan Cloudflare R2:een
    print("  🚀 Ladataan Cloudflare R2:een...")
    master_r2_key        = f"Photographs/{base_name}.webp"
    desktop_r2_key       = f"Photographs/thumbs/{base_name}_desktop.webp"
    desktop_avif_r2_key  = f"Photographs/thumbs/{base_name}_desktop.avif"
    mobile_r2_key        = f"Photographs/thumbs/{base_name}_mobile.webp"

    # Master
    with open(master_webp_path, 'rb') as f:
        s3.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=master_r2_key,
            Body=f,
            ContentType='image/webp'
        )

    # Thumbs
    s3.put_object(Bucket=R2_BUCKET_NAME, Key=desktop_r2_key,      Body=desktop_io,      ContentType='image/webp')
    s3.put_object(Bucket=R2_BUCKET_NAME, Key=desktop_avif_r2_key, Body=desktop_avif_io, ContentType='image/avif',
                  CacheControl='public, max-age=31536000, immutable')
    s3.put_object(Bucket=R2_BUCKET_NAME, Key=mobile_r2_key,       Body=mobile_io,       ContentType='image/webp')

    cdn_url = f"{PUBLIC_CDN_BASE}/{base_name}.webp"
    print(f"  ✨ Valmis! R2 URL: {cdn_url}")

    # 6. Kopioidaan URL leikepöydälle ja ilmoitetaan
    copy_to_clipboard(cdn_url)
    send_notification("Portfolio Uploader", "Kuva valmis & ladattu!", f"R2-linkki kopioitu leikepöydälle ({base_name}.webp)")

    # 7. Siirretään alkuperäinen JPG talteen originals-kansioon
    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)
    dest_original = ORIGINALS_DIR / file_path.name
    # Jos samanniminen jo on, lisätään aikaleima
    if dest_original.exists():
        dest_original = ORIGINALS_DIR / f"{base_name}_{int(time.time())}{file_path.suffix}"
    file_path.rename(dest_original)
    print(f"  📁 Alkuperäinen siirretty: originals/{dest_original.name}")

    return {
        'url': cdn_url,
        'width': width,
        'height': height,
        'local_webp': str(master_webp_path)
    }

def watch_folder(watch_dir: Path):
    watch_dir.mkdir(parents=True, exist_ok=True)
    ORIGINALS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"==================================================")
    print(f"👁️  Portfolio Drop-Folder Vahti käynnissä!")
    print(f"📂 Seurataan kansiota: {watch_dir}")
    print(f"💡 Tallenna tai pudota JPEG Capture Onesta tähän kansioon.")
    print(f"==================================================")

    s3 = get_s3_client()

    # Seuranta-silmukka
    seen = set()
    while True:
        try:
            for item in watch_dir.iterdir():
                if item.is_file() and item.suffix.lower() in ('.jpg', '.jpeg', '.png', '.tif', '.tiff'):
                    if item.name.startswith('.') or item.name in seen:
                        continue
                    
                    # Odotetaan pieni hetki että tiedoston kirjoitus (Capture One export) on valmis
                    initial_size = -1
                    while True:
                        try:
                            cur_size = item.stat().st_size
                            if cur_size == initial_size and cur_size > 0:
                                break
                            initial_size = cur_size
                            time.sleep(0.5)
                        except FileNotFoundError:
                            break

                    process_and_upload(item, s3)
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nVahti pysäytetty.")
            break
        except Exception as e:
            print(f"Virhe vahtisilmukassa: {e}")
            time.sleep(2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Portfolio Auto-Uploader & Drop Folder Watcher")
    parser.add_argument('file', nargs='?', help="Yksittäinen kuvatiedosto prosessoitavaksi")
    parser.add_argument('--watch', action='store_true', help="Käynnistä jatkuva kansionseuranta")
    parser.add_argument('--dir', default=str(DEFAULT_WATCH_DIR), help="Seurattava kansio")
    args = parser.parse_args()

    if args.file:
        target = Path(args.file).resolve()
        process_and_upload(target)
    else:
        watch_folder(Path(args.dir))
