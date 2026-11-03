"""
NASA Space Apps 2026 - Trend Detective: Bengal Water Paradox
CSR GRACE / GRACE-FO RL06.3 Mascon Downloader

Automates downloading of CSR GRACE/GRACE-FO Mascon NetCDF solutions
from official UT-CSR mirrors.
"""

import os
import sys
import argparse
import urllib.request
import ssl
from pathlib import Path

PRIMARY_URL = "https://download.csr.utexas.edu/outgoing/grace/RL0603_mascons/CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc"
TARGET_FILENAME = "CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc"

def download_grace_mascons(output_path: str = TARGET_FILENAME):
    print(f"Connecting to CSR GRACE Mascon distribution mirror...")
    print(f"URL: {PRIMARY_URL}")
    print(f"Target file: {output_path}")

    ctx = ssl._create_unverified_context()

    req = urllib.request.Request(
        PRIMARY_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as response, open(output_path, 'wb') as out_file:
            total_size = int(response.info().get('Content-Length', -1))
            chunk_size = 1024 * 1024
            downloaded = 0
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                out_file.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    pct = (downloaded / total_size) * 100
                    print(f"Progress: {downloaded / (1024*1024):.1f} MB / {total_size / (1024*1024):.1f} MB ({pct:.1f}%)", end="\r")
        print(f"\nDownload completed successfully: {output_path} ({os.path.getsize(output_path):,} bytes)")
        return output_path
    except Exception as e:
        print(f"\nDirect automated download failed ({e}).")
        return None

if __name__ == "__main__":
    download_grace_mascons()
