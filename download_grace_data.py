"""
NASA Space Apps 2026 - Trend Detective: Bengal Water Paradox
CSR GRACE / GRACE-FO RL06.3 Mascon Downloader

Automates downloading of CSR GRACE/GRACE-FO Mascon NetCDF solutions
from official mirrors (UT CSR / NASA PO.DAAC).
"""

import os
import sys
import argparse
import urllib.request
from pathlib import Path

PRIMARY_URL = "http://download.csr.utexas.edu/outgoing/grace/RL0602_mascons/CSR_GRACE_GRACE-FO_RL0602_Mascons_all-corrections.nc"
TARGET_FILENAME = "CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc"

def download_grace_mascons(output_path: str = TARGET_FILENAME):
    print(f"Connecting to CSR GRACE Mascon distribution mirror...")
    print(f"Target file: {output_path}")

    req = urllib.request.Request(
        PRIMARY_URL,
        headers={"User-Agent": "NASA-SpaceApps-TrendDetective/1.0 (Earth Science Research)"}
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response, open(output_path, 'wb') as out_file:
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
        print(f"\nDownload completed successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"\nDirect automated download failed ({e}).")
        print("Note: If the mirror returns 403 or blocks CLI user-agents, download manually from:")
        print("https://www2.csr.utexas.edu/grace/RL0602_mascons.html or NASA Earthdata PO.DAAC Drive.")
        return None

if __name__ == "__main__":
    download_grace_mascons()
