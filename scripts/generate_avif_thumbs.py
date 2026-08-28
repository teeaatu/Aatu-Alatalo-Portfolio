#!/usr/bin/env python3
"""
generate_avif_thumbs.py
-----------------------
Kertaluontoinen skripti: generoi AVIF desktop-thumbit kaikille
Cloudflare R2:ssa oleville kuvamastereille.

Käyttö:
    python3 scripts/generate_avif_thumbs.py

Strategia:
  - Lataa jokaisen kuvan master WebP R2:sta muistiin
  - Skaalaa max 1600px (LANCZOS)
  - Enkoodaa AVIF quality 70
  - Lataa R2:een Photographs/thumbs/{nimi}_desktop.avif
  - Mobile thumbeja ei generoida (6% saasto ei riita)
"""

import os
import io
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

R2_ENDPOINT_URL      = os.environ.get('R2_ENDPOINT_URL')
R2_ACCESS_KEY_ID     = os.environ.get('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME       = os.environ.get('R2_BUCKET_NAME')

AVIF_QUALITY   = 70
DESKTOP_MAX_PX = 1600
MAX_WORKERS    = 4

def get_s3_client():
    import boto3
    return boto3.client(
        's3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name='auto'
    )

def list_masters(s3):
    paginator = s3.get_paginator('list_objects_v2')
    masters = []
    for page in paginator.paginate(Bucket=R2_BUCKET_NAME, Prefix='Photographs/'):
        for obj in page.get('Contents', []):
            key = obj['Key']
            if key.endswith('.webp') and 'thumbs/' not in key:
                name = key.replace('Photographs/', '').replace('.webp', '')
                masters.append(name)
    return sorted(masters)

def avif_already_exists(s3, name):
    try:
        s3.head_object(Bucket=R2_BUCKET_NAME,
                       Key=f'Photographs/thumbs/{name}_desktop.avif')
        return True
    except:
        return False

def process_one(name, idx, total, force=False):
    s3 = get_s3_client()
    avif_key = f'Photographs/thumbs/{name}_desktop.avif'

    if not force and avif_already_exists(s3, name):
        print(f"  [{idx}/{total}] skip  {name}")
        return name, None, None

    try:
        buf = io.BytesIO()
        s3.download_fileobj(R2_BUCKET_NAME, f'Photographs/{name}.webp', buf)
        buf.seek(0)
        img = Image.open(buf)
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')

        desktop = img.copy()
        desktop.thumbnail((DESKTOP_MAX_PX, DESKTOP_MAX_PX), Image.Resampling.LANCZOS)

        avif_buf = io.BytesIO()
        desktop.save(avif_buf, format='AVIF', quality=AVIF_QUALITY)
        avif_size_kb = len(avif_buf.getvalue()) / 1024
        avif_buf.seek(0)

        s3.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=avif_key,
            Body=avif_buf,
            ContentType='image/avif',
            CacheControl='public, max-age=31536000, immutable'
        )

        print(f"  [{idx}/{total}] OK  {name}: {avif_size_kb:.0f} KB")
        return name, avif_size_kb, True

    except Exception as e:
        print(f"  [{idx}/{total}] ERR {name}: {e}")
        return name, None, False

def main():
    force = '--force' in sys.argv
    print("=" * 60)
    print("AVIF Desktop Thumb Generator")
    print("=" * 60)

    s3 = get_s3_client()
    print("Haetaan master-lista R2:sta...")
    masters = list_masters(s3)
    total = len(masters)
    print(f"Loydetty {total} WebP-masteria\n")

    t_start = time.time()
    succeeded = []
    skipped   = []
    failed    = []
    total_size_kb = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(process_one, name, idx + 1, total, force): name
            for idx, name in enumerate(masters)
        }
        for future in as_completed(futures):
            name, size_kb, result = future.result()
            if result is True:
                succeeded.append(name)
                if size_kb:
                    total_size_kb += size_kb
            elif result is None:
                skipped.append(name)
            else:
                failed.append(name)

    elapsed = time.time() - t_start
    print("\n" + "=" * 60)
    print(f"Onnistui: {len(succeeded)}")
    print(f"Ohitettu: {len(skipped)}")
    print(f"Epaonnistui: {len(failed)}")
    if failed:
        for f in failed:
            print(f"  - {f}")
    print(f"Aika: {elapsed:.1f}s")
    print(f"AVIF-thumbeja yhteensa: {total_size_kb:.0f} KB")
    print("=" * 60)

if __name__ == '__main__':
    main()
