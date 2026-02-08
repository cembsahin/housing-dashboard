"""
Download housing market data from Zillow Research.

Zillow publishes free CSV datasets at https://www.zillow.com/research/data/
This script downloads the ZHVI (Zillow Home Value Index) dataset,
which tracks median home values by state over time.

Usage:
    python scripts/download_data.py
"""

import os
import requests
import pandas as pd


# Zillow Home Value Index - All Homes, Smoothed, Seasonally Adjusted (by State)
ZHVI_URL = (
    "https://files.zillowstatic.com/research/public_csvs/zhvi/"
    "State_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def download_zhvi():
    """Download the Zillow Home Value Index CSV."""
    os.makedirs(DATA_DIR, exist_ok=True)
    output_path = os.path.join(DATA_DIR, "zhvi_by_state.csv")

    print(f"Downloading ZHVI data from Zillow...")
    print(f"URL: {ZHVI_URL}")

    try:
        response = requests.get(ZHVI_URL, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"\n❌ Download failed: {e}")
        print("\nThe Zillow URL may have changed. You can manually download the data:")
        print("1. Go to https://www.zillow.com/research/data/")
        print("2. Select 'ZHVI All Homes (SFR, Condo/Co-op) Time Series, Smoothed, Seasonally Adjusted'")
        print("3. Choose 'State' as the geography")
        print("4. Save the CSV to the data/ folder as 'zhvi_by_state.csv'")
        return False

    with open(output_path, "wb") as f:
        f.write(response.content)

    # Quick validation
    df = pd.read_csv(output_path)
    print(f"\n✅ Success! Saved to {output_path}")
    print(f"   States: {len(df)}")
    print(f"   Date columns: {len([c for c in df.columns if c.startswith('20')])}")
    print(f"   Date range: {sorted([c for c in df.columns if c.startswith('20')])[0]} → {sorted([c for c in df.columns if c.startswith('20')])[-1]}")

    return True


if __name__ == "__main__":
    download_zhvi()
