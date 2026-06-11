import os
import glob
import yaml
import requests
import re
from io import BytesIO
from PIL import Image
import boto3
from dotenv import load_dotenv

# Määritetään projektin juurikansio ja etsitään .env sieltä
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, '.env')

if os.path.exists(env_path):
    print(f"🔍 Löydettiin .env tiedosto: {env_path}")
    with open(env_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        if r'{\rtf' in content:
            print("⚠️ .env on tallennettu RTF-muodossa. Yritetään purkaa avaimet koodin seasta automaattisesti...")
            keys = ['R2_ENDPOINT_URL', 'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY', 'R2_BUCKET_NAME']
            for key in keys:
                # Etsitään avain=arvo -pari. Pysähtyy Macin RTF-kenoviivoihin tai väleihin.
                match = re.search(key + r"\s*=\s*([^\\\s{}]+)", content)
                if match:
                    os.environ[key] = match.group(1)
        else:
            load_dotenv(env_path)
else:
    print(f"⚠️ VAROITUS: .env tiedostoa ei löytynyt juuresta: {env_path}")
    load_dotenv()

MAX_WIDTH = 1000
DATA_DIR = '_data'
LOCAL_IMG_DIR = 'assets/images'
LOCAL_THUMB_DIR = 'assets/thumbnails'

# R2 Konfiguraatio (Haetaan .env tiedostosta)
R2_ENDPOINT_URL = os.getenv('R2_ENDPOINT_URL') 
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')

if not R2_ACCESS_KEY_ID or not R2_SECRET_ACCESS_KEY:
    print("\n⚠️ R2 API-avaimia ei löytynyt .env -tiedostosta (tai tiedosto on väärässä muodossa)!")
    print("Kysytään avaimet nyt ja luodaan puhdas .env -tiedosto automaattisesti.\n")
    
    R2_ENDPOINT_URL = input("1. Syötä R2 Endpoint URL (alkaa https://): ").strip()
    R2_ACCESS_KEY_ID = input("2. Syötä R2 Access Key ID: ").strip()
    R2_SECRET_ACCESS_KEY = input("3. Syötä R2 Secret Access Key: ").strip()
    R2_BUCKET_NAME = input("4. Syötä ämpärin nimi (esim. portfolio-media): ").strip()
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(f"R2_ENDPOINT_URL={R2_ENDPOINT_URL}\n")
        f.write(f"R2_ACCESS_KEY_ID={R2_ACCESS_KEY_ID}\n")
        f.write(f"R2_SECRET_ACCESS_KEY={R2_SECRET_ACCESS_KEY}\n")
        f.write(f"R2_BUCKET_NAME={R2_BUCKET_NAME}\n")
    
    print(f"\n✅ Puhdas .env tiedosto tallennettu onnistuneesti!")

if R2_ENDPOINT_URL and R2_ACCESS_KEY_ID:
    print("✅ R2 API-avaimet ladattu onnistuneesti!")
else:
    print("❌ R2 API-avaimia EI löydetty! Tarkista .env tiedoston sisältö.")

os.makedirs(LOCAL_THUMB_DIR, exist_ok=True)

# Yhdistetään Cloudflare R2:een, jos avaimet on annettu
s3 = None
if R2_ENDPOINT_URL and R2_ACCESS_KEY_ID:
    s3 = boto3.client('s3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name='auto'
    )

def process_image(img_path):
    if not img_path: return
    
    try:
        is_cloud = "http" in img_path
        
        if is_cloud:
            if not s3:
                print(f"⚠️ Sivuutetaan R2-kuva, API-avaimia ei määritetty: {img_path}")
                return
                
            filename = img_path.split('/')[-1]
            base_name = os.path.splitext(filename)[0]
            webp_filename = f"{base_name}.webp"
            r2_upload_key = f"thumbs/{webp_filename}" # Tallennetaan R2:n thumbs-kansioon
            
            # Tarkistetaan onko pikkukuva jo R2:ssa
            try:
                s3.head_object(Bucket=R2_BUCKET_NAME, Key=r2_upload_key)
                print(f"✅ R2 Pikkukuva jo olemassa: {webp_filename}")
                return
            except:
                pass
                
            print(f"☁️ Ladataan R2-kuva pienennettäväksi: {filename}")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(img_path, headers=headers)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
            else:
                print(f"❌ Kuvan lataus epäonnistui: {img_path}")
                return
        else:
            filename = os.path.basename(img_path)
            base_name = os.path.splitext(filename)[0]
            webp_filename = f"{base_name}.webp"
            local_thumb_path = os.path.join(LOCAL_THUMB_DIR, webp_filename)
            
            if os.path.exists(local_thumb_path):
                print(f"✅ Paikallinen pikkukuva jo olemassa: {webp_filename}")
                return
                
            local_img_path = os.path.join(LOCAL_IMG_DIR, filename)
            if not os.path.exists(local_img_path):
                print(f"❌ Kuvaa ei löydy koneelta: {local_img_path}")
                return
                
            print(f"🖥️ Pienennetään paikallinen kuva: {filename}")
            img = Image.open(local_img_path)

        # Pienennys (Käännetään värit oikein ja skaalataan nätisti)
        if img.mode in ("RGBA", "P", "CMYK"):
            img = img.convert("RGB")
        if img.width > MAX_WIDTH:
            new_height = int(img.height * (MAX_WIDTH / img.width))
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
            
        if is_cloud:
            output_io = BytesIO()
            img.save(output_io, "WEBP", quality=85)
            output_io.seek(0)
            s3.upload_fileobj(output_io, R2_BUCKET_NAME, r2_upload_key, ExtraArgs={'ContentType': 'image/webp'})
            print(f"🚀 Pikkukuva tallennettu R2-pilveen: {r2_upload_key}")
        else:
            img.save(local_thumb_path, "WEBP", quality=85)
            print(f"💾 Paikallinen pikkukuva tallennettu: {local_thumb_path}")
    except Exception as e:
        print(f"❌ Virhe käsitellessä kuvaa '{img_path}': {e}")

yaml_files = glob.glob(os.path.join(DATA_DIR, '*.yml'))
for filepath in yaml_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = yaml.safe_load(f)
            # Varmistetaan että kyseessä on lista (kuten kuvagalleriat on), ohitetaan kielikäännökset
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        if item.get('layout') == 'diptych' and 'images' in item:
                            for img_item in item['images']:
                                if isinstance(img_item, dict):
                                    process_image(img_item.get('kuva'))
                        else: 
                            process_image(item.get('kuva'))
        except Exception as e:
            print(f"⚠️ Ohitetaan tiedosto {filepath}: ei validi kuvalista ({e})")