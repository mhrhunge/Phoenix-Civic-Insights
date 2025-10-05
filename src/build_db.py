import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "outputs" / "phoenix_civic.db"
SCHEMA = ROOT / "sql" / "schema.sql"


def main():
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    try:
        with open(SCHEMA, "r") as f:
            con.executescript(f.read())

        # Load water production
        water = pd.read_csv(ROOT/"data"/"phoenix_water_production.csv")
        water.columns = [c.strip().lower().replace(" ", "_") for c in water.columns]
        if "millions_of_gallons_" in water.columns and "millions_of_gallons" not in water.columns:
            water = water.rename(
                columns={"millions_of_gallons_": "millions_of_gallons"})
        water = water.rename(columns={"millions_of_gallons": "million_gallons"})

            # Coerce to numeric (handles commas, blanks)
        water["year"]           = pd.to_numeric(water["year"], errors="coerce")
        water["month"]          = pd.to_numeric(water["month"], errors="coerce")
        water["million_gallons"] = pd.to_numeric(
        water["million_gallons"].astype(str).str.replace(",", "").str.strip(),
        errors="coerce"
        )

        # Remove rows that failed conversion
        water = water.dropna(subset=["year","month","million_gallons"])
        water["year"]  = water["year"].astype(int)
        water["month"] = water["month"].astype(int)

        water = water[["year","month","million_gallons"]]
        water.to_sql("phoenix_water_production", con, if_exists="replace", index=False)

        # Calls for Service (concat selected years)
        frames = []
        for p in (ROOT/"data").glob("phoenix_calls_for_service_*.csv"):
            df = pd.read_csv(p, dtype=str)
            df.columns = [c.strip().lower() for c in df.columns]
            keep = ["incident_num", "disp_code", "disposition", "final_radio_code",
                "final_call_type", "call_received", "hundredblockaddr", "grid"]
            present = [c for c in keep if c in df.columns]
            df = df[present]
            frames.append(df)
        if frames:
            calls = pd.concat(frames, ignore_index=True)
            if "incident_num" in calls.columns:
                calls = calls.drop_duplicates(subset=["incident_num"])
            calls.to_sql("phoenix_calls_for_service", con,
                         if_exists="replace", index=False)

        con.commit()
        print(f"Database built at {DB}")
    finally:
        con.close()

if __name__ == "__main__":
    main()
