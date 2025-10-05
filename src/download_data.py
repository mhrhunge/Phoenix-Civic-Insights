import os
from pathlib import Path
import requests

DATA = Path(__file__).resolve().parents[1] / "data"
DATA.mkdir(parents=True, exist_ok=True)

# City of Phoenix Open Data (CKAN) CSVs
WATER_URL = "https://www.phoenixopendata.com/dataset/72820655-3350-44b3-85aa-ed72e78790e9/resource/d5a9b25f-645f-4627-b885-35df56827ecd/download/water-total-produced-million-gallons_water-total-produced-million-gallons_water-production.csv"

CALLS_BASE = "https://www.phoenixopendata.com/dataset/64a60154-3b2d-4583-8fb5-6d5e1b469c28/resource"
YEARS = [2025]  # add 2024, 2023 if desired
CALLS_IDS = {
    2025: "00775c9c-026d-41e5-a4f4-057ad60bea90",
    2024: "e8417a83-fcad-4cad-803c-423de3ad2d92"
}
CALLS_NAME = {
    2025: "calls-for-service_2025-calls-for-service_callsforsrvc2025.csv",
    2024: "calls-for-service_2024-calls-for-service_callsforsrvc2024.csv"
}

def download_file(url: str, dest: Path):
    print(f"Downloading: {url}")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    print(f"Saved to {dest} ({len(resp.content)/1_000_000:.1f} MB)")

def main():
    # Water
    water_path = DATA / "phoenix_water_production.csv"
    download_file(WATER_URL, water_path)

    # Calls for Service (selected years)
    for y in YEARS:
        rid = CALLS_IDS[y]
        fname = CALLS_NAME[y]
        url = f"{CALLS_BASE}/{rid}/download/{fname}"
        dest = DATA / f"phoenix_calls_for_service_{y}.csv"
        download_file(url, dest)

if __name__ == "__main__":
    main()
