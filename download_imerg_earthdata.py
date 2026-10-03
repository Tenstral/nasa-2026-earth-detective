"""
NASA Space Apps 2026 - Trend Detective: Bengal Water Paradox
Official NASA GPM IMERG Downloader (via NASA Earthdata / earthaccess)

Downloads official GPM IMERG Monthly Final Run (GPM_3IMERGM v07B) HDF5/NetCDF files
from NASA GES DISC using Earthdata credentials.

Requirements:
    pip install earthaccess
    Free account at: https://urs.earthdata.nasa.gov/

Usage:
    python download_imerg_earthdata.py --month YYYY-MM
    python download_imerg_earthdata.py --year 2024
"""

import os
import sys
import argparse
from pathlib import Path


def download_official_imerg(year: int, month: int = None, output_dir: str = "data_imerg"):
    try:
        import earthaccess
    except ImportError:
        print("[!] The 'earthaccess' package is required for official NASA Earthdata downloads.")
        print("    Install it via: pip install earthaccess")
        sys.exit(1)

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print("Authenticating with NASA Earthdata Login...")
    print("If not logged in, you will be prompted for your Earthdata credentials.")
    auth = earthaccess.login(strategy="interactive", persist=True)

    if month is not None:
        start_date = f"{year}-{month:02d}-01"
        # End date
        if month == 12:
            end_date = f"{year}-12-31"
        else:
            end_date = f"{year}-{month:02d}-28"
    else:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

    print(f"Searching NASA GES DISC for GPM_3IMERGM between {start_date} and {end_date}...")
    results = earthaccess.search_data(
        short_name="GPM_3IMERGM",
        temporal=(start_date, end_date),
        bounding_box=(88.0, 20.4, 92.8, 26.8)  # Bangladesh bounding box
    )

    if not results:
        print(f"No GPM_3IMERGM files found for {start_date} to {end_date}.")
        return []

    print(f"Found {len(results)} IMERG monthly granules. Downloading to {output_dir}...")
    downloaded_files = earthaccess.download(results, output_dir)
    print(f"Download complete: {len(downloaded_files)} files saved.")
    return downloaded_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download official NASA GPM IMERG monthly files.")
    parser.add_argument("--month", type=str, default=None, help="Specific month (YYYY-MM).")
    parser.add_argument("--year", type=int, default=2024, help="Target year (default: 2024).")
    parser.add_argument("--output-dir", type=str, default="data_imerg", help="Output directory.")

    args = parser.parse_args()

    if args.month:
        parts = args.month.split("-")
        y = int(parts[0])
        m = int(parts[1])
        download_official_imerg(year=y, month=m, output_dir=args.output_dir)
    else:
        download_official_imerg(year=args.year, output_dir=args.output_dir)
