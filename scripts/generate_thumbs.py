import os
import io
import argparse
import boto3
from PIL import Image, ImageEnhance, ImageCms
from dotenv import load_dotenv

# Ladataan ympäristömuuttujat .env -tiedostosta
load_dotenv()

R2_ENDPOINT_URL = os.environ.get('R2_ENDPOINT_URL')
R2_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME')

def get_s3_client():
    """Alustaa boto3-yhteyden Cloudflare R2:een."""
    return boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name='auto'  # R2 käyttää yleensä 'auto' aluetta
    )

def convert_to_srgb(img):
    """
    Muuntaa kuvan sRGB-väriavaruuteen, jos siinä on sisäänrakennettu ICC-profiili (esim. Adobe RGB).
    Tämä on kriittistä, jotta värit toistuvat oikein selaimissa WebP-muodossa.
    """
    icc_profile = img.info.get('icc_profile')
    if icc_profile:
        try:
            io_handle = io.BytesIO(icc_profile)
            src_profile = ImageCms.ImageCmsProfile(io_handle)
            dst_profile = ImageCms.createProfile('sRGB')
            img = ImageCms.profileToProfile(img, src_profile, dst_profile)
        except Exception as e:
            print(f"  [Varoitus] ICC-profiilin muunnos epäonnistui: {e}")
    
    # Varmistetaan että kuva on RGB tai RGBA -tilassa WebP tallennusta varten
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
        
    return img

def process_image_variant(img, max_size):
    """Skaalaa, terävöittää ja palauttaa kuvan WebP-formaatissa tavuvirtana."""
    # Luodaan kopio, jotta alkuperäinen kuva muistissa ei ylikirjoitu seuraavaa varianttia varten
    img_variant = img.copy()
    
    # Skaalaus (aspect ratio säilyttäen) LANCZOS-algoritmilla
    img_variant.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    
    # Kevyt 15% lisäterävöitys (palauttaa linjojen selkeyttä skaalauksen jälkeen)
    enhancer = ImageEnhance.Sharpness(img_variant)
    img_variant = enhancer.enhance(1.15)
    
    # Pakkaus in-memory -puskuriin
    out_io = io.BytesIO()
    img_variant.save(out_io, format='WEBP', quality=82, method=6)
    out_io.seek(0)
    
    return out_io

def main():
    parser = argparse.ArgumentParser(description="Automatisoitu R2 dual-thumbnail kuvaputki.")
    parser.add_argument('--dry-run', action='store_true', help="Aja skripti testaustilassa ilman S3/R2 uploadia.")
    parser.add_argument('--prefix', default='Photographs/', help="Kansio/Prefix, josta alkuperäiset kuvat haetaan.")
    args = parser.parse_args()

    if not all([R2_ENDPOINT_URL, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET_NAME]):
        print("Virhe: S3/R2 ympäristömuuttujia puuttuu. Tarkista .env tiedosto.")
        return

    s3 = get_s3_client()
    paginator = s3.get_paginator('list_objects_v2')
    
    print(f"Skannataan bucketia: {R2_BUCKET_NAME} (Prefix: {args.prefix})...")
    pages = paginator.paginate(Bucket=R2_BUCKET_NAME, Prefix=args.prefix)
    
    all_objects = []
    for page in pages:
        if 'Contents' in page:
            all_objects.extend([obj['Key'] for obj in page['Contents']])
            
    master_images = []
    existing_thumbs = set()
    
    # Erotellaan masterit ja pikkukuvat
    for key in all_objects:
        if '/thumbs/' in key:
            existing_thumbs.add(key)
        elif key.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.webp')):
            master_images.append(key)
            
    # Generoidaan työjono
    process_queue = []
    for master_key in master_images:
        path_parts = master_key.rsplit('/', 1)
        if len(path_parts) == 2:
            base_dir, filename = path_parts
            thumb_dir = f"{base_dir}/thumbs/"
        else:
            filename = master_key
            thumb_dir = "thumbs/"
            
        name_no_ext = filename.rsplit('.', 1)[0]
        desktop_key = f"{thumb_dir}{name_no_ext}_desktop.webp"
        mobile_key = f"{thumb_dir}{name_no_ext}_mobile.webp"
        
        missing_variants = []
        if desktop_key not in existing_thumbs:
            missing_variants.append({'type': 'desktop', 'key': desktop_key, 'size': 1600})
        if mobile_key not in existing_thumbs:
            missing_variants.append({'type': 'mobile', 'key': mobile_key, 'size': 600})
            
        if missing_variants:
            process_queue.append({'master_key': master_key, 'variants': missing_variants})
            
    print(f"Löytyi {len(master_images)} alkuperäiskuvaa. Naistä {len(process_queue)} vaatii päivityksiä.")
    
    if args.dry_run:
        print("\n--- DRY RUN: Muutoksia ei tehdä ---\n")
        for item in process_queue:
            print(f"Päivitettävä kuva: {item['master_key']}")
            for v in item['variants']:
                print(f"  -> Uupuu: {v['key']} (Max {v['size']}px)")
        return
        
    # Prosessointivaihe
    print("\n--- ALOITETAAN PROSESSOINTI ---\n")
    created_count = 0
    
    for item in process_queue:
        master_key = item['master_key']
        print(f"Ladataan alkuperäinen: {master_key}...")
        
        try:
            response = s3.get_object(Bucket=R2_BUCKET_NAME, Key=master_key)
            image_bytes = response['Body'].read()
            
            img = Image.open(io.BytesIO(image_bytes))
            img = convert_to_srgb(img)
            
            for variant in item['variants']:
                print(f"  Luodaan {variant['type']} variantti ({variant['size']}px)...")
                webp_io = process_image_variant(img, variant['size'])
                
                # TURVALLISUUSMEKANISMI: Varmistetaan prefix-eristys
                if '/thumbs/' not in variant['key'] and not variant['key'].startswith('thumbs/'):
                    raise ValueError(f"Estetty ylikirjoitusyritys turvallisuussyistä. Key: {variant['key']}")
                
                print(f"  Upload: {variant['key']}")
                s3.put_object(
                    Bucket=R2_BUCKET_NAME,
                    Key=variant['key'],
                    Body=webp_io,
                    ContentType='image/webp'
                )
                created_count += 1
                
            # Vapautetaan muistia explicitly
            img.close()
            
        except Exception as e:
            print(f"Virhe käsiteltäessä kuvaa {master_key}: {e}")
            
    print(f"\nProsessointi valmis! Luotiin {created_count} uutta pikkukuvaa onnistuneesti.")

if __name__ == "__main__":
    main()